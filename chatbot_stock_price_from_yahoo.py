from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import yfinance as yf

class StockState(TypedDict):
    symbol: str
    price: float
    currency: str
    change: float
    change_percent: float
    error: str

def get_stock_price(state: StockState) -> StockState:
    """Fetch stock price from Yahoo Finance"""
    try:
        symbol = state["symbol"].upper()
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get current price
        current_data = ticker.history(period="1d")
        if current_data.empty:
            return {
                **state,
                "error": f"Could not fetch data for symbol {symbol}"
            }
        
        current_price = current_data['Close'].iloc[-1]
        previous_close = info.get('previousClose', current_price)
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close else 0
        
        return {
            **state,
            "price": round(current_price, 2),
            "currency": info.get("currency", "USD"),
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "error": ""
        }
    except Exception as e:
        return {
            **state,
            "error": f"Error fetching stock price: {str(e)}"
        }

def format_output(state: StockState) -> StockState:
    """Format the output message"""
    if state.get("error"):
        print(f"Error: {state['error']}")
    else:
        symbol = state["symbol"]
        price = state["price"]
        currency = state["currency"]
        change = state["change"]
        change_percent = state["change_percent"]
        change_sign = "+" if change >= 0 else ""
        
        print(f"\n{symbol} Stock Price")
        print(f"{'='*40}")
        print(f"Price: {currency} {price:,.2f}")
        print(f"Change: {change_sign}{change:,.2f} ({change_sign}{change_percent:.2f}%)")
        print(f"{'='*40}\n")
    
    return state

def main():
    # Create the graph
    builder = StateGraph(StockState)
    builder.add_node("get_stock_price", get_stock_price)
    builder.add_node("format_output", format_output)
    
    builder.add_edge(START, "get_stock_price")
    builder.add_edge("get_stock_price", "format_output")
    builder.add_edge("format_output", END)
    
    graph = builder.compile()
    
    # Interactive loop
    print("Stock Price Fetcher (Yahoo Finance)")
    print("Type 'exit' or 'quit' to end\n")
    
    while True:
        symbol = input("Enter stock symbol (e.g., AAPL, MSFT, GOOGL): ").strip().upper()
        
        if symbol.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not symbol:
            continue
        
        result = graph.invoke({
            "symbol": symbol,
            "price": 0.0,
            "currency": "USD",
            "change": 0.0,
            "change_percent": 0.0,
            "error": ""
        })

if __name__ == "__main__":
    main()

