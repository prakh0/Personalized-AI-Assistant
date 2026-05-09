# Personalized AI Assistant

A personalized AI assistant that can automatically respond to messages across **WhatsApp** and **Gmail** using LLM such as Gemini, Mistral, and Qwen. The assistant supports intelligent conversations, automated replies, file sharing and real-time information retrieval through external services and APIs.

## The project integrates:

- WhatsApp Webhooks using Meta WhatsApp Cloud API + ngrok
- Gmail API for reading and replying to emails
- LLM Integration using Gemini, Mistral, and Qwen models
- Conversation memory with recent message context
- RAG pipeline for semantic retrieval and context-aware responses
- REST API backend using FastAPI
- Task scheduling using APScheduler

The system uses FastAPI as the backend and integrates with LLM APIs for intelligent automated conversations.

---

# KEY Features

## WhatsApp Integration
- Receives incoming WhatsApp messages through webhooks
- Uses Meta WhatsApp Cloud API with ngrok
- Generates AI-powered replies automatically
- Maintains conversation context
- Supports intelligent and context-aware interactions

## Gmail Integration
- Reads incoming emails using Gmail API
- Generates AI-powered email replies
- Maintains conversation history
- Supports automated email workflows

## LLM Support
- Integrates with Gemini, Mistral, and Qwen APIs
- Easily switch between different LLM providers
- Unified provider-based architecture
- Supports LiteLLM integration

## RAG Support
- Retrieval-Augmented Generation (RAG) pipeline
- Semantic search using vector embeddings
- Personalized document retrieval
- Context-aware response generation
- Improved response accuracy using external knowledge

## Memory System
- Stores recent conversation history
- Shared memory support across WhatsApp and Gmail
- Configurable memory window
- Personalized contextual responses

## File & Information Handling
- Supports sending files and attachments
- Fetches real-time information from external APIs
- Supports search and summarization workflows
- Automated information retrieval

## Scheduler Support
- Background task scheduling using APScheduler
- Automated periodic jobs
- Scheduled update delivery
- Async workflow support

## Backend Architecture
- REST API backend using FastAPI
- Modular service-based architecture
- PostgreSQL integration
- Scalable and extensible project structure 

---

# Project Structure

# Project Structure

```bash
app/
│
├── main.py
│
├── communication/
│     ├── gmail.py
│     └── whatsapp.py 
│
├── db/
│   └── postgres.py
│
├── llm/
│   └── provider.py
│
├── memory/
│   └── store.py
│
├── rag/
│   ├── chucking.py
│   ├── embedding.py
│   ├── pipeline.py
│   ├── retrieve.py
│   └── vector_store.py
│
├── reply/
│   ├── chat.py
│   ├── detect_intension.py
│   ├── search.py
│   └── summary.py
│
├── services/
│   ├── prompt.py
│   ├── scheduler.py
│   └── stocks.py
│
├── tokens/
└──.gitignore
```    
---

# Project Architecture 

## WhatsApp Flow (Webhook-based)

```text
Incoming WhatsApp Message
        ↓
┌────────────────────────────┐
│ Meta WhatsApp Cloud API    │
└───────────┬────────────────┘
            │ (Webhook via ngrok)
            ▼
┌────────────────────────────┐
│       FastAPI App          │   ← main.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│     Intent Detection       │   ← detect_intension.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│      Memory System         │   ← memory/store.py
│    + RAG Retrieval         │
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│        RAG Pipeline        │   ← rag/pipeline.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│       LLM Providers        │   ← gemini.py / provider.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│    Response Generation     │   ← chat.py
└───────────┬────────────────┘
            ▼
Reply sent back to WhatsApp
```

---

## Gmail Flow (Independent Script)

