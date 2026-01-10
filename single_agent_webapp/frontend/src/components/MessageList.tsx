import React from 'react';
import { Message } from '@/types';
import MessageItem from './MessageItem';

interface MessageListProps {
  messages: Message[];
  currentStreamingMessage: Message | null;
  messagesEndRef: React.RefObject<HTMLDivElement>;
}

const MessageList: React.FC<MessageListProps> = ({
  messages,
  currentStreamingMessage,
  messagesEndRef,
}) => {
  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {messages.map((message) => (
          <MessageItem 
            key={message.id} 
            message={message}
            analysis={message.analysis}
            plan={message.plan}
          />
        ))}
        {currentStreamingMessage && (
          <MessageItem 
            message={currentStreamingMessage}
            analysis={currentStreamingMessage.analysis}
            plan={currentStreamingMessage.plan}
          />
        )}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default MessageList;
