"""
LangGraph workflow definition.

This is the "brain" that orchestrates all agents.
Think of it as a flowchart:

  [Start] → [Research Agent] → [Writer Agent] → [Critic Agent] → Decision
                                      ↑                              |
                                      |_______ Needs Revision _______|
                                                                     |
                                                              [End - Approved]
"""
from langgraph.graph import StateGraph, END
from src.state import ResearchState
from src.agents import research_agent, writer_agent, critic_agent


def should_revise(state: ResearchState) -> str:
    """
    Conditional edge: decide whether to revise or finish.
    This is like an 'if' statement in your flowchart.
    """
    if state.get("is_approved", False):
        return "approved"
    
    # Safety valve: max 2 revisions to prevent infinite loops
    if state.get("revision_count", 0) >= 3:
        return "approved"  # Accept after max revisions
    
    return "needs_revision"


def build_research_graph():
    """
    Build and compile the multi-agent research graph.
    
    The graph looks like this:
    
    START → research → write → critique → [approved?] → END
                         ↑                     |
                         |_____ revision _______|
    """
    # Create the graph with our state schema
    graph = StateGraph(ResearchState)  # type: ignore
    
    # Add nodes (each node is an agent)
    graph.add_node("research", research_agent)
    graph.add_node("write", writer_agent)
    graph.add_node("critique", critic_agent)
    
    # Add edges (the flow between agents)
    # Start → Research (always start with research)
    graph.set_entry_point("research")
    
    # Research → Write (after research, always write)
    graph.add_edge("research", "write")
    
    # Write → Critique (after writing, always get feedback)
    graph.add_edge("write", "critique")
    
    # Critique → ? (conditional: either finish or revise)
    graph.add_conditional_edges(
        "critique",
        should_revise,
        {
            "approved": END,
            "needs_revision": "write",
        },
    )
    
    # Compile the graph (like building your Flutter app)
    return graph.compile()