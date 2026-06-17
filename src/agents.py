"""
Agent definitions for the multi-agent research assistant.

Each agent is a function that:
1. Reads from the shared state
2. Does its job (calls the LLM, uses tools, etc.)
3. Returns updates to the shared state

Think of each agent as a specialized worker on a team.
"""
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from src.state import ResearchState
from tools.search import get_search_tool

# Initialize the Ollama LLM
# This runs completely offline on your local machine
llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)

# Initialize our tools
search_tool = get_search_tool()


def research_agent(state: ResearchState) -> dict:
    """
    🔍 RESEARCH AGENT
    Job: Search the web for information about the topic.
    Like a research assistant who goes to the library for you.
    """
    topic = state["topic"]
    
    # Use the search tool to find information
    search_tool = get_search_tool()
    search_results = search_tool.invoke(topic)
    
    # Format the search results into readable text
    research_data = ""
    for result in search_results:
        source = result.metadata.get('source', 'Unknown Document')
        page = result.metadata.get('page', 'Unknown Page')
        research_data += f"Source: {source} (Page {page})\n"
        research_data += f"Content: {result.page_content}\n\n"
    
    # Ask the LLM to organize and extract key insights
    organize_prompt = f"""You are a research analyst. Organize the following raw research data 
about "{topic}" into clear, structured key findings. 

Extract the most important facts, statistics, and insights.

Raw Research Data:
{research_data}

Provide your organized findings in a clear, bulleted format."""

    response = llm.invoke(organize_prompt)
    
    return {
        "research_data": response.content,
        "messages": [("system", f"✅ Research complete for: {topic}")],
    }


def writer_agent(state: ResearchState) -> dict:
    """
    ✍️ WRITER AGENT
    Job: Take the research data and write a polished report.
    Like a journalist who writes an article from research notes.
    """
    topic = state["topic"]
    research_data = state["research_data"]
    critic_feedback = state.get("critic_feedback", "")
    revision_count = state.get("revision_count", 0)
    
    # Build the prompt based on whether this is a first draft or revision
    if revision_count == 0:
        write_prompt = f"""You are an expert technical writer. Write a comprehensive, 
well-structured report about "{topic}" using the research data below.

Research Data:
{research_data}

Your report should include:
1. An engaging introduction
2. Key findings organized into clear sections with headers
3. Important statistics and facts
4. A conclusion with key takeaways

Write in a professional but accessible tone. Use markdown formatting."""
    else:
        write_prompt = f"""You are an expert technical writer. Revise the following report 
based on the critic's feedback.

Original Report:
{state.get('draft_report', '')}

Critic's Feedback:
{critic_feedback}

Research Data (for reference):
{research_data}

Improve the report by addressing ALL feedback points. Maintain markdown formatting."""
    
    response = llm.invoke(write_prompt)
    
    return {
        "draft_report": response.content,
        "revision_count": revision_count + 1,
        "messages": [("system", f"✅ Draft v{revision_count + 1} complete")],
    }


def critic_agent(state: ResearchState) -> dict:
    """
    🧐 CRITIC AGENT
    Job: Review the draft report and decide if it's good enough.
    Like an editor who reviews articles before publication.
    """
    draft_report = state["draft_report"]
    topic = state["topic"]
    
    critic_prompt = f"""You are a strict but fair editorial critic. Review this report about "{topic}".

Report to Review:
{draft_report}

Evaluate on these criteria:
1. **Accuracy**: Are claims supported by the research?
2. **Completeness**: Does it cover the topic thoroughly?
3. **Clarity**: Is it well-organized and easy to understand?
4. **Engagement**: Is it interesting to read?

Score each criterion out of 10.

If the TOTAL score is 32 or above (out of 40), respond with:
VERDICT: APPROVED
[Your brief praise]

If the total score is below 32, respond with:
VERDICT: NEEDS_REVISION
[Your specific, actionable feedback for improvement]

Be constructive — give specific suggestions, not vague criticism."""

    response = llm.invoke(critic_prompt)
    
    is_approved = "VERDICT: APPROVED" in response.content
    
    return {
        "critic_feedback": response.content,
        "is_approved": is_approved,
        "messages": [("system", f"{'✅ Report APPROVED' if is_approved else '🔄 Revision needed'}")],
    }