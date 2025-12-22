import argparse
import os
import sys

from src.core.pipeline import build_single_agent_graph
from src.utils.task_loader import load_tasks
from src.utils.config import config
from src.evaluation.quality import format_metrics_report

# Ensure project root is on sys.path so `src` package is importable when
# running this script directly (e.g. `python scripts/run_single_agent.py`).
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


def main():
    parser = argparse.ArgumentParser(
        description="Run single-agent code generation pipeline"
    )
    parser.add_argument(
        "task_file",
        nargs="?",
        default="data/test-tasks.json",
        help="Path to task file (e.g., data/logic/logic-tasks.json)",
    )
    args = parser.parse_args()

    graph = build_single_agent_graph()
    tasks = load_tasks(args.task_file)

    for task in tasks:
        print("\n\nQUERY:")
        print(f"  ID        : {task.get('id')}")
        print(f"  Signature : {task.get('signature')}")
        print(f"  Docstring : {task.get('docstring')}")
        if task.get("examples"):
            print("  Examples  :")
            for ex in task["examples"]:
                print(f"    - Input : {ex.get('input')}")
                print(f"      Output: {ex.get('output')}")
        if task.get("difficulty"):
            print(f"  Difficulty: {task.get('difficulty')}\n\n")

        state = {
            "task_id": task["id"],
            "signature": task["signature"],
            "docstring": task["docstring"],
            "examples": task.get("examples"),
            "difficulty": task.get("difficulty"),
            "model": config.model_name,
            "analysis": None,
            "plan": None,
            "code": None,
            "review": None,
            "exec_result": None,
            "quality_metrics": None,
            "refinement_count": 0,
        }

        final_state = graph.invoke(state)

        print("\n=== FINAL OUTPUT ===")
        print(final_state["code"])

        if final_state.get("quality_metrics"):
            print("\n" + format_metrics_report(final_state["quality_metrics"]))


if __name__ == "__main__":
    main()


# Usage examples:
# python -m scripts.run_single_agent                              # uses default (data/test-tasks.json)
# python -m scripts.run_single_agent data/logic/logic-tasks.json  # run logic tasks
# python -m scripts.run_single_agent data/strings/strings-tasks.json
# python -m scripts.run_single_agent data/dsa/dsa-tasks.json