```text
Incoming Email
      ↓
┌────────────────────────────┐
│         Gmail API          │
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│       Gmail Script         │   ← gmail.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│      Intent Detection      │   ← detect_intension.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│      Memory Retrieval      │   ← memory/store.py
│     + RAG Retrieval        │
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│        RAG Pipeline        │   ← rag/pipeline.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│       LLM Providers        │   ← gemini.py / provider.py
└───────────┬────────────────┘
            ▼
┌────────────────────────────┐
│       Email Reply          │   ← chat.py
└───────────┬────────────────┘
            ▼
Reply sent back to Gmail
```

---
# Installation

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

## 2. Create Virtual Environment

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
# LLM
LLM_MODEL=qwen
OPENAI_API_KEY=your_key_if_needed

# WhatsApp Cloud API
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_verify_token

# Gmail
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_REFRESH_TOKEN=your_refresh_token

# ngrok
NGROK_URL=your_ngrok_url
```

---

# Running the Project

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## Start ngrok

```bash
ngrok http 8000
```

Copy the generated public URL and configure it in:

- Meta WhatsApp webhook settings
- Gmail callback configuration (if required)

---

# Gmail Setup

1. Create a project in Google Cloud Console
2. Enable Gmail API
3. Create OAuth credentials
4. Generate refresh token
5. Add credentials to `.env`

---

# Meta WhatsApp Cloud API Setup

1. Create a Meta Developer account
2. Create a WhatsApp Cloud API application
3. Configure webhook URL

Point webhook to:

```text
https://your-ngrok-url/webhook/whatsapp
```

---

# Memory System

The project supports conversation memory to maintain context across messages.

Example:

```python
user_memory[user_id] = [
    "Hello",
    "Hi, how can I help you?",
    "Tell me about vector embeddings"
]
```

You can limit stored history:

```python
MAX_HISTORY = 5
```

---

# Switching LLM Models

The project is designed so you can easily swap models without changing business logic.

Example:

```python
MODEL_NAME = "qwen"
```

Switch to another provider/model:

```python
MODEL_NAME = "mistral"
```

---

# Scheduler Example

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
scheduler.start()
```

Example scheduled task:

```python
scheduler.add_job(
    send_daily_updates,
    trigger='cron',
    hour=9,
    minute=0
)
```

---

# Features Enabled After Setup

- WhatsApp AI replies
- Gmail AI replies
- RAG-based contextual responses
- Conversation memory
- Semantic search
- File sharing support
- Real-time information retrieval
- Scheduled background tasks

---
# Core Components

| Component        | Responsibility |
|------------------|----------------|
| `communication/` | Handles WhatsApp and Gmail integrations |
| `llm/`           | LLM provider integrations and response generation |
| `memory/`        | Stores and retrieves conversation history |
| `rag/`           | Retrieval-Augmented Generation pipeline and semantic search |
| `reply/`         | Intent detection, chat responses, search, and summarization |
| `services/`      | Background jobs, scheduling, and utility services |
| `db/`            | Database connection and vector storage |
| `tokens/`        | OAuth credentials and authentication tokens |
| `main.py`        | FastAPI entry point and webhook handling |
---
## Performance Notes

- Response latency depends on external LLM API response times
- RAG retrieval adds minimal overhead before response generation
- Embedding generation time varies based on document size
- Larger conversation history increases prompt processing latency
- PostgreSQL + pgvector enables efficient semantic retrieval
- ngrok may introduce slight webhook latency during local development
- Background jobs run independently using APScheduler
- FastAPI async architecture supports concurrent request handling

---
# Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | FastAPI, Python, Uvicorn |
| **LLM APIs** | Gemini API, Mistral API, Qwen |
| **RAG Pipeline** | Vector Embeddings, Semantic Search, Retrieval-Augmented Generation |
| **Database** | PostgreSQL, pgvector |
| **Communication** | Meta WhatsApp Cloud API, Gmail API |
| **Scheduling** | APScheduler |
| **Authentication** | OAuth 2.0 |
| **Tunneling** | ngrok |
| **Architecture** | REST APIs, Webhooks, Async Processing |

---
# Future Improvements

- Long-term vector memory
- Advanced RAG pipeline optimization
- Multi-user conversation isolation
- Voice interaction support
- Telegram integration
- Discord integration
---