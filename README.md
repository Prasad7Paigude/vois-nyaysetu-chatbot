"# NyaySetu - AI Legal Chatbot

An AI-powered legal information chatbot that provides accessible legal knowledge through text and voice interfaces. Built for the VOIS Hackathon 2025.

## Features

- 🤖 **RAG-based Legal Q&A** - Retrieval-augmented generation using ChromaDB and LangChain
- 🗣️ **Voice Input/Output** - Speech-to-text and text-to-speech support
- 📚 **Legal Knowledge Base** - IPC, CrPC, amendments, glossary, and legal documents
- 🎯 **Intent Classification** - Routes queries to appropriate handlers
- 📝 **Document Assistance** - Information about FIR, RTI, bail applications, legal notices
- 🚫 **Safe Boundaries** - Refuses procedural and legal advice queries

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: LangChain, OpenAI (via OpenRouter), ChromaDB, Sentence Transformers
- **Voice**: Whisper (speech-to-text), gTTS (text-to-speech)
- **Deployment**: Render (backend), Vercel (frontend)

## Project Structure

```
.
├── main.py                 # FastAPI web service (NEW)
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (API keys)
├── data/                  # Legal knowledge base
│   ├── normalized_ipc.json
│   ├── normalized_crpc.json
│   ├── normalized_amendments.json
│   └── normalized_glossary.json
└── scripts/               # Core chatbot logic
    ├── rag_pipeline.py    # Main query processing
    ├── retriever.py       # Vector DB retrieval
    ├── intent_router.py   # Query classification
    ├── context_builder.py # Context assembly
    ├── response_formatter.py
    ├── voice_input.py     # Speech-to-text
    ├── voice_output.py    # Text-to-speech
    └── chroma_day1/       # ChromaDB vector store
```

## Setup & Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key (via OpenRouter)

### Local Development

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd "Legal Chatbot"
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv legal_chatbot

   # Windows
   legal_chatbot\Scripts\activate

   # macOS/Linux
   source legal_chatbot/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openrouter_api_key
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   ```

5. **Run the API server**

   ```bash
   # Development (with auto-reload)
   uvicorn main:app --reload --port 8000

   # Production
   python main.py
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Health check: http://localhost:8000/health

## API Endpoints

### `GET /health`

Health check endpoint.

**Response:**

```json
{
  "status": "ok",
  "voice_input_available": true,
  "voice_output_available": true
}
```

### `POST /chat`

Text-based chat endpoint.

**Request:**

```json
{
  "session_id": "optional-uuid",
  "message": "What is IPC Section 420?"
}
```

**Response:**

```json
{
  "reply": "Legal Information\n\nIPC Section 420 deals with...",
  "session_id": "abc-123-def",
  "confidence": null
}
```

### `POST /chat/voice`

Voice-based chat endpoint (multipart/form-data).

**Request:**

- `audio`: Audio file (WAV, MP3, etc.)
- `session_id`: Optional session ID
- `return_audio`: Boolean (default: true)

**Response:**

```json
{
  "reply": "Legal information response...",
  "session_id": "abc-123",
  "audio_base64": "base64-encoded-audio-data",
  "transcribed_text": "What is FIR"
}
```

## Testing Existing Chatbot

Test the core chatbot functionality without the API:

```bash
cd scripts
python test_rag.py
```

## Deployment on Render

### Prerequisites

- Render account
- GitHub repository

### Steps

1. **Connect Repository**

   - Create new Web Service on Render
   - Connect your GitHub repository

2. **Configure Build Settings**

   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

3. **Environment Variables**
   Add in Render dashboard:

   ```
   OPENAI_API_KEY=your_openrouter_api_key
   OPENAI_BASE_URL=https://openrouter.ai/api/v1
   PORT=10000
   ```

4. **Deploy**
   - Render will auto-deploy on push to main branch
   - Vector DB (`chroma_day1/`) is included in deployment

### Important Notes

- **No Docker required** - Render uses native Python buildpack
- **Vector DB included** - ChromaDB folder is ~1MB, safe to include
- **Persistent storage** - Not required (vector DB is read-only)
- **Cold starts** - First request may be slow (~10-20s)

## Frontend Integration

The API is CORS-enabled for:

- `http://localhost:3000` (local Next.js dev)
- `https://*.vercel.app` (Vercel deployments)

### Example Next.js Integration

```typescript
// app/api/chat.ts
const response = await fetch("https://your-api.onrender.com/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: userQuery,
  }),
});

const data = await response.json();
console.log(data.reply);
```

## Architecture

```
User Query → FastAPI → Intent Classification → RAG Pipeline
                                              ↓
                                        Vector DB (ChromaDB)
                                              ↓
                                        Context Builder
                                              ↓
                                        LLM (Llama 3.1 8B)
                                              ↓
                                        Response Formatter
                                              ↓
                                        JSON Response
```

## Query Types Supported

✅ **Informational** - "What is IPC Section 420?"
✅ **Document Explanation** - "Explain FIR"
✅ **Document Selection** - "Which document for property dispute?"
✅ **Legal Definitions** - "What does bail mean?"

🚫 **Procedural** - "How to file FIR?"
🚫 **Advice** - "Will I win this case?"

## Limitations

- Provides **legal information only**, not legal advice
- No session persistence (sessions are in-memory only)
- Voice features require Whisper model (~140MB download on first use)
- Knowledge base limited to Indian law (IPC, CrPC)

## Troubleshooting

### "Voice input is not available"

- Whisper model failed to load
- Install ffmpeg: `choco install ffmpeg` (Windows) or `brew install ffmpeg` (macOS)

### "Chatbot temporarily unavailable"

- Check `.env` file exists with valid API key
- Verify OpenRouter API key is active
- Check ChromaDB vector store exists in `scripts/chroma_day1/`

### CORS errors from frontend

- Verify frontend URL matches allowed origins in `main.py`
- Check browser console for specific CORS error

## Development Notes

- **DO NOT modify** existing scripts/\* files unless fixing bugs
- **DO NOT move** ChromaDB folder
- **DO NOT commit** `.env` file
- All API logic is in `main.py` only

## License

MIT License - Built for VOIS Hackathon 2025

## Contributors

Team NyaySetu - VOIS Hackathon 2025
"
"# VOIS-NyaySetu" 
