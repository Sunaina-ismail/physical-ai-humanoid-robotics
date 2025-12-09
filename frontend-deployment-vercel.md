# Frontend Deployment on Vercel

This document provides instructions for deploying the Physical AI & Humanoid Robotics textbook frontend on Vercel.

## Prerequisites

- Vercel account
- GitHub repository with the frontend code
- Backend API deployed and accessible (from Railway or other hosting)

## Environment Variables

For production deployment, you'll need to configure the backend API URL in the frontend. Currently, the frontend is hardcoded to connect to `http://localhost:8000/chat`, but for production you'll need to update the code to use an environment variable.

### Required Code Modification

The frontend code currently has the backend URL hardcoded. You must modify the Chatbot component to use an environment variable:

1. Update the API URL in `frontend/src/components/Chatbot/Chatbot.tsx` line 80:
   ```typescript
   const response = await fetch(process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000/chat', {
   ```

### Required Environment Variables in Vercel

After modifying the code, set this environment variable in your Vercel project:

```
REACT_APP_BACKEND_URL=https://your-backend-app.up.railway.app/chat
```

Replace `https://your-backend-app.up.railway.app/chat` with your actual deployed Railway backend URL.

### Additional Environment Variables

```
NODE_VERSION=20
```

## Deployment Steps

1. **Prepare the Frontend for Production API URL**
   - Update the hardcoded backend URL in `frontend/src/components/Chatbot/Chatbot.tsx`
   - Replace `'http://localhost:8000/chat'` with your deployed backend URL
   - Or implement environment variable support as shown above

2. **Connect Your Repository**
   - Go to Vercel dashboard
   - Click "Add New Project"
   - Import your GitHub repository containing the Physical AI & Humanoid Robotics frontend

3. **Configure the Project**
   - Root Directory: Select the `frontend` directory
   - Framework Preset: Docusaurus
   - Build Command: `yarn build` (or `npm run build`)
   - Output Directory: `build`
   - Install Command: `yarn install` (or `npm install`)

4. **Set Environment Variables**
   - In the "Environment Variables" section, add:
     - `NODE_VERSION`: `20` (or your preferred Node version)
     - `REACT_APP_BACKEND_URL`: Your deployed backend URL (e.g., `https://your-backend-app.up.railway.app/chat`)

5. **Deploy**
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