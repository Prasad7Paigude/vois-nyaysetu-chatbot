"""
FastAPI Web Service for AI Legal Chatbot
Exposes existing chatbot functionality via HTTP API (Text-only)
"""

import os
import sys
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Add scripts directory to Python path
SCRIPTS_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Lazy import pattern - heavy components loaded only on first use
# This reduces startup memory footprint significantly


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


class HealthResponse(BaseModel):
    """Health check response"""
    status: str


# =============================================================================
# STARTUP / SHUTDOWN LIFECYCLE
# =============================================================================

# No startup initialization - all components loaded lazily on first request
# This minimizes memory footprint and avoids loading heavy models at startup


# =============================================================================
# FASTAPI APP INITIALIZATION
# =============================================================================

app = FastAPI(
    title="AI Legal Chatbot API",
    description="HTTP API for the NyaySetu Legal Chatbot - provides legal information through text interface",
    version="1.0.0"
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
    Uses lazy import to avoid loading heavy dependencies at startup.
    Returns error message on failure.
    """
    try:
        # Lazy import - only load when actually needed
        from rag_pipeline import answer_query
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
            "text_chat": "/chat"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    Returns service status.
    """
    return HealthResponse(status="ok")


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
    
    print("🚀 Starting AI Legal Chatbot API (Text-only, Memory Optimized)")
    
    # Use PORT environment variable for Render compatibility
    port = int(os.environ.get("PORT", 10000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
