"""
FastAPI backend for LLM-for-SE Agent
Provides REST API endpoints for interacting with the LangChain agent
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio
from typing import AsyncGenerator, Optional

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from single_agent.src.core.pipeline import build_single_agent_graph
from single_agent.src.utils.config import config

app = FastAPI(title="LLM-for-SE Agent API", version="1.0.0")

# CORS middleware to allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    show_node_info: bool = True


class TaskRequest(BaseModel):
    task_id: str
    signature: str
    docstring: str
    examples: list = []
    difficulty: Optional[str] = None
    show_node_info: bool = True


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "LLM-for-SE Agent API is running"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "model": config.model_name}


@app.post("/api/query")
async def process_query(request: QueryRequest):
    """
    Process a natural language query through the agent
    Returns the final result after all processing
    """
    try:
        graph = build_single_agent_graph()
        state = {'query': request.query}
        
        final_state = graph.invoke(state)
        
        return {
            "success": True,
            "code": final_state.get("code", ""),
            "task_id": final_state.get("task_id", ""),
            "signature": final_state.get("signature", ""),
            "docstring": final_state.get("docstring", ""),
            "quality_metrics": final_state.get("quality_metrics", {}),
            "refinement_count": final_state.get("refinement_count", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/task")
async def process_task(request: TaskRequest):
    """
    Process a structured task through the agent
    Returns the final result after all processing
    """
    try:
        graph = build_single_agent_graph()
        
        task_dict = {
            "task_id": request.task_id,
            "signature": request.signature,
            "docstring": request.docstring,
            "examples": request.examples,
            "show_node_info": request.show_node_info,
        }
        if request.difficulty:
            task_dict["difficulty"] = request.difficulty
            
        query = json.dumps(task_dict, ensure_ascii=False, indent=2)
        state = {'query': query}
        
        final_state = graph.invoke(state)
        
        return {
            "success": True,
            "code": final_state.get("code", ""),
            "task_id": final_state.get("task_id", ""),
            "signature": final_state.get("signature", ""),
            "docstring": final_state.get("docstring", ""),
            "quality_metrics": final_state.get("quality_metrics", {}),
            "refinement_count": final_state.get("refinement_count", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_stream_response(query: str, show_node_info: bool = True) -> AsyncGenerator[str, None]:
    """
    Generator that yields Server-Sent Events (SSE) during agent execution
    """
    try:
        # Send initial message
        yield f"data: {json.dumps({'type': 'start', 'message': 'Starting agent execution...'})}\n\n"
        await asyncio.sleep(0.1)
        
        # Build and invoke graph
        graph = build_single_agent_graph()
        state = {'query': query}
        
        # Stream preprocessing
        yield f"data: {json.dumps({'type': 'node', 'node': 'preprocessing', 'status': 'running'})}\n\n"
        await asyncio.sleep(0.1)
        
        # For real-time streaming, we'd need to modify the pipeline to yield intermediate results
        # For now, we'll invoke the full graph and simulate streaming of the result
        final_state = graph.invoke(state)
        
        # Stream each node completion
        nodes = ['preprocessing', 'analysis', 'planning', 'generation', 'review', 'refinement']
        for node in nodes:
            yield f"data: {json.dumps({'type': 'node', 'node': node, 'status': 'completed'})}\n\n"
            await asyncio.sleep(0.2)
        
        # Stream the analysis
        if show_node_info and final_state.get('analysis'):
            yield f"data: {json.dumps({'type': 'analysis', 'content': final_state['analysis']})}\n\n"
            await asyncio.sleep(0.1)
        
        # Stream the plan
        if show_node_info and final_state.get('plan'):
            yield f"data: {json.dumps({'type': 'plan', 'content': final_state['plan']})}\n\n"
            await asyncio.sleep(0.1)
        
        # Stream the code
        if final_state.get('code'):
            yield f"data: {json.dumps({'type': 'code', 'content': final_state['code']})}\n\n"
            await asyncio.sleep(0.1)
        
        # Stream quality metrics
        if final_state.get('quality_metrics'):
            yield f"data: {json.dumps({'type': 'metrics', 'content': final_state['quality_metrics']})}\n\n"
            await asyncio.sleep(0.1)
        
        # Send final complete message
        result = {
            'type': 'complete',
            'result': {
                'code': final_state.get('code', ''),
                'task_id': final_state.get('task_id', ''),
                'signature': final_state.get('signature', ''),
                'docstring': final_state.get('docstring', ''),
                'quality_metrics': final_state.get('quality_metrics', {}),
                'refinement_count': final_state.get('refinement_count', 0),
            }
        }
        yield f"data: {json.dumps(result)}\n\n"
        
    except Exception as e:
        error_data = {'type': 'error', 'message': str(e)}
        yield f"data: {json.dumps(error_data)}\n\n"


@app.post("/api/stream")
async def stream_query(request: QueryRequest):
    """
    Stream agent execution progress in real-time using Server-Sent Events (SSE)
    """
    return StreamingResponse(
        generate_stream_response(request.query, request.show_node_info),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
