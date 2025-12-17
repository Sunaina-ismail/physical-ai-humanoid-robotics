# Backend URL Configuration Fix

## Problem
When deploying to Vercel, the chatbot was throwing this error:
```
ReferenceError: process is not defined
```

This happened because `process.env` is a Node.js feature that doesn't exist in the browser.

## Solution
We've updated the frontend to use Docusaurus's `customFields` feature, which properly handles environment variables at build time.

## Steps to Deploy

### 1. Set Environment Variable in Vercel

Go to your Vercel project settings → Environment Variables and add:

```
BACKEND_URL=https://your-backend-app.up.railway.app/chat
```

Replace `https://your-backend-app.up.railway.app/chat` with your actual Railway backend URL.

### 2. Redeploy Your Frontend

After setting the environment variable, trigger a new deployment in Vercel. The chatbot will now use your production backend URL.

### 3. For Local Development

Create a `.env` file in the `frontend/` directory:

```bash
cd frontend
cp .env.example .env
```

Edit `.env` and set:
```
BACKEND_URL=http://localhost:8000/chat
```

## Technical Details

### Changes Made

1. **`frontend/docusaurus.config.ts`**:
   - Added `customFields.backendUrl` that reads from `process.env.BACKEND_URL`

2. **`frontend/src/components/Chatbot/Chatbot.tsx`**:
   - Imported `useDocusaurusContext` hook
   - Updated backend URL retrieval to use `siteConfig.customFields.backendUrl`

3. **`frontend/.env.example`**:
   - Created example environment file for documentation

### How It Works

- At **build time**, Docusaurus reads the `BACKEND_URL` environment variable
- It injects this value into `customFields` in the site configuration
- The React component accesses it via the `useDocusaurusContext()` hook
- This approach is browser-safe and follows Docusaurus best practices

## Verification

After deployment, test the chatbot by:
1. Opening your deployed Vercel site
2. Clicking the chatbot button
3. Typing "hi" or any question
4. The chatbot should respond without errors

If you still see errors, check:
- Environment variable is set correctly in Vercel (no typos)
- Backend URL ends with `/chat` (e.g., `https://your-app.up.railway.app/chat`)
- Backend is running and accessible (test with curl or browser)
- Vercel build logs show the environment variable was detected
