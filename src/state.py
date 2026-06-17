from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class ResearchState(TypedDict):
 
    topic: str
    messages: Annotated[list, add_messages]
    research_data: str
    draft_report: str
    critic_feedback: str
    final_report: str
    revision_count: int
    is_approved: bool