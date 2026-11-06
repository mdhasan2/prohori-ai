"""Single-operator local CLI slice. No LLM, arbitrary target, or shell execution."""

import argparse
import json
from pathlib import Path
from uuid import UUID, uuid4

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command, interrupt

from prohori_ai.application.local_workflow import (
    SCOPE_BINDING,
    Runtime,
    build_graph,
    proposal_binding,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", metavar="RUN_ID")
    args = parser.parse_args()
    run_id = str(UUID(args.resume)) if args.resume else str(uuid4())
    directory = Path(".prohori-cli")
    runtime = Runtime(directory, run_id)
    print(f"Run ID: {run_id}")
    print("Target: http://127.0.0.1:18080/ (fixed local lab)")
    try:
        with SqliteSaver.from_conn_string(str(directory / "checkpoints.sqlite")) as saver:
            graph = build_graph(runtime, saver)
            config: RunnableConfig = {"configurable": {"thread_id": run_id}}
            if args.resume:
                snapshot = graph.get_state(config)
                if not snapshot.values:
                    parser.error("Unknwon run ID")
                if snapshot.next and not snapshot.interrupts:
                    parser.error("Run was interrupted during execution; start a new run")
                result = dict(snapshot.values)
                result["__interrupt__"] = snapshot.interrupts
            else:
                result = graph.invoke({"status": "created"}, config)
            while result.get("__interrupt__"):
                request = result["__interrupt__"][0].value
                print(json.dumps(request, indent=2))
                print("Type approve to authorize; Enter to reject; pause to exit and resume later.")
                try:
                    answer = input("> ").strip().lower()
                except EOFError:
                    answer = "pause"
                if answer == "pause":
                    print(
                        "Paused. Resuem: uv run python -m prohori_ai.interfaces.cli "
                        f"--resume {run_id}"
                    )
                    return
                runtime.record_approval(request["gate"], request["binding"], answer == "approve")
                result = graph.invoke(Command(resume="operator_recorded"), config)
            final = graph.get_state(config).values
            print(json.dumps(final, indent=2))
            if final.get("status") == "failed":
                raise SystemExit(1)
    except KeyboardInterrupt:
        print("Interrupted. Pending approval checkpoints can be resumed with the Run ID.")
        raise SystemExit(130) from None
    finally:
        runtime.close()


if __name__ == "__main__":
    main()
