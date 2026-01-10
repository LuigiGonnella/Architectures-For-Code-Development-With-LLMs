import React from 'react';
import { Message } from '@/types';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import { AnalysisSection, PlanSection } from './AgentSections';

interface MessageItemProps {
  message: Message;
  analysis?: string;
  plan?: string;
}

const MessageItem: React.FC<MessageItemProps> = ({ message, analysis, plan }) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  // Don't show analysis/plan text in the message content
  const cleanContent = message.content
    .replace(/📊\s*\*\*Analysis:\*\*[\s\S]*?(?=📝|\💻|$)/g, '')
    .replace(/📝\s*\*\*Plan:\*\*[\s\S]*?(?=💻|$)/g, '')
    .replace(/💻\s*\*\*Generated Code:\*\*[\s\S]*?$/g, '')
    .trim();

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} ${
        isSystem ? 'justify-center' : ''
      }`}
    >
      <div
        className={`max-w-[85%] rounded-lg p-4 ${
          isUser
            ? 'bg-blue-600 text-white'
            : isSystem
            ? 'bg-gray-700 text-gray-300 text-center text-sm'
            : 'bg-input-bg text-gray-100'
        }`}
      >
        {!isUser && !isSystem && (
          <div className="flex items-center mb-2">
            <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mr-2">
              <span className="text-white text-xs font-bold">AI</span>
            </div>
            <span className="text-gray-400 text-xs">
              {message.timestamp.toLocaleTimeString()}
            </span>
          </div>
        )}

        {/* Show user message */}
        {isUser && (
          <div className="text-white">
            {message.content}
          </div>
        )}

        {/* Show analysis section if available */}
        {analysis && !isUser && !isSystem && (
          <div className="mb-4">
            <AnalysisSection content={analysis} />
          </div>
        )}

        {/* Show plan section if available */}
        {plan && !isUser && !isSystem && (
          <div className="mb-4">
            <PlanSection content={plan} />
          </div>
        )}

        {/* Show status messages */}
        {cleanContent && !isUser && (
          <div className="text-sm text-gray-300 mb-2 font-normal">
            {cleanContent}
          </div>
        )}

        {message.code && (
          <div className="mt-4">
            <div className="bg-slate-900 rounded-xl overflow-hidden border-2 border-emerald-600/50 shadow-xl">
              <div className="bg-gradient-to-r from-emerald-900/50 to-teal-900/50 px-5 py-4 flex items-center justify-between border-b border-emerald-700/50">
                <div className="flex items-center gap-3">
                  <span className="text-emerald-400 text-xl">💻</span>
                  <span className="text-lg font-bold text-emerald-300">GENERATED CODE</span>
                </div>
                <button
                  onClick={() => navigator.clipboard.writeText(message.code || '')}
                  className="text-sm bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-lg transition-all font-bold shadow-lg hover:shadow-emerald-500/50"
                >
                  Copy
                </button>
              </div>
              <SyntaxHighlighter
                language="python"
                style={vscDarkPlus as any}
                customStyle={{
                  margin: 0,
                  borderRadius: 0,
                  fontSize: '14px',
                }}
              >
                {message.code}
              </SyntaxHighlighter>
            </div>
          </div>
        )}

        {message.metrics && Object.keys(message.metrics).length > 0 && (
          <div className="mt-4 bg-gradient-to-br from-indigo-900/30 to-purple-900/30 rounded-xl p-5 border-2 border-indigo-600/50 shadow-lg">
            <h4 className="text-lg font-bold text-indigo-300 mb-4 flex items-center gap-2">
              <span>📊</span>
              <span>QUALITY METRICS</span>
            </h4>
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(message.metrics).map(([key, value]) => (
                <div key={key} className="bg-gradient-to-br from-slate-800/60 to-slate-900/60 rounded-lg p-4 border border-indigo-700/40 shadow-md">
                  <div className="text-indigo-300 text-xs mb-2 font-bold uppercase tracking-wider">
                    {key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                  </div>
                  <div className="text-slate-50 font-mono font-bold text-lg">
                    {typeof value === 'number' ? value.toFixed(2) : value}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {message.isStreaming && (
          <div className="mt-2 flex items-center space-x-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-75"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-150"></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageItem;
