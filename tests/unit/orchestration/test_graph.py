"""Unit tests for Supervisor LangGraph topology."""

from langgraph.graph import END, START

from prohori_ai.orchestration.graph import (
    build_supervisor,
)

# def graph_edges() -> set[tuple[str, str]]:
#     graph = build_supervisor()

#     drawable = graph.get_graph()


def test_graph_contains_expected_nodes() -> None:
    """Verify that the supervisor contains tits required nodes."""
    graph = build_supervisor().compile()

    drawable = graph.get_graph()

    expected_nodes = {
        "observe",
        "discover",
    }

    assert expected_nodes.issubset(set(drawable.nodes))
