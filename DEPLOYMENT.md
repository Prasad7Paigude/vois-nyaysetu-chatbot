# Deployment Checklist

Complete this checklist before deploying to Render.

## Pre-Deployment Setup

### 1. Install New Dependencies

```bash
# Activate virtual environment
legal_chatbot\Scripts\activate  # Windows
# source legal_chatbot/bin/activate  # macOS/Linux

# Install FastAPI and dependencies
pip install fastapi==0.115.6 python-multipart==0.0.20

# Verify installation
pip list | findstr fastapi
```

### 2. Test API Locally

```bash
# Run integration test
python test_api.py

# Should output:
# ✅ rag_pipeline imported successfully
# ✅ voice_input imported successfully
# ✅ voice_output imported successfully
# ✅ Chatbot responded successfully
```

### 3. Start API Server

```bash
# Option 1: Development mode
uvicorn main:app --reload --port 8000

# Option 2: Production mode
python main.py
```

### 4. Verify Endpoints

Open browser and test:

- http://localhost:8000 - Root endpoint
- http://localhost:8000/health - Health check
- http://localhost:8000/docs - Interactive API docs

### 5. Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Text chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is IPC Section 420?\"}"
```

## Render Deployment

### 1. Create GitHub Repository (if not exists)

```bash
git init
git add .
git commit -m "Add FastAPI wrapper for legal chatbot"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Create Render Web Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `nyaysetu-legal-chatbot-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`

### 3. Set Environment Variables

In Render dashboard, add:

```
OPENAI_API_KEY=<your-openrouter-key>
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

### 4. Deploy

- Click "Create Web Service"
- Wait for deployment (~5-10 minutes first time)
- Watch logs for any errors

### 5. Verify Deployment

```bash
# Replace with your Render URL
curl https://nyaysetu-legal-chatbot-api.onrender.com/health

# Expected response:
# {"status":"ok","voice_input_available":true,"voice_output_available":true}
```

## Frontend Integration

### Update Frontend Environment Variables

```env
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=https://nyaysetu-legal-chatbot-api.onrender.com
```

### Update CORS if Needed

If your Vercel domain is different from `*.vercel.app`, update [main.py](main.py) line ~160:

```python
allow_origins=[
    "http://localhost:3000",
    "https://your-custom-domain.com",  # Add your domain
    "https://*.vercel.app",
],
```

## Post-Deployment Verification

### 1. Check All Endpoints

- [ ] GET /health returns 200
- [ ] POST /chat returns valid response
- [ ] POST /chat/voice returns 503 (if Whisper not working) or valid response
- [ ] GET /docs shows API documentation

### 2. Test from Frontend

- [ ] Frontend can call /chat successfully
- [ ] Error handling works correctly
- [ ] CORS headers are present

### 3. Monitor Performance

- [ ] Check Render dashboard for memory usage
- [ ] Monitor response times (should be <5s)
- [ ] Check for any error logs

## Troubleshooting

### "Chatbot temporarily unavailable"

**Cause**: API key issue or vector DB not loaded

**Fix**:

1. Check environment variables in Render dashboard
2. Verify chroma_day1/ folder exists in deployment
3. Check Render logs for specific error

### CORS Errors

**Cause**: Frontend domain not in allowed origins

**Fix**: Update `allow_origins` in [main.py](main.py)

### "Voice input is not available"

**Cause**: Whisper model failed to load (expected on Render free tier)

**Fix**: This is expected. Voice features may not work on limited memory environments. Use text chat only.

### Cold Starts (slow first request)

**Cause**: Render spins down inactive services

**Fix**:

- Upgrade to paid plan for always-on
- Implement keep-alive ping from frontend
- Accept 10-20s first request time

## Maintenance

### Updating the API

```bash
# Make changes
git add .
git commit -m "Update API"
git push

# Render auto-deploys on push
```

### Monitoring

- Check Render dashboard regularly
- Monitor API logs for errors
- Set up uptime monitoring (e.g., UptimeRobot)

## Rollback Plan

If deployment fails:

1. Check Render logs for errors
2. Roll back to previous commit:
   ```bash
   git revert HEAD
   git push
   ```
3. Fix issues locally and redeploy

## Success Criteria

- [ ] API deployed successfully on Render
- [ ] /health endpoint returns 200
- [ ] /chat endpoint returns valid legal responses
- [ ] Frontend can communicate with backend
- [ ] No CORS errors
- [ ] Response time <5 seconds
- [ ] All existing chatbot tests still pass

---

**Need help?** Check API_EXAMPLES.md or README.md
