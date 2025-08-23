#!/usr/bin/env python3
import os
import re
from pprint import pprint

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.sqlite import SqliteSaver

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

    # THIS IS THE SYNCH STREAMING (USING INVOKE)
    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

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

def main():
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
    )

    with SqliteSaver.from_conn_string(":memory:") as memory:
        abot = Agent(model, [tool], system=system_prompt, checkpointer=memory)

        question = "What is the weather in sf?"
        messages = few_shot + [HumanMessage(content=question)]
        thread = {"configurable": {"thread_id": "1"}}

        for event in abot.graph.stream({"messages": messages}, thread):
            for v in event.values():
                print(v['messages'][-1].content)

        print("\n\n\n")
        messages = [HumanMessage(content="What about in la?")]
        thread = {"configurable": {"thread_id": "1"}}
        for event in abot.graph.stream({"messages": messages}, thread):
            for v in event.values():
                print(v['messages'][-1].content)

        print("\n\n\n")
        messages = [HumanMessage(content="Which one is warmer?")]
        thread = {"configurable": {"thread_id": "1"}}
        for event in abot.graph.stream({"messages": messages}, thread):
            for v in event.values():
                print(v['messages'][-1].content)

if __name__ == "__main__":
    main()
