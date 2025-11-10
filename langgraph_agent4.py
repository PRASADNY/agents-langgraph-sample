
from langchain_ollama import ChatOllama
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
@tool
def get_stock_price(symbol: str) -> float:
    '''Return the current price of a stock given the stock symbol
    :param symbol: stock symbol
    :return: current price of the stock
    '''
    return {
        "META": 200.3,
        "TSLA": 100.4,
        "NFLX": 150.0,
        "GOOGL": 87.6
    }.get(symbol, 0.0)

tools = [get_stock_price]

llm = ChatOllama(model="llama3.2")
llm_with_tools = llm.bind_tools(tools)
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)
graph = builder.compile()

def main():
    print("Chatbot with Tools ready! Type 'exit' or 'quit' to end the conversation.")
    print("Try asking: 'What is the price of META?' or 'Tell me about TSLA stock'\n")
    
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
        # The graph will automatically route to tools if needed
        response = graph.invoke({"messages": messages})
        
        # Update messages with all responses (including tool calls and results)
        messages = response["messages"]
        
        # Get the last message (which should be the final response)
        last_message = messages[-1]
        
        # Display the response
        if hasattr(last_message, 'content') and last_message.content:
            print(f"Bot: {last_message.content}\n")
        else:
            # If no content, show the message type
            print(f"Bot: {type(last_message).__name__}\n")

if __name__ == "__main__":
    main()