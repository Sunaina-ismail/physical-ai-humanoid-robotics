// src/config.ts

interface AppConfig {
  backendUrl: string;
}

// The DefinePlugin will replace this entire string with your URL
const config: AppConfig = {
  backendUrl: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000/chat',
};

export default config;