export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  code?: string;
  metrics?: QualityMetrics;
  analysis?: string;
  plan?: string;
  timestamp: Date;
  isStreaming?: boolean;
}

export interface QualityMetrics {
  lines_of_code?: number;
  cyclomatic_complexity?: number;
  maintainability_index?: number;
  [key: string]: any;
}

export interface AgentResponse {
  success: boolean;
  code: string;
  task_id: string;
  signature: string;
  docstring: string;
  quality_metrics: QualityMetrics;
  refinement_count: number;
}

export interface StreamEvent {
  type: 'start' | 'node' | 'analysis' | 'plan' | 'code' | 'metrics' | 'complete' | 'error';
  node?: string;
  status?: string;
  content?: string | QualityMetrics;
  result?: AgentResponse;
  message?: string;
}
