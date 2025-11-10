from typing import Annotated
from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

llm = ChatOllama(model="llama3.2")

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(State)
builder.add_node("chatbot_node", chatbot)

builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

print("Chatbot ready! Type 'exit' or 'quit' to end the conversation.\n")

# Maintain conversation history
messages = []

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'q']:
        print("Goodbye!")
        break
    
    if not user_input:
        continue
    
    # Add user message to history
    user_message = HumanMessage(content=user_input)
    messages.append(user_message)
    
    # Get response with full conversation history
    response = graph.invoke({"messages": messages})
    
    # Add bot response to history for context
    bot_message = response["messages"][-1]
    messages.append(bot_message)
    
    print(f"Bot: {bot_message.content}\n")