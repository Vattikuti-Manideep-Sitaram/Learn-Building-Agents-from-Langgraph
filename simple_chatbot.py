from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph,START
from langgraph.graph import add_messages
from langchain.chat_models import init_chat_model

class State(TypedDict):
    messages: Annotated[list,add_messages]
    
graph_builder=StateGraph(State)

llm=init_chat_model("openai:gpt-4.1")

def chatbot(state: State):
    return {"messages":[llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot",chatbot)

graph_builder.add_edge(START,"chatbot")

graph=graph_builder.compile()


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

def custom_graph_update(user_input : str):
    res= graph.invoke({"messages": [{"role":"user","content":user_input}]})
    print("Assistant:", res["messages"][-1].content)

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    custom_graph_update(user_input)
        