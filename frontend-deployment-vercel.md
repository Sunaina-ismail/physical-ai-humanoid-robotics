# Frontend Deployment on Vercel

This document provides instructions for deploying the Physical AI & Humanoid Robotics textbook frontend on Vercel.

## Prerequisites

- Vercel account
- GitHub repository with the frontend code
- Backend API deployed and accessible (from Railway or other hosting)

## Environment Variables

For production deployment, you need to configure the backend API URL in Vercel.

### Required Environment Variables in Vercel

Set this environment variable in your Vercel project settings:

```
BACKEND_URL=https://your-backend-app.up.railway.app/chat
```

Replace `https://your-backend-app.up.railway.app/chat` with your actual deployed Railway backend URL.

**Note**: The frontend uses Docusaurus's `customFields` to access this environment variable at build time. Make sure to set this in Vercel's environment variables section before deploying.

### Additional Environment Variables

```
NODE_VERSION=20
```

## Deployment Steps

1. **Connect Your Repository**
   - Go to Vercel dashboard
   - Click "Add New Project"
   - Import your GitHub repository containing the Physical AI & Humanoid Robotics frontend

2. **Configure the Project**
   - Root Directory: Select the `frontend` directory
   - Framework Preset: Docusaurus
   - Build Command: `yarn build` (or `npm run build`)
   - Output Directory: `build`
   - Install Command: `yarn install` (or `npm install`)

3. **Set Environment Variables**
   - In the "Environment Variables" section, add:
     - `NODE_VERSION`: `20` (or your preferred Node version)
     - `BACKEND_URL`: Your deployed backend URL (e.g., `https://your-backend-app.up.railway.app/chat`)

4. **Deploy**
   - Click "Deploy" to build and deploy your application
   - Vercel will automatically build your Docusaurus site

## Build Configuration

- **Build Command**: `yarn build` (or `npm run build`)
- **Output Directory**: `build` (automatically detected by Docusaurus)
- **Install Command**: `yarn install`
- **Framework**: Docusaurus
- **Runtime**: Node.js 20+

## Post-Deployment Setup

1. **Verify the Deployment**
   - Access your deployed frontend using the provided Vercel URL
   - Test the chatbot functionality to ensure it connects to your backend

2. **Custom Domain (Optional)**
   - Go to your project settings in Vercel
   - Add your custom domain in the "Domains" section
   - Update DNS settings as instructed by Vercel

3. **Environment Configuration**
   - Ensure the backend API URL is correctly configured
   - Test all interactive components to verify they work in production

## Configuration Files

The deployment will use the following configuration files from your repository:
- `docusaurus.config.ts` - Main Docusaurus configuration
- `package.json` - Dependencies and build scripts
- `tsconfig.json` - TypeScript configuration

## Troubleshooting

- **Build Failures**: Ensure you're using Node.js version 20+ and have all dependencies in package.json
- **Chatbot Not Working**: Verify that the backend API URL is correctly configured
- **Static Assets**: Ensure all images and static files are properly referenced
- **Internationalization**: Verify that both English and Urdu content are properly deployed

## Scaling and Performance

- Vercel automatically handles scaling for static content
- Static assets are served from CDN for optimal performance
- Monitor backend API usage as it handles the chatbot functionality
- Consider using Vercel's edge network for improved global performance

## Environment-Specific Considerations

- **Development**: Uses `http://localhost:8000/chat` for backend API
- **Production**: Should use your deployed backend URL (e.g., `https://your-backend.up.railway.app/chat`)
- **Preview Deployments**: Each pull request will get its own preview URL