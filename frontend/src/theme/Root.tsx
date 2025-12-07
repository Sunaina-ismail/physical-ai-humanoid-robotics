import React, { type ReactNode } from 'react';
import { ThemeProvider } from '../components/HeroSection/ThemeContext';

export default function Root({ children }: { children: ReactNode }): ReactNode {
  return <ThemeProvider>{children}</ThemeProvider>;
}