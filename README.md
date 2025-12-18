# QuickNode AI Support Agent ⚡🤖

A production-ready diagnostic tool designed to automate "Tier 1 Support" for blockchain infrastructure. It intercepts raw JSON-RPC errors and uses **GPT-4.1-mini** to instantly draft technical, accurate responses for customers.

![App Screenshot](https://via.placeholder.com/800x400?text=Blockchain+API+Support+Agent+Demo)

## 🎯 Why I Built This
In high-volume support environments, speed and accuracy are critical. I built this tool to demonstrate how we can use AI to bridge the gap between raw infrastructure errors and human-readable support tickets.

### 📊 Benchmark Decision: Why GPT-4.1-mini?
I benchmarked multiple models for this specific "JSON-RPC Root Cause Analysis" task.
* **GPT-5.1:** High quality, but too slow (~18s latency).
* **GPT-5-mini:** Struggled with strict JSON formatting.
* **GPT-4.1-mini:** **The Winner.** It delivered 95% of the reasoning quality in **<2.5 seconds** and correctly identified edge cases (like Zero Address errors) that older models missed.

## 🚀 Key Features
* **Fault Simulation:** One-click simulation of common user errors (e.g. `eth_estimateGas` from a zero-balance wallet).
* **Intelligent Analysis:** Instantly translates cryptic error codes (e.g. `-32000: execution reverted`) into a "Root Cause" note for engineers and a "Polite Reply" for customers.
* **Raw Debug View:** Allows support staff to inspect the raw JSON payload to verify the AI's findings.
* **Production Ready:** Built with Type Hinting, Environment Security (.env), and Robust Error Handling.

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Python)
* **Blockchain:** Ethereum JSON-RPC (QuickNode / Public LlamaNodes)
* **AI Engine:** OpenAI GPT-4.1-mini (JSON Mode)

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/optaimi/rpc-support-agent.git](https://github.com/optaimi/rpc-support-agent.git)
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
    # Optional: Use your own QuickNode Endpoint (defaults to public if omitted)
    QUICKNODE_RPC_URL="[https://your-endpoint.quiknode.pro/](https://your-endpoint.quiknode.pro/)..."
    ```

4.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 🧪 How to Test (Demo Flow)
1.  Launch the app.
2.  In the left column, click **🔴 Trigger Failed Transaction**.
3.  This simulates an `eth_estimateGas` call from the "Zero Address" (`0x00...00`).
4.  Watch the AI Agent in the right column automatically:
    * Detect the `-32000` error.
    * Analyse the root cause (Invalid Sender/No Funds).
    * Draft a support ticket response signed by the "Support Team".

---
*Developed as a proof-of-concept for the QuickNode Support Engineering role.*