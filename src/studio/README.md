# Fresh Alert Agent - LangGraph Studio

This directory contains the LangGraph implementation of the Fresh Alert Agent.

## Setup

### 1. Install Dependencies

For LangGraph Studio development, you can install just the essential dependencies:

```bash
# Option 1: Install studio-specific requirements
pip install -r requirements.txt

# Option 2: Install the main project (includes all dependencies)
cd ../..
pip install -e .
```

### 2. Environment Variables

Create a `.env` file in this directory or set these environment variables:

```bash
# Required: Fresh Alert API
FRESH_ALERT_BEARER_TOKEN=your_bearer_token_here

# Required: LLM Provider (choose one)
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional: Recipe functionality
SPOONACULAR_API_KEY=your_spoonacular_api_key

# Optional: Environment setting
ENVIRONMENT=dev  # or 'prod'
```

### 3. Run with LangGraph Studio

```bash
# Start LangGraph Studio from this directory
langgraph dev

# Or specify the config explicitly
langgraph dev --config langgraph.json
```

### 4. Test the Agent

```bash
# Run from the project root
cd ../..
python test_agent.py

# Or run the interactive demo
python fresh_alert_demo.py --interactive
```

## Project Structure

```
src/studio/
├── freshalert_agent.py     # Main agent implementation
├── langgraph.json          # LangGraph Studio configuration
├── requirements.txt        # Studio-specific dependencies
├── config/                 # Agent configuration
│   ├── states.py          # State management
│   ├── models.py          # LLM integration
│   ├── prompts.py         # System prompts
│   ├── edges.py           # Workflow routing
│   └── nodes/             # Agent nodes
│       ├── conversation.py
│       ├── async_tool.py
│       ├── log_tool_call.py
│       └── summarize.py
└── README.md              # This file
```

## Agent Features

- **🍎 Food Inventory Management**: Track products and expiration dates
- **⏰ Proactive Alerts**: Get notified about expiring items
- **🍳 Recipe Suggestions**: Find recipes based on available ingredients
- **💬 Conversational Interface**: Natural language interaction
- **🔄 Memory Persistence**: Maintains conversation context
- **🛡️ Error Handling**: Graceful failure recovery

## API Integration

The agent integrates with:

- **Fresh Alert API**: Food tracking and expiration monitoring
- **Spoonacular API**: Recipe discovery and nutritional information
- **LLM Providers**: Groq, OpenAI, or Anthropic for conversation processing