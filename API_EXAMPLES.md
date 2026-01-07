# API Usage Examples

This document provides example API calls for frontend integration.

## Base URL

- **Local**: `http://localhost:8000`
- **Production**: `https://your-app.onrender.com`

---

## 1. Health Check

Check if the API is running and which features are available.

### Request

```bash
curl http://localhost:8000/health
```

### Response

```json
{
  "status": "ok",
  "voice_input_available": true,
  "voice_output_available": true
}
```

---

## 2. Text Chat

Send a text message and receive a legal information response.

### Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is IPC Section 420?"
  }'
```

### Response

```json
{
  "reply": "Legal Information\n\nIPC Section 420 deals with cheating and dishonestly inducing delivery of property...",
  "session_id": "abc-123-def-456",
  "confidence": null
}
```

### With Session ID

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "my-session-123",
    "message": "What is bail?"
  }'
```

---

## 3. Voice Chat

Send an audio file and receive text + audio response.

### Request

```bash
curl -X POST http://localhost:8000/chat/voice \
  -F "audio=@question.mp3" \
  -F "return_audio=true"
```

### Response

```json
{
  "reply": "Legal Information about...",
  "session_id": "abc-123",
  "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA...",
  "transcribed_text": "What is FIR",
  "audio_path": null
}
```

### Without Audio Response

```bash
curl -X POST http://localhost:8000/chat/voice \
  -F "audio=@question.mp3" \
  -F "return_audio=false"
```

---

## Frontend Integration Examples

### Next.js / TypeScript

```typescript
// lib/chatApi.ts

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatRequest {
  session_id?: string;
  message: string;
}

export interface ChatResponse {
  reply: string;
  session_id: string;
  confidence: number | null;
}

export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function sendVoiceMessage(
  audioFile: File,
  sessionId?: string
): Promise<any> {
  const formData = new FormData();
  formData.append("audio", audioFile);
  formData.append("return_audio", "true");

  if (sessionId) {
    formData.append("session_id", sessionId);
  }

  const response = await fetch(`${API_BASE_URL}/chat/voice`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
```

### React Component Example

```typescript
// components/ChatInterface.tsx

"use client";

import { useState } from "react";
import { sendMessage } from "@/lib/chatApi";

export default function ChatInterface() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [sessionId, setSessionId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await sendMessage({
        message,
        session_id: sessionId,
      });

      setResponse(result.reply);
      setSessionId(result.session_id);
      setMessage("");
    } catch (error) {
      console.error("Chat error:", error);
      setResponse("Sorry, something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask a legal question..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {response && (
        <div>
          <h3>Response:</h3>
          <pre>{response}</pre>
        </div>
      )}
    </div>
  );
}
```

---

## Error Handling

### Empty Message

```json
{
  "detail": "Message cannot be empty"
}
```

**Status**: 400

### Chatbot Unavailable

```json
{
  "error": "Chatbot temporarily unavailable"
}
```

**Status**: 500

### Voice Not Available

```json
{
  "detail": "Voice input is not available. Speech recognition is disabled."
}
```

**Status**: 503

### Audio Transcription Failed

```json
{
  "detail": "Could not transcribe audio. Please ensure the audio is clear and in a supported format."
}
```

**Status**: 400

---

## Testing the API

### Using curl

```bash
# Test health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is IPC Section 420?"}'
```

### Using Postman

1. Create a new POST request to `http://localhost:8000/chat`
2. Set Headers: `Content-Type: application/json`
3. Body (raw JSON):
   ```json
   {
     "message": "What is bail?"
   }
   ```
4. Send

### Using HTTPie

```bash
# Install: pip install httpie

# Text chat
http POST localhost:8000/chat message="What is FIR?"

# Voice chat
http -f POST localhost:8000/chat/voice audio@question.mp3 return_audio=true
```

---

## Interactive API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser!

---

## Environment Variables for Frontend

```env
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Production
NEXT_PUBLIC_API_URL=https://your-app.onrender.com
```

---

## Rate Limiting & Best Practices

1. **Session Management**: Store session_id in browser localStorage
2. **Error Handling**: Always handle 500 errors gracefully
3. **Loading States**: Show loading indicator during API calls
4. **Timeouts**: Set reasonable timeouts (30s recommended)
5. **Retry Logic**: Implement exponential backoff for failed requests

---

## Support

For issues or questions, contact the backend team.
