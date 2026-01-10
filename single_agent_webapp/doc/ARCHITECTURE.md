# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
│                     (http://localhost:3000)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ HTTP/SSE
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Frontend                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Components:                                         │    │
│  │  • ChatInterface - Main chat UI                     │    │
│  │  • MessageList - Display messages                   │    │
│  │  • MessageItem - Individual message w/ code         │    │
│  │  • InputArea - User input with textarea             │    │
│  │  • Header - App header                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  API Client (utils/api.ts):                         │    │
│  │  • streamQuery() - SSE streaming                    │    │
│  │  • sendQuery() - Non-streaming requests             │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ REST API / SSE
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│                  (http://localhost:8000)                     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Endpoints:                                          │    │
│  │  • POST /api/query      - Process query (sync)      │    │
│  │  • POST /api/stream     - Stream query (SSE)        │    │
│  │  • POST /api/task       - Process structured task   │    │
│  │  • GET  /health         - Health check              │    │
│  └─────────────────────────────────────────────────────┘    │
│                           │                                   │
│                           ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Agent Integration:                                  │    │
│  │  • build_single_agent_graph()                       │    │
│  │  • generate_stream_response()                       │    │
│  └─────────────────────────────────────────────────────┘    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ Invokes
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   LangChain Agent Pipeline                   │
│                (single_agent/src/core/pipeline.py)           │
│                                                               │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │  Preprocessing   │───▶│    Analysis      │               │
│  └──────────────────┘    └──────────────────┘               │
│           │                       │                          │
│           ▼                       ▼                          │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │    Planning      │───▶│   Generation     │               │
│  └──────────────────┘    └──────────────────┘               │
│           │                       │                          │
│           ▼                       ▼                          │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │     Review       │───▶│   Refinement     │               │
│  └──────────────────┘    └──────────────────┘               │
│                                                               │
│  Each node:                                                  │
│  • Receives AgentState                                       │
│  • Calls LLM (via call_llm)                                 │
│  • Updates state                                             │
│  • Returns updated state                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ API Calls
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      LLM Provider                            │
│                (OpenAI GPT-4 / Other)                        │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Query Processing Flow

1. **User Input**
   - User types query in browser
   - Example: "Write a function that counts vowels"

2. **Frontend Processing**
   - ChatInterface captures input
   - Creates user message
   - Calls `streamQuery()` from API client

3. **Backend Reception**
   - FastAPI receives POST to `/api/stream`
   - Extracts query from request body
   - Initiates `generate_stream_response()`

4. **Agent Execution**
   - Builds LangGraph pipeline
   - Invokes graph with query
   - Graph executes nodes sequentially:
     - **Preprocessing**: Converts NL query → structured task
     - **Analysis**: Analyzes requirements
     - **Planning**: Creates implementation plan
     - **Generation**: Generates code
     - **Review**: Executes and reviews code
     - **Refinement**: Refines code if needed

5. **Streaming Response**
   - Backend streams SSE events as agent progresses
   - Events include: node status, analysis, plan, code, metrics

6. **Frontend Updates**
   - ChatInterface receives SSE events
   - Updates streaming message in real-time
   - Displays code with syntax highlighting
   - Shows quality metrics

7. **Completion**
   - Final message added to chat history
   - User can copy code or submit new query

## State Management

### AgentState (Backend)
```python
{
  "task_id": str,           # Task identifier
  "signature": str,         # Function signature
  "docstring": str,         # Function description
  "examples": list,         # Input/output examples
  "analysis": str,          # Task analysis
  "plan": str,              # Implementation plan
  "code": str,              # Generated code
  "review": str,            # Review feedback
  "exec_result": dict,      # Execution results
  "quality_metrics": dict,  # Code quality metrics
  "refinement_count": int,  # Number of refinements
  "model": str,             # LLM model name
  "show_node_info": bool    # Show detailed info
}
```

### Message State (Frontend)
```typescript
{
  id: string,              // Unique message ID
  role: 'user' | 'assistant' | 'system',
  content: string,         // Message text (Markdown)
  code?: string,           // Generated code
  metrics?: object,        // Quality metrics
  timestamp: Date,         // Message timestamp
  isStreaming?: boolean    // Currently streaming
}
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **LangChain**: Agent orchestration
- **LangGraph**: State management for agent
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

### Frontend
- **Next.js 14**: React framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS
- **React Markdown**: Markdown rendering
- **React Syntax Highlighter**: Code highlighting

### Communication
- **REST API**: Standard HTTP requests
- **Server-Sent Events (SSE)**: Real-time streaming
- **CORS**: Cross-origin resource sharing

## Deployment Options

### Option 1: Local Development
- Run backend with `python main.py`
- Run frontend with `npm run dev`
- Best for development and testing

### Option 2: Docker Compose
- Single command: `docker-compose up`
- Isolated containers
- Easy to deploy
- Best for production-like environment

### Option 3: Separate Deployment
- Deploy backend to cloud (AWS, GCP, Azure)
- Deploy frontend to Vercel, Netlify
- Scale independently
- Best for production
