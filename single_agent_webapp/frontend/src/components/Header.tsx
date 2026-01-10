import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-sidebar-bg border-b border-gray-700 px-4 py-3">
      <div className="max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold">AI</span>
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">LLM for SE</h1>
            <p className="text-gray-400 text-xs">Code Generation Agent</p>
          </div>
        </div>
        <div className="text-gray-400 text-sm">
          Powered by LangChain
        </div>
      </div>
    </header>
  );
};

export default Header;
