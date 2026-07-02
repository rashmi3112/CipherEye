---
title: CipherEye
sdk: docker
app_port: 7860
pinned: false
---

# CipherEye 👁️ — AI-Powered Cybersecurity Investigation Platform

> **Kaggle Gemini API Developer Competition Submission**

CipherEye is an end-to-end AI cybersecurity threat analysis platform that uses a **multi-agent system powered by Google Gemini** to investigate URLs, text messages, emails, and images for phishing campaigns, social engineering attacks, and PII exposure — and returns a structured, human-readable investigation report with a trust score.

🔗 **Live Demo (Hugging Face Spaces):** [rashmiunhale/ciphereye](https://huggingface.co/spaces/rashmiunhale/ciphereye)

---

## 🧩 The Problem

Cybersecurity threats like phishing, scams, and social engineering attacks are increasing in sophistication and volume. Everyday users — and even trained professionals — struggle to identify malicious URLs, deceptive emails, and fake login pages before it is too late.

Current limitations:
- Existing URL scanners are rule-based and cannot reason about novel patterns.
- Manual threat analysis is slow, requires domain expertise, and does not scale.
- Sensitive PII (names, SSNs, card numbers) in analyzed content can itself be leaked if sent raw to third-party APIs.
- There is no single unified tool that combines URL, text, and image threat detection.

---

## 💡 The Solution

CipherEye solves this by orchestrating a **5-agent AI pipeline** backed by **Google Gemini 2.5 Flash** to perform deep, contextual threat analysis.

Key differentiators:
- **Privacy-first**: All text is scanned by a local **Microsoft Presidio + spaCy** NLP engine to mask PII *before* it ever reaches an LLM.
- **Multi-modal**: Analyzes URLs, raw text/emails, and images in one unified interface.
- **Explainable**: Returns structured findings, threat categories, trust scores (0–100), and actionable recommendations — not just a binary result.
- **Extensible**: An MCP (Model Context Protocol) manager allows agents to call external tools (e.g., domain reputation APIs, OCR services) via SSE streams.
- **Production-ready**: Deployed as a Docker container on Hugging Face Spaces; built-in prompt injection defense and exponential backoff for rate limits.

---

## 🏗️ Architecture

CipherEye uses a sequential multi-agent pipeline where each agent has a single, focused responsibility.

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Frontend  (React + Vite + TS)                  │
│           Home Page ──► Analyze Page ──► Report Page                │
└────────────────────────────┬────────────────────────────────────────┘
                             │  POST /api/v1/analyze
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Backend  (FastAPI)                               │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  1. Security Guardrails  (core/security.py)                  │   │
│  │     • Prompt injection heuristics                            │   │
│  │     • Input sanitization                                     │   │
│  └──────────────────────┬───────────────────────────────────────┘   │
│                          │                                           │
│  ┌──────────────────────▼───────────────────────────────────────┐   │
│  │  2. PII Agent  (agents/pii_agent.py)                         │   │
│  │     • Microsoft Presidio + spaCy (offline NLP)               │   │
│  │     • Detects & masks: EMAIL, PHONE, SSN, CREDIT_CARD, etc.  │   │
│  └──────────────────────┬───────────────────────────────────────┘   │
│                          │  masked + safe content                    │
│  ┌──────────────────────▼───────────────────────────────────────┐   │
│  │  3. Orchestrator  (agents/orchestrator.py)                   │   │
│  │     Routes to the correct specialized agent by content type  │   │
│  │                                                              │   │
│  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │   │
│  │   │  URL Agent   │  │  Text Agent  │  │ Image Agent  │     │   │
│  │   │  phishing /  │  │  email scam/ │  │ multimodal   │     │   │
│  │   │  typosquat   │  │  social eng. │  │ screenshot   │     │   │
│  │   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │   │
│  │          └─────────────────┼──────────────────┘             │   │
│  │                            │  raw findings                  │   │
│  │   ┌────────────────────────▼──────────────────────────┐     │   │
│  │   │  4. Threat Agent  (agents/threat_agent.py)        │     │   │
│  │   │     • Consolidates all findings                   │     │   │
│  │   │     • Calculates Trust Score (0–100)              │     │   │
│  │   │     • Final Risk Level: low / medium / high /     │     │   │
│  │   │       critical                                    │     │   │
│  │   └────────────────────────┬──────────────────────────┘     │   │
│  │                            │                                │   │
│  │   ┌────────────────────────▼──────────────────────────┐     │   │
│  │   │  5. Report Agent  (agents/report_agent.py)        │     │   │
│  │   │     • Human-readable summary                      │     │   │
│  │   │     • Actionable recommendations                  │     │   │
│  │   └────────────────────────┬──────────────────────────┘     │   │
│  └──────────────────────────── ┘                                │   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Base Agent (agents/base_agent.py)  — shared by all agents  │   │
│  │     • Google GenAI SDK wrapper (gemini-2.5-flash)           │   │
│  │     • Structured JSON schema enforcement                     │   │
│  │     • Retry with exponential backoff on rate limits          │   │
│  │     • Content-aware offline mock fallback                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  MCP Manager (mcp/client_manager.py)  — optional             │   │
│  │     • SSE connections to external MCP tool servers           │   │
│  │     • Search / domain reputation / OCR integrations         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
           ┌─────────────────────────────┐
           │  Google Gemini 2.5 Flash    │
           │  (structured JSON output)   │
           └─────────────────────────────┘
```

### Agent Responsibilities

| Agent | Tool / Model | Responsibility |
| :--- | :--- | :--- |
| **PII Agent** | Microsoft Presidio + spaCy `en_core_web_sm` | Detect & mask PII from text before it reaches any LLM |
| **URL Agent** | Gemini 2.5 Flash | Typosquatting, phishing params, suspicious TLDs |
| **Text Agent** | Gemini 2.5 Flash | Urgency/scarcity language, impersonation, scam signals |
| **Image Agent** | Gemini 2.5 Flash (multimodal) | Spoofed login pages, fake interfaces in screenshots |
| **Threat Agent** | Gemini 2.5 Flash | Consolidate findings → Trust Score + Risk Level |
| **Report Agent** | Gemini 2.5 Flash | Plain-language summary + mitigation recommendations |

### Data Flow Summary

```
User Input (URL / Text / Email / Image)
    │
    ├─► [Security] Prompt injection check + sanitize
    │
    ├─► [PII Agent] Mask SSN, email, card numbers (offline, local NLP)
    │
    ├─► [Content Agent] URL / Text / Image — Gemini structured analysis
    │
    ├─► [Threat Agent] Gemini — risk level, trust score, threat categories
    │
    └─► [Report Agent] Gemini — summary + recommendations
              │
              ▼
        InvestigationReport
        { trust_score, risk_level, threat_categories,
          summary, findings, confidence,
          recommendations, detected_pii }
```

---

## 🗂️ Project Structure

```
CipherEye/
├── Dockerfile                   # Multi-stage build: React → Python + FastAPI
├── README.md
│
├── backend/
│   ├── main.py                  # FastAPI app factory, SPA static file serving
│   ├── requirements.txt
│   └── app/
│       ├── agents/
│       │   ├── base_agent.py    # Google GenAI SDK wrapper (shared by all agents)
│       │   ├── orchestrator.py  # Agent coordinator & workflow manager
│       │   ├── pii_agent.py     # Microsoft Presidio PII detection & masking
│       │   ├── url_agent.py     # URL threat analysis agent
│       │   ├── text_agent.py    # Text/email analysis agent
│       │   ├── image_agent.py   # Image multimodal analysis agent
│       │   ├── threat_agent.py  # Threat consolidation & trust scoring agent
│       │   └── report_agent.py  # Report generation agent
│       ├── api/
│       │   └── endpoints.py     # POST /api/v1/analyze route
│       ├── core/
│       │   ├── config.py        # Pydantic settings (env vars)
│       │   └── security.py      # Prompt injection detection & input sanitizer
│       ├── mcp/
│       │   └── client_manager.py # MCP SSE client for external tool calls
│       └── models/
│           └── schemas.py       # Pydantic request/response models
│
└── frontend/
    ├── index.html
    └── src/
        ├── pages/
        │   ├── Home.tsx         # Landing page
        │   ├── Analyze.tsx      # Input form (URL / text / image tabs)
        │   └── Report.tsx       # Structured investigation report viewer
        ├── components/          # Reusable UI components
        │   ├── core/
        │   ├── input/
        │   ├── layout/
        │   ├── loading/
        │   └── report/
        └── services/
            └── api.ts           # Frontend API client
```

---

## ⚙️ Configuration & Environment Variables

Create a `.env` file inside the `backend/` directory:

| Variable | Description | Required | Default |
| :--- | :--- | :---: | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API key | ✅ Yes | — |
| `MOCK_LLM` | Use offline content-aware mock responses (for testing) | No | `False` |
| `ENABLE_PII_DETECTION` | Enable local Presidio PII masking | No | `True` |
| `MCP_SEARCH_URL` | SSE endpoint of an external MCP search server | No | — |
| `MCP_OCR_URL` | SSE endpoint of an external MCP OCR server | No | — |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Option 1 — Local Development (No Docker)

#### Backend
```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Download the spaCy NLP model for PII detection
python -m spacy download en_core_web_sm

# 5. Set your API key
echo "GEMINI_API_KEY=your_key_here" > .env

# 6. Start the FastAPI server
python main.py
# → Running at http://localhost:8000
```

#### Frontend
```bash
# In a new terminal
cd frontend

npm install
npm run dev
# → Running at http://localhost:5173
```

---

### Option 2 — Docker (Recommended for Production)

The included multi-stage `Dockerfile` builds the React frontend and bundles it with the Python backend, serving everything from a single container on port `7860`.

```bash
# 1. Build the image
docker build -t ciphereye .

# 2. Run the container
docker run -p 7860:7860 -e GEMINI_API_KEY="your_key_here" ciphereye

# 3. Open the dashboard
# → http://localhost:7860
```

---

### Option 3 — Hugging Face Spaces (Live Deployment)

This repository is configured as a **Docker Space** on Hugging Face. The YAML frontmatter at the top of this `README.md` defines the Space metadata (`sdk: docker`, `app_port: 7860`).

To deploy your own copy:
1. Fork this repository.
2. Create a new **Docker Space** on Hugging Face and link it to your fork.
3. Go to **Settings → Variables and Secrets** on your Space.
4. Add `GEMINI_API_KEY` as a secret.

The Space will auto-build and deploy on every push to `main`.

---

## 🔬 API Reference

### `POST /api/v1/analyze`

**Request body:**
```json
{
  "content_type": "url" | "text" | "email" | "image",
  "content": "<string or base64-encoded image>"
}
```

**Response (`InvestigationReport`):**
```json
{
  "trust_score": 5,
  "risk_level": "critical",
  "threat_categories": ["phishing", "impersonation"],
  "summary": "This email is a critical phishing attempt impersonating PayPal...",
  "findings": [
    "Sender domain matches known PayPal typosquatting patterns.",
    "Requests SSN, credit card number, and banking password."
  ],
  "confidence": 0.98,
  "recommendations": [
    "Do not click the link or enter any information.",
    "Report the attempt to PayPal's official security team."
  ],
  "detected_pii": [
    { "entity_type": "EMAIL_ADDRESS", "start": 12, "end": 35, "replacement": "<EMAIL_ADDRESS>" }
  ]
}
```

---

## 🧪 Running Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with mock LLM (no API key required)
MOCK_LLM=True pytest tests/ -v
```

---

## 🛡️ Security Design Decisions

| Decision | Rationale |
| :--- | :--- |
| **PII masked locally before LLM calls** | Prevents sensitive user data from being sent to third-party APIs |
| **Prompt injection heuristics at ingress** | Blocks adversarial inputs before they reach agent prompts |
| **Non-root Docker user** | Follows Hugging Face Spaces security requirements and container hardening best practices |
| **Structured JSON schema enforcement** | Forces Gemini to return parseable, validated output — prevents hallucinated free-form responses |
| **Exponential backoff on 429 errors** | Handles Gemini API rate limits gracefully without crashing |
| **Content-aware offline mock fallback** | Ensures the app stays functional during testing or API outages |

---

## 🤖 Gemini API Usage

CipherEye uses **Gemini 2.5 Flash** via the `google-genai` Python SDK. Key usage patterns:

- **Structured output**: Every agent passes a JSON `response_schema` to enforce typed, machine-parseable responses.
- **System instructions**: Each agent receives a tailored security-expert system prompt scoped to its specific analysis domain.
- **Multimodal analysis**: The Image Agent sends base64-encoded image data directly to Gemini's multimodal endpoint.
- **Model**: `gemini-2.5-flash` — chosen for its speed, cost-efficiency, and strong reasoning capabilities.

---

## 📦 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI / LLM** | Google Gemini 2.5 Flash (`google-genai` SDK) |
| **PII Detection** | Microsoft Presidio, spaCy `en_core_web_sm` |
| **Data Validation** | Pydantic v2 |
| **External Tools** | MCP (Model Context Protocol) via SSE |
| **Containerization** | Docker (multi-stage build) |
| **Deployment** | Hugging Face Spaces (Docker SDK) |

---

## 📄 License

This project was created for the **Kaggle Gemini API Developer Competition**.
