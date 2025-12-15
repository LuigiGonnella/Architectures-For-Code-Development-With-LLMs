# Single-Agent Code Generation with LangGraph

This repository implements the **single-agent baseline** for Project A2  
(_Architectures for Code Development with LLMs_).

The goal is to study how a **single LLM**, structured as a **multi-step reasoning pipeline**, performs on code generation tasks (e.g. HumanEval), and to provide a clean foundation that can later scale to a **multi-agent architecture**.

---

## 🧠 Architecture Overview

We use **LangGraph** to structure the reasoning process of **one single agent** into multiple steps.

Although the pipeline has multiple nodes, **all nodes invoke the same LLM with the same agent identity**, so this is still a **single-agent system**.

### Single-Agent Pipeline

Task Analysis → Planning → Code Generation → Self-Review → Refinement

### Key Design Principles

- **Single agent, single identity**
- No role separation (planner/coder/debugger are _steps_, not agents)
- Explicit reasoning stages for reproducibility and analysis
- Clean separation between:
  - agent cognition
  - orchestration
  - execution tools
  - evaluation

This design improves correctness and modularity while remaining fully compliant with the single-agent requirement of A2.

---

## 📂 Project Structure (Core Files)

src/
├── core/
│ ├── llm.py # LLM runtime (Ollama interface, retries, identity)
│ ├── agent.py # Single-agent reasoning steps (analysis, planning, etc.)
│ ├── state.py # Shared LangGraph state definition
│ └── pipeline_single.py # LangGraph single-agent workflow
│
├── utils/
│ ├── task_loader.py # Load tasks from JSON
│ └── code_parser.py # Extract clean Python code from LLM output
│
├── tools/
│ └── executor.py # (Stub) Code execution sandbox
│
├── evaluation/
│ ├── functional.py # Functional correctness
│ └── quality.py # Static code metrics
│
data/
└── tasks.json # Sample tasks

---

## 🤖 Model Selection

We use **local, quantized models via Ollama** to keep the project cheap, reproducible, and easy to run.

### Models Tested

1. **Qwen2.5-Coder-7B-Instruct**  
   _Primary single-agent baseline (best quality / cost tradeoff)_

2. **DeepSeek-Coder-V2-Lite (6.7B)**  
   _Small, fast comparison model_

3. **CodeLlama-7B-Instruct**  
   _Classic baseline for reference_

All models run locally through Ollama and can be swapped via configuration without changing the pipeline.

---

## ▶️ Running the Sample Case

1. Start Ollama

```bash
ollama serve
2. Pull a model
ollama pull qwen2.5-coder:7b-instruct. ##assign the model inside the state within scripts/run_single_agent
3. Install dependencies
pip install -r requirements.txt
4. Run the single-agent pipeline
python scripts/run_single_agent.py

Sample Task (data/test-tasks.json)

[
  {
    "id": "smoke_test",
    "signature": "def add(a, b):",
    "docstring": "Return the sum of a and b."
  }
]

Expected Output (example)

def add(a, b):
    return a + b
```
