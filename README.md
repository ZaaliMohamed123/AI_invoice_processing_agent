# 🧾 AI Invoice Processing Agent

**Cutting-edge, production-ready LangChain + LangGraph project for automated PDF invoice understanding and approval.**

---

## 🚀 Overview

The AI Invoice Processing Agent is an advanced open-source workflow for automatically extracting, validating, and processing invoice documents using state-of-the-art LLMs. It blends:
- 📄 PDF ingestion
- 🤖 LLM-powered information extraction (OpenAI, Gemini, Claude, etc)
- 🧩 Modular validation and business rule enforcement
- ✉️ Automated email notification on approval or rejection
- 🖥️ A modern Gradio web interface

**Demonstrates best practices for real-world GenAI workflow engineering!**

---

## ✨ Features

- **Upload and Process**: Drag-and-drop PDF invoices for analysis
- **Structured Extraction**: Auto-populates all key invoice fields with GPT-4/Claude/Gemini
- **Calculation Checks**: Math validation on line items, totals, tax
- **Business Policy Checks**: Enforces custom rules (field requirements, amount limits, duplicate detection)
- **Automated Decisions**: Auto-approve or reject invoices with a clear explanation
- **Notifications**: Sends approval/rejection emails with details, out-of-the-box via Gmail
- **Production Architecture**: LangChain + LangGraph nodes, modularity, .env setup for secrets, high code quality

---

## 📦 Project Structure

```
AI_invoice_processing_agent/
├── src/
│   ├── app.py                # Gradio web interface
│   ├── graph.py              # Wires the full LangGraph pipeline
│   ├── state.py              # State schema for workflow
│   ├── nodes/                # Modular nodes for each stage
│   ├── models/               # Pydantic models (invoice data)
│   ├── services/             # PDF, LLM, Email services
│   └── config/               # Environment settings
├── sample_invoices/          # Add your test PDFs here
├── .env                      # Your API keys & secrets
├── requirements.txt
└── README.md
```

---

## 🧑‍💻 Quickstart

1. **Clone & Enter**
   ```bash
   git clone https://github.com/ZaaliMohamed123/AI_invoice_processing_agent.git
   cd AI_invoice_processing_agent
   ```

2. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Open `.env`, fill in:
     ```ini
     OPENAI_API_KEY=...
     OPENAI_BASE_URL=https://api.openai.com/v1
     GMAIL_ADDRESS=your-gmail@gmail.com
     GMAIL_APP_PASSWORD=your-app-password
     NOTIFICATION_EMAIL=recipient@example.com
     ```
   - [How to get a Gmail App Password?](https://support.google.com/accounts/answer/185833)

4. **Run**
   ```bash
   python -m src.app
   # Open browser: http://localhost:7860
   ```

5. **Upload Invoice, Process, Receive Email!**

---

## 🛠️ Technologies Used

- **LangChain** (⬆️ 2024 best-practice, multi-node pipeline)
- **LangGraph** (Cutting-edge AI workflow orchestration)
- **OpenAI GPT-4, GPT-3.5 and compatible models**
- **Gradio** (Modern Python UIs for ML/AI)
- **pdfplumber** (Structured PDF text extraction)
- **Pydantic** (Type-checked LLM output contract)
- **Python-dotenv** (Configurable & secure with .env)

---

## 🏆 Why This Project Stands Out

- **Real LangGraph Patterns**: Not a toy! Shows production-ready node separation, state design, business logic, and error handling.
- **Robust & Safe**: Handles PDF corruptions, AI errors, and calculation edge cases. Never stores secrets in source.
- **Extendable**: Want human-in-the-loop review? Azure or Gemini? New business logic? Just add a node!
- **Career-Ready Code**: High readability, clear docstrings, and modern tools – ideal portfolio centerpiece for AI, LLM, and automation jobs.

---

## 🤝 Contributing

Found a bug? Have an idea or want to integrate more features? [Open an issue or pull request](https://github.com/ZaaliMohamed123/AI_invoice_processing_agent/pulls)!

---

## 🙋 FAQ

### How do I get a Gmail App Password?
- Visit your [Google Account security page](https://myaccount.google.com/security)
- Enable 2-Step Verification
- Go to "App Passwords", create one for this app, and use it as `GMAIL_APP_PASSWORD` in your `.env`. Learn more in [Google's docs](https://support.google.com/accounts/answer/185833)

### Can I use other LLMs?
- Absolutely! Update `OPENAI_BASE_URL` and `OPENAI_API_KEY` to Gemini, Claude, Azure, or even Ollama (local) endpoints. The modular design makes it easy.

### Is my data secure?
- Yes. Environment vars are kept out of Git. No PDFs or extracted data are stored server-side by default.

---

## 📮 Contact

- [Zaali Mohamed](https://www.linkedin.com/in/zaalimohamed/) (Project Author)
- [Open an Issue](https://github.com/ZaaliMohamed123/AI_invoice_processing_agent/issues)

---

**If you find this project useful, please ⭐ star the repo or share it to help others!**
