from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class ProtFolioState(TypedDict):
    amount_usd: float
    total_usd: float
    total_inr: float
    tax_usd: float

def calc_total(state: ProtFolioState) -> ProtFolioState:
    state["total_usd"] = state["amount_usd"] * 1.08
    return state

def convert_to_inr(state: ProtFolioState) -> ProtFolioState:
    state["total_inr"] = state["total_usd"] * 85
    return state

def calculate_tax(state: ProtFolioState) -> ProtFolioState:
    state["tax_usd"] = state["total_usd"] * 0.6
    return state




def main():
    print("Hello from agents-langgraph-sample!")
   
    builder = StateGraph(ProtFolioState)
    builder.add_node("calc_total_node", calc_total)
    builder.add_node("convert_to_inr_node", convert_to_inr)
    builder.add_node("calculate_tax_node", calculate_tax)
    builder.add_edge(START, "calc_total_node")
    builder.add_edge("calc_total_node", "calculate_tax_node")    
    builder.add_edge("calculate_tax_node", "convert_to_inr_node")
    builder.add_edge("convert_to_inr_node", END)
    graph = builder.compile()
    result = graph.invoke({"amount_usd": 1000, "total_usd": 1000, "tax_usd": 0, "total_inr": 0})
    print("Graph result:", result)
   



if __name__ == "__main__":
    main()
