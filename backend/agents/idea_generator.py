import operator
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Annotated
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, add_messages, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import InjectedState
from datetime import datetime
from pathlib import Path

load_dotenv()

# Load the idea generator system prompt
idea_generator_prompt = open("prompts/idea_generator.md", "r", encoding="utf-8").read()


class IdeaGeneratorState(BaseModel):
    """The state of the idea generator agent.
    
    The research_reports attribute is shared with the supervisor state.
    """
    messages: Annotated[list, add_messages] = []
    research_reports: Annotated[list, operator.add] = []


@tool
async def review_existing_posts():
    """Review all existing posts in the generated_content folder to analyze topics, tone, and style.

    Returns:
        A dictionary containing all existing posts and their contents.
    """
    posts = {}
    for folder in [Path("example_content"), Path("generated_content")]:
        for file in folder.rglob("*.md"):
            posts[file.stem] = file.read_text(encoding="utf-8", errors="replace")
    
    
    if not posts:
        return {"message": "No existing posts found in generated_content folder or example_content folder.", "posts": {}}

    return {
        "message": f"Found {len(posts)} existing post(s).",
        "posts": posts
    }


@tool
async def generate_ideas_report(
    title: str,
    ideas: str,
):
    """Save the generated content ideas as a report in the generated_content folder.

    Args:
        title: The title of the ideas report.
        ideas: The content ideas in markdown format.

    Returns:
        A string indicating the location of the saved report.
    """
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title).strip()
    filename = f"generated_content/{safe_title}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(ideas)

    return f"The ideas report has been saved to {filename}"


llm = ChatGoogleGenerativeAI(
    name="IdeaGenerator",
    model="gemini-3.1-flash-lite-preview",
)

tools = [
    review_existing_posts,
    generate_ideas_report,
]
llm_with_tools = llm.bind_tools(tools)


async def idea_generator(state: IdeaGeneratorState):
    """The main idea generator agent."""
    system_prompt = SystemMessage(content=idea_generator_prompt.format(
        current_datetime=datetime.now(),
    ))
    response = llm_with_tools.invoke([system_prompt] + state.messages)
    return {"messages": [response]}


async def idea_generator_router(state: IdeaGeneratorState) -> str:
    """Route to the tools node if the idea generator makes a tool call."""
    if state.messages[-1].tool_calls:
        return "tools"
    return END


builder = StateGraph(IdeaGeneratorState)

builder.add_node(idea_generator)
builder.add_node("tools", ToolNode(tools))

builder.set_entry_point("idea_generator")

builder.add_conditional_edges(
    "idea_generator",
    idea_generator_router,
    {
        "tools": "tools",
        END: END,
    }
)
builder.add_edge("tools", "idea_generator")

graph = builder.compile()