"""
FastAPI Web Service for AI Legal Chatbot
Exposes existing chatbot functionality via HTTP API
"""

import os
import sys
import uuid
import base64
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Add scripts directory to Python path
SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import existing chatbot components
from rag_pipeline import answer_query
from voice_input import VoiceInputProcessor
from voice_output import VoiceOutputProcessor

# Global instances (initialized at startup)
voice_input_processor = None
voice_output_processor = None


# =============================================================================
# REQUEST / RESPONSE MODELS
# =============================================================================

class ChatRequest(BaseModel):
    """Text chat request"""
    session_id: Optional[str] = None
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "optional-uuid",
                "message": "What is IPC Section 420?"
            }
        }


class ChatResponse(BaseModel):
    """Text chat response"""
    reply: str
    session_id: str
    confidence: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "reply": "IPC Section 420 deals with cheating and dishonesty...",
                "session_id": "abc-123",
                "confidence": None
            }
        }


class VoiceChatResponse(BaseModel):
    """Voice chat response"""
    reply: str
    session_id: str
    audio_base64: Optional[str] = None
    audio_path: Optional[str] = None
    transcribed_text: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "reply": "Legal information about...",
                "session_id": "abc-123",
                "audio_base64": "base64-encoded-audio-data",
                "transcribed_text": "What is FIR"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    voice_input_available: bool
    voice_output_available: bool


# =============================================================================
# STARTUP / SHUTDOWN LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize heavy components once at startup.
    This avoids reloading models and vector DB on every request.
    """
    global voice_input_processor, voice_output_processor

    print("=" * 80)
    print("🚀 Initializing Legal Chatbot API...")
    print("=" * 80)

    # Initialize voice processors
    try:
        voice_input_processor = VoiceInputProcessor(model_size="base")
        print("✅ Voice input processor initialized")
    except Exception as e:
        print(f"⚠️  Voice input initialization failed: {e}")
        voice_input_processor = None

    try:
        voice_output_dir = SCRIPTS_DIR / "voice_outputs"
        voice_output_processor = VoiceOutputProcessor(output_dir=str(voice_output_dir))
        print("✅ Voice output processor initialized")
    except Exception as e:
        print(f"⚠️  Voice output initialization failed: {e}")
        voice_output_processor = None

    # Test RAG pipeline initialization (this loads the vector DB)
    try:
        test_response = answer_query("test initialization")
        print("✅ RAG pipeline initialized successfully")
    except Exception as e:
        print(f"⚠️  RAG pipeline test failed: {e}")

    print("=" * 80)
    print("✅ Legal Chatbot API ready to serve requests")
    print("=" * 80)

    yield

    # Cleanup on shutdown
    print("🛑 Shutting down Legal Chatbot API...")


# =============================================================================
# FASTAPI APP INITIALIZATION
# =============================================================================

app = FastAPI(
    title="AI Legal Chatbot API",
    description="HTTP API for the NyaySetu Legal Chatbot - provides legal information through text and voice interfaces",
    version="1.0.0",
    lifespan=lifespan
)

# =============================================================================
# CORS CONFIGURATION
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "https://vercel.app"
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())


def safe_chatbot_call(user_message: str) -> str:
    """
    Safely call the chatbot with error handling.
    Returns error message on failure.
    """
    try:
        return answer_query(user_message)
    except Exception as e:
        print(f"❌ Chatbot error: {str(e)}")
        return "I apologize, but I'm temporarily unable to process your request. Please try again."


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint - API information"""
    return {
        "service": "AI Legal Chatbot API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "text_chat": "/chat",
            "voice_chat": "/chat/voice"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns service status and feature availability.
    """
    return HealthResponse(
        status="ok",
        voice_input_available=voice_input_processor is not None and voice_input_processor.model is not None,
        voice_output_available=voice_output_processor is not None
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Text-based chat endpoint.
    
    Accepts a text message and returns a legal information response.
    Session IDs are generated if not provided but are not persisted.
    """
    # Generate session ID if not provided
    session_id = request.session_id or generate_session_id()

    # Validate message
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # Get chatbot response
    try:
        reply = safe_chatbot_call(request.message.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Chatbot temporarily unavailable")

    return ChatResponse(
        reply=reply,
        session_id=session_id,
        confidence=None  # Confidence scoring not implemented in current chatbot
    )


@app.post("/chat/voice", response_model=VoiceChatResponse, tags=["Chat"])
async def chat_voice(
    audio: UploadFile = File(..., description="Audio file (WAV, MP3, etc.)"),
    session_id: Optional[str] = Form(None),
    return_audio: bool = Form(True, description="Whether to return audio response")
):
    """
    Voice-based chat endpoint.
    
    Accepts an audio file, transcribes it to text, processes through chatbot,
    and optionally returns audio response.
    
    Returns both text and optional audio (base64-encoded).
    """
    # Generate session ID if not provided
    session_id = session_id or generate_session_id()

    # Check if voice input is available
    if not voice_input_processor or not voice_input_processor.model:
        raise HTTPException(
            status_code=503,
            detail="Voice input is not available. Speech recognition is disabled."
        )

    # Save uploaded file temporarily
    temp_dir = Path(__file__).parent / "temp_audio"
    temp_dir.mkdir(exist_ok=True)
    temp_audio_path = temp_dir / f"{uuid.uuid4().hex}_{audio.filename}"

    try:
        # Save uploaded file
        with open(temp_audio_path, "wb") as f:
            content = await audio.read()
            f.write(content)

        # Transcribe audio to text
        transcribed_text = voice_input_processor.transcribe(str(temp_audio_path))

        if not transcribed_text:
            raise HTTPException(
                status_code=400,
                detail="Could not transcribe audio. Please ensure the audio is clear and in a supported format."
            )

        # Get chatbot response
        try:
            reply = safe_chatbot_call(transcribed_text)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Chatbot temporarily unavailable")

        # Generate audio response if requested
        audio_base64 = None
        audio_path = None

        if return_audio and voice_output_processor:
            try:
                audio_path = voice_output_processor.speak(reply)
                if audio_path and os.path.exists(audio_path):
                    # Read audio file and encode as base64
                    with open(audio_path, "rb") as audio_file:
                        audio_data = audio_file.read()
                        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            except Exception as e:
                print(f"⚠️  Voice output generation failed: {e}")

        return VoiceChatResponse(
            reply=reply,
            session_id=session_id,
            audio_base64=audio_base64,
            audio_path=None,  # Don't expose server paths
            transcribed_text=transcribed_text
        )

    finally:
        # Cleanup temporary audio file
        if temp_audio_path.exists():
            try:
                temp_audio_path.unlink()
            except:
                pass


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Chatbot temporarily unavailable"}
    )


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Use PORT environment variable for Render compatibility
    port = int(os.environ.get("PORT", 10000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Disable in production
    )
