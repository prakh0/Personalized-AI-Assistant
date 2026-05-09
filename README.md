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
# Setup Guide

## 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Personalized-AI-Assistant
```
---

## 2. Create Virtual Environment

### macOS / Linux

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

Create a `.env` file in the root directory.

```env
# LLM APIs
GEMINI_API_KEY=your_gemini_api_key
MISTRAL_API_KEY=your_mistral_api_key

# WhatsApp Cloud API
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
WHATSAPP_VERIFY_TOKEN=your_verify_token

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

# ngrok
NGROK_URL=your_ngrok_url
```
---

# Gmail API Setup

## 1. Create Google Cloud Project

- Open Google Cloud Console
- Create a new project

---

## 2. Enable Gmail API

- Go to APIs & Services
- Enable Gmail API

---

## 3. Configure OAuth Consent Screen

- Configure app details
- Add test users if needed

---

## 4. Create OAuth Credentials

- Create OAuth Client ID
- Download credentials JSON file

Place the file inside:

```bash
app/tokens/
```

Example:

```bash
app/tokens/Oauth_cred_chatbot_gmail.json
```
---

## 5. Generate Gmail Token

Run your Gmail authentication script to generate:

```bash
token.json
```

This file should also be stored in:

```bash
app/tokens/
```
---

# WhatsApp Cloud API Setup

## 1. Create Meta Developer App

- Open Meta Developer Dashboard
- Create a new app
- Add WhatsApp product

---

## 2. Configure Webhook

Set webhook URL:

```text
https://your-ngrok-url/webhook/whatsapp
```

Verify using your:

```env
WHATSAPP_VERIFY_TOKEN
```
---

## 3. Add Access Token

Copy:
- Permanent Access Token
- Phone Number ID

Add them to `.env`

---

# PostgreSQL Setup

## Create Database

```sql
CREATE DATABASE personalized_ai_assistant;
```
---

## Enable pgvector Extension

```sql
CREATE EXTENSION vector;
```
---

# Run the Project

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```
---

## Start ngrok

```bash
ngrok http 8000
```
---

# RAG Setup

## 1. Ingest Documents

Run your ingestion pipeline:

```bash
python -m app.rag.pipeline
```
---

## 2. Generate Embeddings

Embeddings are generated using:

- Mistral Embeddings API
- Vector storage using PostgreSQL + pgvector

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

- Uses asynchronous FastAPI endpoints for efficient request handling
- Supports scalable webhook-based communication architecture
- Response latency depends on external LLM API response times
- RAG pipeline improves response relevance through semantic retrieval
- RAG retrieval adds minimal overhead before response generation
- PostgreSQL + pgvector enables efficient vector similarity search
- Embedding generation time varies based on document size
- Larger conversation history increases prompt processing latency
- Conversation memory reduces repeated context generation
- Embedding-based retrieval minimizes unnecessary LLM context usage
- Modular architecture allows easy scaling and provider switching
- APScheduler handles background jobs independently from request flow
- ngrok may introduce slight webhook latency during local development
- Designed for low-latency conversational workflows across WhatsApp and Gmail

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
- Distributed vector storage
- Autonomous AI workflows
- Multi-agent orchestration
- Real-time streaming responses
- File-aware contextual retrieval
- Advanced personalization layer

---

# Example Use Cases

- Personal AI assistant
- Automated customer support
- AI email responder
- AI WhatsApp bot
- Internal productivity assistant
- AI scheduling assistant
- Knowledge retrieval assistant
- AI-powered workflow automation
- Intelligent document assistant

---

# Author

## Prakhar Pandey

Creator of **Personalized AI Assistant**

Computer Science graduate focused on:

- Backend Engineering
- AI Integrations
- Retrieval-Augmented Generation (RAG)
- Distributed Systems
- Automation Tools
- Scalable AI Systems
