# Agents LangGraph Sample

A collection of LangGraph examples demonstrating different patterns and use cases for building stateful agent workflows.

## Prerequisites

- Python >= 3.13
- [uv](https://github.com/astral-sh/uv) package manager
- Ollama (for chatbot examples) - See installation instructions below

## Installation

### Step 1: Install Ollama

Ollama is required for chatbot examples (`chatbot.py` and `langgraph_tool.py`). Install it based on your operating system:

#### Windows
1. Download the installer from [ollama.com/download](https://ollama.com/download)
2. Run the installer (OllamaSetup.exe)
3. Verify installation by opening PowerShell and running:
   ```bash
   ollama --version
   ```

#### macOS
1. Download from [ollama.com/download](https://ollama.com/download) or use Homebrew:
   ```bash
   brew install ollama
   ```
2. Start Ollama service:
   ```bash
   ollama serve
   ```

#### Linux
1. Install using the official script:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Or use your package manager (e.g., `apt`, `yum`, `dnf`)

#### After Installation
1. Pull the required model:
   ```bash
   ollama pull llama3.2
   ```
2. Verify the model is installed:
   ```bash
   ollama list
   ```

### Step 2: Install Python Dependencies

1. Install dependencies:
```bash
uv sync
```

2. Activate virtual environment:
```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

## Project Files

### 1. `LangGraph.py`
**Description:** Basic sequential workflow example demonstrating a portfolio calculation pipeline.

**Features:**
- Calculates total USD amount with 8% multiplier
- Calculates tax (60% of total USD)
- Converts final amount to INR

**Workflow:**
```
START → calc_total → calculate_tax → convert_to_inr → END
```

**Usage:**
```bash
python LangGraph.py
```

**Example Output:**
- Input: `amount_usd: 1000`
- Process: `total_usd = 1080`, `tax_usd = 648`, `total_inr = 91800`

---

### 2. `condlanggraph.py`
**Description:** Conditional routing example with currency conversion based on target currency.

**Features:**
- Calculates total USD with 8% multiplier
- Conditionally routes to INR or EUR conversion based on `target_currency`
- Uses conditional edges for dynamic workflow routing

**Workflow:**
```
START → calc_total → [conditional_edge] → convert_to_inr OR convert_to_eur → END
```

**Usage:**
```bash
python condlanggraph.py
```

**Example:**
- Input: `{"amount_usd": 1000, "target_currency": "INR"}`
- Output: `total: 91800` (1000 * 1.08 * 85)

---

### 3. `chatbot.py`
**Description:** Interactive chatbot using Ollama's Llama 3.2 model with conversation history.

**Features:**
- Interactive command-line chatbot
- Maintains full conversation history for context
- Uses LangGraph for message handling
- Powered by Ollama (local LLM)

**Requirements:**
- Ollama must be running locally
- `llama3.2` model must be installed: `ollama pull llama3.2`

**Usage:**
```bash
python chatbot.py
```

**Commands:**
- Type your message and press Enter
- Type `exit`, `quit`, or `q` to end the conversation

**Example:**
```
You: Who walked on the moon first?
Bot: Neil Armstrong
```

---

### 4. `chatbot_stock_price.py`
**Description:** Stock price fetcher using Yahoo Finance API with LangGraph workflow.

**Features:**
- Fetches real-time stock prices from Yahoo Finance
- Calculates price change and percentage change
- Formatted output with currency information
- Interactive command-line interface

**Workflow:**
```
START → get_stock_price → format_output → END
```

**Usage:**
```bash
python chatbot_stock_price.py
```

**Example:**
```
```
Enter stock symbol (e.g., AAPL, MSFT, GOOGL): AAPL

AAPL Stock Price
========================================
Price: USD 175.50
Change: +2.30 (+1.33%)
========================================
```

**Supported Symbols:**
- Any valid stock ticker symbol (e.g., AAPL, MSFT, GOOGL, TSLA, etc.)

---

### 5. `langgraph_tool.py`
**Description:** LangGraph agent with tool calling capabilities using Ollama and custom tools.

**Features:**
- Demonstrates tool integration with LangGraph
- Uses Ollama's Llama 3.2 model with tool binding
- Custom stock price lookup tool
- Conditional routing between chatbot and tool execution

**Workflow:**
```
START → chatbot → [tools_condition] → tools (if needed) → END
```

**Requirements:**
- Ollama must be running locally
- `llama3.2` model must be installed: `ollama pull llama3.2`

**Usage:**
```python
from langgraph_tool import graph
from langchain_core.messages import HumanMessage

# Example usage
response = graph.invoke({
    "messages": [HumanMessage(content="What is the price of AAPL?")]
})
print(response["messages"][-1].content)
```

**Features:**
- The LLM can decide when to call tools based on user queries
- Tools are automatically invoked when needed
- Supports custom tool definitions using `@tool` decorator

**How the Agent Handles Complex Questions:**

The agent can answer complex, multi-step questions by intelligently calling tools multiple times and performing calculations. Here's an example:

**Example Query:**
```
You: I want to buy 20 META stocks using current price. Then 10 TSLA. What will be the total cost?
```

**Agent Response:**
```
Bot: The current price of 1 share of Meta (META) is $200.30.
The current price of 1 share of Tesla (TSLA) is $100.40.

If you want to buy 20 META stocks, the total cost would be:
20 x $200.30 = $4,006

If you want to buy 10 TSLA stocks, the total cost would be:
10 x $100.40 = $1,004

The total cost of buying both would be:
$4,006 + $1,004 = $5,010
```

**Workflow Diagram for Complex Questions:**

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query                                │
│  "Buy 20 META stocks, then 10 TSLA. What's the total cost?" │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │   START Node    │
              └────────┬─────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │    Chatbot Node          │
        │  (LLM analyzes query)    │
        │  - Identifies: META, TSLA│
        │  - Needs: stock prices   │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │  tools_condition        │
        │  (Decision: Use tools?) │
        └────────┬──────────────────┘
                 │ YES
                 ▼
        ┌──────────────────────────┐
        │    Tools Node            │
        │  get_stock_price("META") │
        │  Returns: $200.30       │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │    Chatbot Node          │
        │  (LLM processes result)  │
        │  - Has META price        │
        │  - Still needs TSLA      │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │  tools_condition        │
        │  (Decision: Use tools?) │
        └────────┬──────────────────┘
                 │ YES
                 ▼
        ┌──────────────────────────┐
        │    Tools Node            │
        │  get_stock_price("TSLA") │
        │  Returns: $100.40       │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │    Chatbot Node          │
        │  (LLM performs math)      │
        │  - 20 × $200.30 = $4,006 │
        │  - 10 × $100.40 = $1,004 │
        │  - Total = $5,010        │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │  tools_condition        │
        │  (Decision: Use tools?) │
        └────────┬──────────────────┘
                 │ NO (has all data)
                 ▼
              ┌──────────┐
              │ END Node │
              └──────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │   Final Response         │
        │  (Comprehensive answer)   │
        └──────────────────────────┘
```

**Key Capabilities:**
- **Multi-step reasoning**: Breaks down complex questions into steps
- **Multiple tool calls**: Can call tools multiple times as needed
- **State management**: Maintains context between tool calls
- **Automatic calculations**: Performs arithmetic operations
- **Natural language synthesis**: Combines tool results into coherent answers

---

### 7. `langgraph_memory.py`
**Description:** LangGraph agent with persistent memory using `MemorySaver` checkpointer for remembering previous calculations and conversation context across multiple interactions.

**Key Feature: MemorySaver Checkpointing**

Unlike basic agents that only remember within a single conversation turn, `MemorySaver` enables the agent to persist state across multiple invocations using a `thread_id`. This allows the agent to remember previous calculations and build upon them in subsequent queries.

**How MemorySaver Works:**

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
config = {'configurable': {'thread_id': '1'}}

# Each invocation with the same thread_id maintains state
response = graph.invoke({"messages": messages}, config=config)
```

**Key Components:**
1. **MemorySaver**: Creates an in-memory checkpoint store
2. **checkpointer**: Passed to `graph.compile()` to enable state persistence
3. **thread_id**: Unique identifier that groups related conversations
4. **config**: Passed to each `invoke()` call to maintain thread context

**Example: Remembering Previous Calculations**

The following conversation demonstrates how `MemorySaver` enables the agent to remember and build upon previous results:

**Turn 1:**
```
You: I want to buy 10 META stocks using current price. Then 10 TSLA. What will be the total cost?
Bot: Based on the latest available data, the current price of 1 share of META (Meta) stock is approximately $200.30 USD.

To buy 10 shares of META at this price would be:
10 x $200.30 = $2003.00

The current price of 1 share of TSLA (Tesla) stock is approximately $100.40 USD.

To buy 10 shares of TSLA at this price would be:
10 x $100.40 = $1040.00

The total cost for both purchases would be:
$2003.00 + $1040.00 = $3043.00
```

**Turn 2:**
```
You: Using the current price tell me the total price of 10 GOOGL stocks and add it to previous total cost
Bot: Based on the latest available data, the current price of 1 share of GOOGL (Alphabet Inc.) stock is approximately $87.60 USD.

To buy 10 shares of GOOGL at this price would be:
10 x $87.60 = $876.00

Adding this to the previous total cost:
$3043.00 + $876.00 = $3919.00
```
*Note: Agent remembers the updated total of $3043.00 and adds the new purchase*

**How Memory Persistence Works:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Turn 1: Initial Query                    │
│  "Buy 10 META + 10 TSLA. What's the total cost?"            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │  Graph Execution         │
        │  - Calculates: $3043.00  │
        └────────┬──────────────────┘
                 │
                 ▼
        ┌──────────────────────────┐
        │  MemorySaver            │
        │  thread_id: '1'          │
        │  Checkpoint saved        │
        │  State: $3043.00         │
        └──────────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────────────────────────────┐
        │                    Turn 2: Follow-up Query                   │
        │  "Add 10 GOOGL to previous total cost"                      │
        └──────────────────────┬──────────────────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  MemorySaver            │
                    │  thread_id: '1'          │
                    │  Retrieves checkpoint    │
                    │  Previous state: $3043.00│
                    └────────┬──────────────────┘
                             │
                             ▼
                    ┌──────────────────────────┐
                    │  Graph Execution         │
                    │  - Has context: $3043.00  │
                    │  - Adds GOOGL: $876.00    │
                    │  - New total: $3919.00     │
                    └──────────────────────────┘
```

**Benefits of MemorySaver:**

1. **Persistent Context**: Maintains conversation state across multiple invocations
2. **Thread Isolation**: Different `thread_id` values create separate conversation contexts
3. **State Recovery**: Can resume conversations from any checkpoint
4. **Incremental Calculations**: Builds upon previous results naturally
5. **No Manual State Management**: LangGraph handles checkpointing automatically

**Comparison: With vs Without MemorySaver**

| Aspect | Without MemorySaver | With MemorySaver |
|--------|---------------------|------------------|
| **State Persistence** | Only within single invocation | Across multiple invocations |
| **Previous Results** | Not remembered | Automatically remembered |
| **Follow-up Queries** | Require re-stating context | Can reference "previous total" |
| **Thread Management** | Not applicable | Each thread_id = separate conversation |
| **Use Case** | Single-turn interactions | Multi-turn conversations with context |

**Requirements:**
- Ollama must be running locally
- `llama3.2` model must be installed: `ollama pull llama3.2`

**Usage:**
```bash
python langgraph_memory.py
```

---

## Dependencies

- `langgraph>=1.0.2` - State graph framework
- `langchain-core>=0.3.0` - Core LangChain functionality
- `langchain-ollama>=0.2.0` - Ollama integration
- `yfinance>=0.2.0` - Yahoo Finance API
- `python-dotenv>=1.2.1` - Environment variable management
- `notebook>=7.4.7` - Jupyter notebook support

## Key Concepts Demonstrated

1. **Sequential Workflows** (`LangGraph.py`) - Linear node execution
2. **Conditional Routing** (`condlanggraph.py`) - Dynamic path selection based on state
3. **Message Handling** (`chatbot.py`) - Conversation state management
4. **External API Integration** (`chatbot_stock_price.py`) - Fetching data from external sources
5. **Tool Calling** (`langgraph_tool.py`) - LLM agents with function/tool execution capabilities
6. **Persistent Memory** (`langgraph_memory.py`) - State checkpointing with MemorySaver for multi-turn conversations

## Notes

- All examples use TypedDict for type-safe state management
- State is passed between nodes and can be modified at each step
- Error handling is implemented in the stock price example
- The chatbot maintains conversation history for context-aware responses

## License

This is a sample project for educational purposes.
I would like thank Dhaval Patel for his support.
