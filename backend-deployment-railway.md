# Backend Deployment on Railway

This document provides instructions for deploying the Physical AI & Humanoid Robotics RAG chatbot backend on Railway.

## Prerequisites

- Railway account
- Gemini API key
- Qdrant Cloud account and API key
- GitHub repository with the backend code

## Environment Variables

Set the following environment variables in your Railway project:

### Required Environment Variables

```
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=rag-textbook
```

### Optional Environment Variables

```
SIMILARITY_THRESHOLD=0.7
TOP_K_RESULTS=5
ENVIRONMENT=production
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
LOG_LEVEL=INFO
MAX_QUERY_LENGTH=2000
```

## CORS Configuration (Optional)

If you want to restrict which origins can access your API, you may want to add CORS configuration. Currently, the backend allows all origins (`allow_origins=["*"]`), but for production you might want to restrict this to your Vercel frontend URL:

```
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

Note: This would require modifying the CORS middleware in `app/main.py` to use the environment variable instead of wildcard.

## Deployment Steps

1. **Connect Your Repository**
   - Go to Railway dashboard
   - Click "New Project"
   - Select "GitHub" and connect your repository
   - Choose the repository containing the Physical AI & Humanoid Robotics backend

2. **Configure the Project**
   - Select the `backend` directory as your project root
   - Railway should automatically detect this as a Python project

3. **Set Environment Variables**
   - Navigate to the "Variables" tab in your Railway project
   - Add all required environment variables listed above
   - Make sure to use secure values for API keys

4. **Configure Build and Start Commands**
   - Railway will automatically detect the Python dependencies from `requirements.txt`
   - The start command should be: `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`

5. **Deploy**
   - Click "Deploy" to build and deploy your application
   - Monitor the build logs for any errors

## Build Configuration

- **Build Command**: Railway will automatically run `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`
- **Runtime**: Python 3.10+ (as specified in the requirements)

## Post-Deployment Setup

After your backend is deployed, you'll need to initialize the Qdrant vector database with your textbook content:

1. Access your deployed backend's `/docs` endpoint to use the interactive API documentation
2. Run the content ingestion script to populate your Qdrant collection with textbook data
3. Test the `/health` endpoint to ensure everything is working properly

## Health Check

Your deployed backend will have a health check endpoint at:
`https://your-project-slug.up.railway.app/health`

## API Documentation

Interactive API documentation is available at:
`https://your-project-slug.up.railway.app/docs`

## Troubleshooting

- **Environment Variables Missing**: Ensure all required environment variables are set
- **Qdrant Connection Issues**: Verify your Qdrant URL, API key, and collection name
- **Gemini API Issues**: Confirm your Gemini API key is valid and has proper permissions
- **Port Configuration**: Railway automatically provides a PORT environment variable

## Scaling

- Adjust instance size based on expected load
- Monitor your Qdrant Cloud usage for vector database operations
- Consider connection pooling for high-traffic scenarios