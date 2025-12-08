import React, { type ReactNode } from 'react';
import { ThemeProvider } from '../components/HeroSection/ThemeContext';
import Chatbot from '../components/Chatbot/Chatbot';

export default function Root({ children }: { children: ReactNode }): ReactNode {
  return (
    <ThemeProvider>
      {children}
      <Chatbot />
    </ThemeProvider>
  );
}