import { StreamEvent, AgentResponse } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const sendQuery = async (query: string, showNodeInfo: boolean = true): Promise<AgentResponse> => {
  const response = await fetch(`${API_URL}/api/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, show_node_info: showNodeInfo }),
  });

  if (!response.ok) {
    throw new Error('Failed to process query');
  }

  return response.json();
};

export const streamQuery = async (
  query: string,
  onEvent: (event: StreamEvent) => void,
  showNodeInfo: boolean = true
): Promise<void> => {
  const response = await fetch(`${API_URL}/api/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, show_node_info: showNodeInfo }),
  });

  if (!response.ok) {
    throw new Error('Failed to start streaming');
  }

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  if (!reader) {
    throw new Error('Response body is not readable');
  }

  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6);
          try {
            const event: StreamEvent = JSON.parse(data);
            onEvent(event);
          } catch (e) {
            console.error('Failed to parse SSE data:', e);
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
};

export const checkHealth = async (): Promise<{ status: string; model: string }> => {
  const response = await fetch(`${API_URL}/health`);
  
  if (!response.ok) {
    throw new Error('Health check failed');
  }

  return response.json();
};
