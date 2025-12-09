import React, { useState, useEffect, useRef } from 'react';
import styles from './Chatbot.module.css';
import config from '../../config';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  citations?: Array<{
    chapter_number: number;
    chapter_title: string;
    section_title: string;
    snippet: string;
    similarity_score: number;
  }>;
}

const Chatbot: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection && selection.toString().trim().length > 0) {
        const selectedText = selection.toString().trim();
        if (selectedText.length > 0 && selectedText.length < 500) { // Reasonable length limit
          setSelectedText(selectedText);
        }
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, []);

  const sendMessage = async () => {
    if (!inputValue.trim() && !selectedText) return;

    const userMessage = inputValue || 'Explain this selected text';
    const userMessageObj: Message = {
      id: Date.now().toString(),
      text: userMessage,
      isUser: true,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessageObj]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the query with selected text if available
      const queryData = {
        query: userMessage,
        selected_text: selectedText || undefined,
      };

      // Call the backend API using configuration
      const response = await fetch(config.backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(queryData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessageObj: Message = {
        id: (Date.now() + 1).toString(),
        text: data.answer,
        isUser: false,
        timestamp: new Date(),
        citations: data.citations || [],
      };

      setMessages(prev => [...prev, botMessageObj]);
      setSelectedText(null); // Clear selected text after sending
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error processing your request. Please try again.",
        isUser: false,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <>
      {!isOpen ? (
        <button className={styles.floatingButton} onClick={toggleChat} aria-label="Open chatbot">
          <svg className={styles.robotIcon} viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H9L3 7V9C3 10.1 3.9 11 5 11V17C5 18.1 5.9 19 7 19H8V22H10V20H14V22H16V19H17C18.1 19 19 18.1 19 17V11C20.1 11 21 10.1 21 9ZM11 15H13V17H11V15ZM7 15H9V17H7V15ZM15 15H17V17H15V15ZM12 11C10.34 11 9 12.34 9 14V17H7V14C7 11.24 9.24 9 12 9S17 11.24 17 14V17H15V14C15 12.34 13.66 11 12 11Z" />
          </svg>
        </button>
      ) : (
        <div className={styles.chatbotContainer}>
          <div className={styles.chatHeader}>
            <h3 className={styles.chatTitle}>
              <svg className={styles.robotIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H9L3 7V9C3 10.1 3.9 11 5 11V17C5 18.1 5.9 19 7 19H8V22H10V20H14V22H16V19H17C18.1 19 19 18.1 19 17V11C20.1 11 21 10.1 21 9ZM11 15H13V17H11V15ZM7 15H9V17H7V15ZM15 15H17V17H15V15ZM12 11C10.34 11 9 12.34 9 14V17H7V14C7 11.24 9.24 9 12 9S17 11.24 17 14V17H15V14C15 12.34 13.66 11 12 11Z" />
              </svg>
              Physical AI Assistant
            </h3>
            <div className={styles.chatActions}>
              <button className={styles.chatClose} onClick={clearChat} aria-label="Clear chat">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                </svg>
              </button>
              <button className={styles.chatClose} onClick={toggleChat} aria-label="Close chat">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
                </svg>
              </button>
            </div>
          </div>

          <div className={styles.chatMessages}>
            {messages.length === 0 && (
              <div className={styles.botMessage}>
                Hello! I'm your Physical AI & Humanoid Robotics assistant.
                Select any text on the page to get explanations, or ask me any questions about the content.
              </div>
            )}

            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${message.isUser ? styles.userMessage : styles.botMessage}`}
              >
                {message.isUser ? (
                  <>
                    <div className={styles.queryText}>Query: {message.text}</div>
                  </>
                ) : (
                  <>
                    <div className={styles.responseText}>{message.text}</div>
                    {message.citations && message.citations.length > 0 && (
                      <div className={styles.citation}>
                        <div className={styles.citationTitle}>Sources:</div>
                        {message.citations.slice(0, 3).map((citation, index) => (
                          <div key={index} className={styles.citationItem}>
                            <div><strong>Ch {citation.chapter_number}: {citation.chapter_title}</strong>{citation.section_title && ` - ${citation.section_title}`}</div>
                            <div className={styles.citationSnippet}>{citation.snippet.substring(0, 100)}{citation.snippet.length > 100 ? '...' : ''}</div>
                            <div className={styles.citationScore}>Relevance: {(citation.similarity_score * 100).toFixed(0)}%</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
                <div className={styles.messageTimestamp}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.botMessage}`}>
                <div className={styles.loadingIndicator}>
                  <span>Processing your query...</span>
                  <div className={styles.loadingDots}>
                    <div className={styles.loadingDot}></div>
                    <div className={styles.loadingDot}></div>
                    <div className={styles.loadingDot}></div>
                  </div>
                </div>
              </div>
            )}

            {selectedText && (
              <div className={styles.selectedTextIndicator}>
                <svg className={styles.selectedTextIcon} width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z" />
                </svg>
                <div className={styles.selectedTextContent}>
                  <div className={styles.queryText}>Selected Text:</div>
                  "{selectedText}"
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputArea}>
            <textarea
              ref={textareaRef}
              className={styles.chatInput}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={selectedText ? "Ask about the selected text..." : "Ask about Physical AI & Robotics..."}
              rows={1}
            />
            <button
              className={styles.sendButton}
              onClick={sendMessage}
              disabled={isLoading || (!inputValue.trim() && !selectedText)}
              aria-label="Send message"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;