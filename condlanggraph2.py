from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class ProtFolioState(TypedDict):
    amount_usd: float
    total_usd: float
    total:float
    target_currency:Literal["INR","EUR"]

    
def calc_total(state: ProtFolioState) -> ProtFolioState:
    state["total_usd"] = state["amount_usd"] * 1.08
    return state

def convert_to_inr(state: ProtFolioState) -> ProtFolioState:
    state["total"] = state["total_usd"] * 85
    return state

def convert_to_eur(state: ProtFolioState) -> ProtFolioState:
    state["total"] = state["total_usd"] * 0.89
    return state

def conditional_edge(state: ProtFolioState) -> str:
    return state["target_currency"]


def main():

    builder = StateGraph(ProtFolioState)
    builder.add_node("calc_total_node", calc_total)
    builder.add_node("convert_to_inr_node", convert_to_inr)
    builder.add_node("convert_to_eur_node", convert_to_eur)
    builder.add_edge(START, "calc_total_node")
    builder.add_conditional_edges("calc_total_node", conditional_edge, {
        "INR": "convert_to_inr_node",
        "EUR": "convert_to_eur_node"
    })
    builder.add_edge(["convert_to_inr_node", "convert_to_eur_node"], END)   
    graph = builder.compile()
    result = graph.invoke({"amount_usd": 1000, "target_currency": "INR"})
    print("Graph result:", result)
    print(f"Total in INR: {result['total']}")
    result = graph.invoke({"amount_usd": 1000, "total_usd": 0, "total": 0, "target_currency": "EUR"})
    print("Graph result:", result)
    print(f"Total in EUR: {result['total']}")




if __name__ == "__main__":
    main()
