#!/usr/bin/env python3

# https://chatgpt.com/share/68aa362e-0ee0-8000-ac53-c9b1b7eeb83e
"""
You’re still not seeing individual tokens because Gemini’s LangChain wrapper quietly disables streaming
when tool-calling is involved. That’s harshly ironic: you built a streaming agent, but it's effectively
forced into a dump-all-at-the-end mode because the model doesn’t support token streaming when chained with tools.
Happens all the time—tools and streaming don’t play nice in this combo.

Reddit users pointed this out bluntly:

“Gemini API does not support tools in combination with streaming calls.”
Reddit

In short: your switch to .astream() in call_openai is entirely in vain if the LLM detects tool binding.
And ChatGoogleGenerativeAI—bless its over-engineered soul—is apparently detecting that tool usage and disabling streaming.
"""


import asyncio
import os

from dotenv import load_dotenv
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:

    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    # FOR THE ASYNCH STREAMING HERE
    async def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        async for chunk in self.model.astream(messages):
            yield {'messages': [chunk]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:
                print("\n ....bad tool name....")
                result = "bad tool name, retry"
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

async def main():
    load_dotenv()
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tool = TavilySearch(tavily_api_key=tavily_api_key, max_results=4)

    system_prompt = """You are a smart research assistant.
You have access to the following tool:

TavilySearch — use this to look up any information from the web, including current events and live data such as weather.

Rules:
- Always call TavilySearch when the user asks for up-to-date or real-time info.
- Return results in JSON tool call format, never guess.
- Do not say you "cannot" do something if TavilySearch can provide the answer.
"""

    # Few-shot example to teach Gemini tool call format
    few_shot = [
        HumanMessage(content="What's the weather in New York right now?"),
        AIMessage(content="", tool_calls=[
            {"id": "call_1", "name": tool.name, "args": {"query": "current weather in New York"}}
        ])
    ]

    model = ChatGoogleGenerativeAI(
        google_api_key=os.getenv("GOOGLE_GENAI_API_KEY"),
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        disable_streaming=False, stream=True
    )

    async with AsyncSqliteSaver.from_conn_string(":memory:") as memory:
        abot = Agent(model, [tool], system=system_prompt, checkpointer=memory)

        question = "What is the weather in SF?"
        messages = few_shot + [HumanMessage(content=question)]
        thread = {"configurable": {"thread_id": "3"}}
        async for event in abot.graph.astream_events({"messages": messages}, thread, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    print(content, end=" | ")
    print()


if __name__ == "__main__":
    asyncio.run(main())
