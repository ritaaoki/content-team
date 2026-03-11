import operator
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import Annotated, Literal
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, add_messages, END
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.checkpoint.memory import MemorySaver
from datetime import datetime
from researcher import graph as research_agent
from copywriter import graph as copywriter_agent
from idea_generator import graph as idea_generator_agent
from langgraph.types import Command, RunnableConfig

load_dotenv()

# Load the supervisor system prompt
supervisor_prompt = open("prompts/supervisor.md", "r", encoding="utf-8").read()


class SupervisorState(BaseModel):
    messages: Annotated[list, add_messages] = []
    research_reports: Annotated[list, operator.add] = []
    task_description: Annotated[str | None, lambda x, y: y] = None


@tool
async def handoff_to_subagent(
    agent_name: Literal["researcher", "copywriter", "idea_generator"],
    task_description: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
    ):
    """Assign a task to a sub-agent: researcher, copywriter, or idea_generator.
    
    Args:
        agent_name: The name of the agent to handoff the task to. Valid agent names are researcher, copywriter, and idea_generator.
        task_description: The description of the task to be completed.
    """
    update = {
        "task_description": task_description,
        "messages": [ToolMessage(
            name=f"handoff_to_{agent_name}",
            content=f"Successfully handed off task to {agent_name}.",
            tool_call_id=tool_call_id,
        )],
        }
    return Command(
        goto=f"call_{agent_name}",
        update=update
        )


async def call_researcher(state: SupervisorState, config: RunnableConfig):
    """Call the researcher agent."""
    research_response = await research_agent.ainvoke(
        input={
            "messages": [HumanMessage(content=state.task_description)],
            },
        config=config,
    )
    ai_message = AIMessage(name="researcher", content=research_response["messages"][-1].content)
    return {
        "research_reports": research_response["research_reports"],
        "messages": [ai_message],
        }


async def call_copywriter(state: SupervisorState, config: RunnableConfig):
    """Call the copywriter agent."""
    copywriter_response = await copywriter_agent.ainvoke(
        input={
            "messages": [HumanMessage(content=state.task_description)],
            "research_reports": state.research_reports,
            },
        config=config,
        )
    ai_message = AIMessage(name="copywriter", content=copywriter_response["messages"][-1].content)
    return {"messages": [ai_message]}


async def call_idea_generator(state: SupervisorState, config: RunnableConfig):
    """Call the idea generator agent."""
    idea_response = await idea_generator_agent.ainvoke(
        input={
            "messages": [HumanMessage(content=state.task_description)],
            },
        config=config,
    )
    ai_message = AIMessage(name="idea_generator", content=idea_response["messages"][-1].content)
    return {"messages": [ai_message]}


llm = ChatGoogleGenerativeAI(
        name="Supervisor",
        model="gemini-3.1-flash-lite-preview",
)

tools = [handoff_to_subagent]
llm_with_tools = llm.bind_tools(tools)


async def supervisor(state: SupervisorState):
    """The main supervisor agent."""
    response = llm_with_tools.invoke([
        SystemMessage(content=supervisor_prompt.format(current_datetime=datetime.now()))
        ] + state.messages)
    return {"messages": [response]}


async def supervisor_router(state: SupervisorState) -> str:
    """Route to the tools node if the supervisor makes a tool call."""
    if state.messages[-1].tool_calls:
        return "tools"
    return END


builder = StateGraph(SupervisorState)

builder.add_node(supervisor)
builder.add_node("tools", ToolNode(tools))
builder.add_node(call_researcher)
builder.add_node(call_copywriter)
builder.add_node(call_idea_generator)

builder.set_entry_point("supervisor")

builder.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "tools": "tools",
        END: END,
    }
)

builder.add_edge("call_researcher", "supervisor")
builder.add_edge("call_copywriter", "supervisor")
builder.add_edge("call_idea_generator", "supervisor")

graph = builder.compile(checkpointer=MemorySaver())