import { useState, useRef, useEffect } from 'react';
import { Message, StreamEvent } from '@/types';
import { streamQuery } from '@/utils/api';
import MessageList from './MessageList';
import InputArea from './InputArea';
import Header from './Header';

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'system',
      content: 'Welcome! I\'m your AI code generation assistant. I can help you write Python functions. Just describe what you need, and I\'ll generate the code for you with analysis, planning, and quality metrics.',
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState<Message | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages((prev: Message[]) => [...prev, userMessage]);
    setIsLoading(true);

    // Create streaming message for assistant
    const assistantMessageId = (Date.now() + 1).toString();
    let streamingMessage: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '⚙️ Starting agent execution...',
      timestamp: new Date(),
      isStreaming: true,
    };

    setCurrentStreamingMessage(streamingMessage);

    try {
      await streamQuery(content.trim(), (event: StreamEvent) => {
        switch (event.type) {
          case 'start': {
            streamingMessage = {
              ...streamingMessage,
              content: event.message || 'Starting...',
            };
            setCurrentStreamingMessage({ ...streamingMessage });
            break;
          }

          case 'node': {
            if (event.status === 'running') {
              streamingMessage = {
                ...streamingMessage,
                content: `🔄 ${event.node}...`,
              };
            } else if (event.status === 'completed') {
              streamingMessage = {
                ...streamingMessage,
                content: `✅ ${event.node} completed`,
              };
            }
            setCurrentStreamingMessage({ ...streamingMessage });
            break;
          }

          case 'analysis': {
            streamingMessage = {
              ...streamingMessage,
              content: `⚙️ Processing analysis...`,
              analysis: String(event.content),
            };
            setCurrentStreamingMessage({ ...streamingMessage });
            break;
          }

          case 'plan': {
            streamingMessage = {
              ...streamingMessage,
              content: `⚙️ Creating solution plan...`,
              plan: String(event.content),
            };
            setCurrentStreamingMessage({ ...streamingMessage });
            break;
          }

          case 'code': {
            streamingMessage = {
              ...streamingMessage,
              content: `✅ Code generated successfully`,
              code: event.content as string,
            };
            setCurrentStreamingMessage({ ...streamingMessage });
            break;
          }

          case 'metrics': {
            streamingMessage = {
              ...streamingMessage,
              metrics: event.content as any,
            };
            setCurrentStreamingMessage({ ...streamingMessage });
            break;
          }

          case 'complete': {
            const finalMessage: Message = {
              ...streamingMessage,
              content: `✅ Task completed`,
              code: event.result?.code,
              metrics: event.result?.quality_metrics,
              isStreaming: false,
            };
            setMessages((prev: Message[]) => [...prev, finalMessage]);
            setCurrentStreamingMessage(null);
            break;
          }

          case 'error': {
            const errorMessage: Message = {
              ...streamingMessage,
              content: `❌ Error: ${event.message}`,
              isStreaming: false,
            };
            setMessages((prev: Message[]) => [...prev, errorMessage]);
            setCurrentStreamingMessage(null);
            break;
          }
        }
      });
    } catch (error) {
      const errorMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: `❌ Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
        timestamp: new Date(),
      };
      setMessages((prev: Message[]) => [...prev, errorMessage]);
      setCurrentStreamingMessage(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen">
      <Header />
      <div className="flex-1 overflow-hidden">
        <MessageList
          messages={messages}
          currentStreamingMessage={currentStreamingMessage}
          messagesEndRef={messagesEndRef}
        />
      </div>
      <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}
