# Physical AI & Humanoid Robotics Chatbot

## Overview
The chatbot is a teacher/assistant for students learning about Physical AI and Humanoid Robotics. It provides contextual explanations based on the textbook content and helps students understand concepts related to the subject.

## Features

### 1. Modern UI Design
- Robotic-themed SVG icon with gradient colors matching the site theme
- Fixed position at bottom-right corner
- Responsive design that works on all screen sizes
- Smooth animations and transitions

### 2. Text Selection Integration
- Automatically detects when user selects text on any page
- Shows the selected text in the chat interface
- Sends selected text to the backend with user queries
- Handles both selected text explanations and general questions

### 3. Educational Focus
- Contextualizes responses within Physical AI & Humanoid Robotics framework
- Provides citations linking to specific chapters and sections
- Explains concepts in relation to robotics applications
- Maintains anti-hallucination measures

### 4. Backend Integration
- Connects to the RAG agent backend API
- Sends queries with optional selected text
- Processes responses with citations and confidence scores
- Handles error states gracefully

## Technical Implementation

### Color Scheme
- Uses the same gradient theme as the main site (`#0f0c29`, `#302b63`, `#24243e`)
- Accent colors with gold/yellow (`#d4af37`) for highlights
- Green for user messages (`#2e8555` to `#33925d`)
- Appropriate contrast for readability

### Responsive Design
- Desktop: 380px wide, 500px tall chat window
- Mobile: Full width minus margins, height adjusted for mobile screens
- Proper z-index to appear above other content
- Touch-friendly controls for mobile devices

### API Integration
- Connects to `http://localhost:8000/chat` (backend API)
- Sends JSON with query and optional selected_text
- Processes responses with answer, citations, and confidence scores
- Shows loading indicators during processing

## Usage

### For Students
1. Select any text on the page to get an explanation
2. The selected text will appear in the chat interface
3. Ask questions about Physical AI & Robotics concepts
4. Review citations to understand source material
5. Use the chat as a study companion for the textbook

### For Developers
1. The chatbot is integrated into the Root component
2. Works on all pages automatically
3. Follows the same design system as the rest of the site
4. Properly handles API errors and loading states