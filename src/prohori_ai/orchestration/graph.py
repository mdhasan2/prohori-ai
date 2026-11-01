from langgraph.graph import END, START, StateGraph

from prohori_ai.orchestration.nodes import (
    discover_node,
    observe_node,
)
from prohori_ai.orchestration.state import SupervisorState

# from langgraph.checkpoint.sqlite import SqliteSaver


def build_supervisor() -> StateGraph[
    SupervisorState,
    None,
    SupervisorState,
    SupervisorState,
]:
    """Build the uncompleted supervisor graph."""

    builder = StateGraph(SupervisorState)

    builder.add_node("observe", observe_node)
    builder.add_node("discover", discover_node)

    builder.add_edge(START, "observe")
    builder.add_edge("observe", "discover")
    builder.add_edge("discover", END)

    return builder


# with SqliteSaver.from_conn_string(
#     "var/checkpoints.db"
# ) as checkpointer:
#     graph = build_supervisor().compile(
#         checkpointer=checkpointer,
#     )
