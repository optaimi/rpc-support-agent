# Blockchain Support Agent ⚡🤖

A production-ready diagnostic tool designed to automate "Tier 1 Support" for blockchain infrastructure. It acts as a bridge between raw JSON-RPC errors and human-readable support tickets, using **GPT-4.1-mini** to instantly draft technical, accurate responses.

![App Screenshot](https://via.placeholder.com/800x400?text=Blockchain+Support+Agent+Demo)

## 🎯 Project Goal
In high-volume support environments, engineers often spend time decoding standard EVM errors (like `-32000: execution reverted`). I built this tool to demonstrate how AI can:
1.  **Intercept** the raw JSON error.
2.  **Analyze** the context (Method + Error Code).
3.  **Draft** a polite, technically accurate response in <3 seconds.

## 🚀 Key Features

### 1. Dual Diagnostic Modes
* **Fault Simulator:** One-click simulation of common blockchain errors to test the agent's reasoning.
    * *Scenario A:* `eth_estimateGas` from a zero-balance wallet (Insufficient Funds).
    * *Scenario B:* Smart Contract Revert (Execution Reverted).
    * *Scenario C:* Invalid Gas Parameters (Intrinsic Gas Too Low).
* **✍️ Manual Input Mode:** A "Utility Mode" that allows support engineers to paste **real raw error data** from actual customer tickets to get an instant analysis.

### 2. Intelligent Analysis
* Instantly translates cryptic error codes into a **"Root Cause"** internal note for the engineer.
* Drafts a **"Client Reply"** that is empathetic, professional, and company-agnostic (signed simply as "Support Team").

### 3. Security & Production Standards
* **Credential Masking:** API keys and RPC endpoints are strictly hidden in the UI to prevent leaks during screen shares or demos.
* **Environment Security:** All sensitive configuration is managed via `.env` files, never hardcoded.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **Blockchain:** Ethereum JSON-RPC (Interacts with live nodes)
* **AI Engine:** OpenAI GPT-4.1-mini (Optimized for JSON output & speed)

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/rpc-support-agent.git](https://github.com/YOUR_USERNAME/rpc-support-agent.git)
    cd rpc-support-agent
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**
    Create a file named `.env` in the root folder:
    ```ini
    OPENAI_API_KEY="sk-..."
    # Your JSON-RPC Endpoint (e.g., QuickNode, Alchemy, or Public)
    QUICKNODE_RPC_URL="[https://eth.llamarpc.com](https://eth.llamarpc.com)"
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 🧪 How to Use

### Simulator Mode (Demo)
1.  Select a scenario from the dropdown (e.g., **💰 Insufficient Funds**).
2.  Click **🔴 Trigger Simulation**.
3.  The app sends a live request to the RPC node, catches the specific error, and passes it to the AI.
4.  View the **Internal Note** and the **Drafted Reply**.

### Manual Mode (Real World)
1.  Select **✍️ Manual Error Input** from the dropdown.
2.  Paste an Error Code (e.g., `-32601`) and Message (e.g., `Method not found`).
3.  Click **🧠 Analyse Manual Error** to see how the agent handles custom data.

---
*Developed as a portfolio project to demonstrate AI integration in Support Engineering workflows.*