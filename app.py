import streamlit as st
import requests
import json
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION
# ==========================================
load_dotenv()

st.set_page_config(
    page_title="Blockchain API Support Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Constants
DEFAULT_RPC = os.environ.get("QUICKNODE_RPC_URL", "https://eth.llamarpc.com")
MODEL_ID = "gpt-4.1-mini"

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================


def clean_json_output(raw_text):
    """Robustly extracts JSON from the AI response."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise ValueError("AI did not return valid JSON.")


def analyze_error(api_key, rpc_url, error_code, error_msg, method):
    """Core logic: Sends error to OpenAI and parses result."""
    client = OpenAI(api_key=api_key)

    system_prompt = "You are a Senior Support Engineer working at a company like QuickNode. Output valid JSON only."
    user_prompt = f"""
    [CONTEXT]
    Endpoint: {rpc_url}
    Method: {method}
    Error Code: {error_code}
    Error Message: "{error_msg}"
    
    [TASK]
    Output a JSON object with exactly two keys:
    1. "root_cause": A technical, 1-sentence explanation (Internal Note).
    2. "client_reply": A polite, professional markdown response. 
       - Sign off simply as "Support Team", you do not represent any specific company.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            max_tokens=400,
            temperature=0.3,
        )
        return clean_json_output(response.choices[0].message.content)
    except Exception as e:
        return {
            "root_cause": "AI Processing Failed",
            "client_reply": f"System Error: {str(e)}",
        }


# ==========================================
# 3. USER INTERFACE
# ==========================================

# Sidebar
with st.sidebar:
    st.title("Settings")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        st.error("⚠️ OpenAI API Key Missing")
        st.stop()
    else:
        st.success(f"🟢 Model: {MODEL_ID}")

    # API/Endpoint Hidden for Security
    rpc_input = st.text_input(
        "RPC Endpoint",
        value=DEFAULT_RPC,
        type="password",
        help="The full URL is hidden for security.",
    )

    if rpc_input and "//" in rpc_input:
        try:
            domain = rpc_input.split("/")[2]
            st.caption(f"🔌 Connected to: `{domain}`")
        except Exception:
            st.caption("🔌 Connected")

    st.info(
        "ℹ️ Note: Transaction Hash input is disabled because `eth_estimateGas` is a pre-chain simulation."
    )

# Main Layout
st.title("⚡ Blockchain Support Agent")
st.markdown("### Automated Root-Cause Analysis for JSON-RPC Errors")
st.markdown("---")

col_left, col_right = st.columns([2, 3])

# LEFT COLUMN: Simulator
with col_left:
    st.subheader("1. Inject Fault")

    # 1. Select Scenario
    scenario = st.selectbox(
        "Select Error Scenario:",
        [
            "📉 Execution Reverted (Smart Contract Logic)",
            "💰 Insufficient Funds (Gas/Value)",
            "⛽ Intrinsic Gas Too Low (Invalid Params)",
        ],
    )

    # 2. Define Parameters based on Selection (Happens BEFORE button click)
    if "Execution Reverted" in scenario:
        st.info(
            "Simulates sending 1 ETH to USDT contract from a Zero Address. \n\nExpected: `execution reverted` (-32000)"
        )
        payload_params = [
            {
                "from": "0x0000000000000000000000000000000000000000",
                "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "value": "0xDE0B6B3A7640000",
            }
        ]
    elif "Insufficient Funds" in scenario:
        st.info(
            "Simulates sending 100 ETH from a random empty wallet. \n\nExpected: `insufficient funds` (-32000)"
        )
        payload_params = [
            {
                "from": "0x1111111111111111111111111111111111111111",
                "to": "0x2222222222222222222222222222222222222222",
                "value": "0x56BC75E2D63100000",
            }
        ]
    elif "Intrinsic Gas" in scenario:
        st.info(
            "Simulates a transaction with Gas Limit = 10 (Impossible). \n\nExpected: `intrinsic gas too low` (-32000)"
        )
        payload_params = [
            {
                "from": "0x0000000000000000000000000000000000000000",
                "to": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "gas": "0xA",
            }
        ]

    st.markdown("<br>", unsafe_allow_html=True)  # Fixed the 'br' typo

    # 3. Trigger Simulation
    if st.button("🔴 Trigger Simulation", type="primary", use_container_width=True):
        with st.status("Sending RPC Request...", expanded=True) as status:
            payload = {
                "jsonrpc": "2.0",
                "method": "eth_estimateGas",
                "params": payload_params,
                "id": 1,
            }

            try:
                response = requests.post(rpc_input, json=payload, timeout=5)
                data = response.json()

                if "error" in data:
                    status.update(label="❌ RPC Error Caught!", state="error")
                    err_code = data["error"].get("code")
                    err_msg = data["error"].get("message")

                    st.error(f"**Code:** `{err_code}`")
                    st.error(f"**Message:** `{err_msg}`")

                    # Store for AI
                    st.session_state["active_error"] = (err_code, err_msg)
                    st.session_state["raw_debug"] = data
                else:
                    status.update(
                        label="⚠️ Transaction Succeeded (Unexpected)", state="complete"
                    )
                    st.json(data)

            except Exception as e:
                status.update(label="Connection Failed", state="error")
                st.error(f"Network Error: {e}")

# RIGHT COLUMN: AI Analysis
with col_right:
    st.subheader("2. AI Analysis")

    if "active_error" in st.session_state:
        code, msg = st.session_state["active_error"]

        with st.spinner(f"Consulting {MODEL_ID}..."):
            result = analyze_error(api_key, rpc_input, code, msg, "eth_estimateGas")

        # Internal Note
        st.markdown("**🔍 Root Cause (Internal Note)**")
        st.warning(result.get("root_cause"))

        # Client Reply
        st.markdown("**📝 Drafted Client Response**")
        st.success(result.get("client_reply"))

        col_a, col_b = st.columns([1, 4])
        with col_a:
            st.button("✅ Approve", type="secondary")

        st.divider()

        with st.expander("🛠️ View Raw JSON Debug Data"):
            st.json(st.session_state.get("raw_debug", {}))

    else:
        st.markdown(
            """
            <div style="padding: 40px; text-align: center; border: 1px dashed #ccc; border-radius: 10px; color: #666; margin-top: 20px;">
                Waiting for simulation event...
            </div>
            """,
            unsafe_allow_html=True,
        )
