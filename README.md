# Fresh Alert Agent

A comprehensive AI-powered food management system that combines recipe discovery, food tracking, and expiration monitoring to help users reduce food waste and make informed meal planning decisions.

## Project Overview

The Fresh Alert Agent is an intelligent assistant that integrates multiple food-related APIs and services to provide users with:

- **Smart food tracking** with barcode scanning and expiration monitoring
- **Recipe discovery** based on available ingredients and dietary preferences
- **Food waste prevention** through proactive expiration alerts
- **Meal planning assistance** using expiring ingredients
- **Nutritional analysis** and dietary restriction support
- **Conversational AI interface** powered by LangGraph

## Architecture

### Core Components

#### 1. **Fresh Alert API Integration** (`src/utils/freshalert/`)
- **Purpose**: Track user products, expiration dates, and food freshness
- **Features**:
  - Product barcode scanning and lookup
  - Expiration date tracking with OCR
  - User-specific product management
  - Firebase push notifications
  - Image upload and processing
- **Endpoints Supported**:
  - `GET /product/user` - Get all user products
  - `GET /product/user/expired` - Get expired/expiring products

#### 2. **Spoonacular API Integration** (`src/utils/spoonacular/`)
- **Purpose**: Recipe discovery, nutritional analysis, and meal planning
- **Features**:
  - Complex recipe search with filtering
  - Detailed recipe information with instructions
  - Nutritional data and analysis
  - Ingredient substitutions
  - Wine pairing suggestions
  - Meal planning capabilities

#### 3. **MCP (Model Context Protocol) Tools** (`src/mcps/`)
- **Fresh Alert MCP** (`src/mcps/freshalert/`):
  - `fresh_alert_get_user_products()` - Retrieve user's food inventory
  - `fresh_alert_get_expired_products()` - Get expiring/expired items
- **Spoonacular MCP** (`src/mcps/spoonacular/`):
  - `spoonacular_complex_search()` - Advanced recipe search
  - `spoonacular_get_recipe()` - Detailed recipe information

#### 4. **LangGraph Studio Agent** (`src/studio/`)
- **Purpose**: Orchestrate AI conversations and decision-making
- **Components**:
  - State management for conversation context
  - Node definitions for agent actions
  - Edge configuration for workflow transitions
  - Model integration for LLM processing

## Features

### 🍽️ **Smart Food Management**
- **Product Tracking**: Automatic product identification via barcode scanning
- **Expiration Monitoring**: OCR-based date extraction from product images
- **Inventory Management**: Real-time tracking of product quantities and locations
- **Waste Prevention**: Proactive alerts for expiring items

### 🔍 **Intelligent Recipe Discovery**
- **Natural Language Search**: "gluten-free pasta under 30 minutes"
- **Ingredient-Based Matching**: Find recipes using available ingredients
- **Dietary Filtering**: Support for various diets and restrictions
- **Nutritional Analysis**: Detailed macro and micronutrient information

### 🤖 **Conversational AI Agent**
- **Context-Aware Responses**: Understands user preferences and inventory
- **Multi-Turn Conversations**: Maintains context across interactions
- **Personalized Recommendations**: Tailored suggestions based on user data
- **Integration Ready**: Works with chat UIs and voice interfaces

### 📱 **API Integration**
- **Authentication**: Secure Bearer token handling from request headers
- **Error Handling**: Comprehensive error management and recovery
- **Rate Limiting**: Automatic request throttling and retry logic
- **Type Safety**: Full Pydantic model validation

## Technology Stack

### **Backend & APIs**
- **Python 3.11+** - Core development language
- **AsyncIO** - Asynchronous programming for performance
- **HTTPx** - Modern async HTTP client
- **Pydantic** - Data validation and serialization
- **LangGraph** - AI agent orchestration framework

### **External APIs**
- **Fresh Alert API** - Food tracking and expiration monitoring
- **Spoonacular API** - Recipe and nutrition data
- **OpenAI/Anthropic** - LLM processing (via LangGraph)

### **Development Tools**
- **VS Code** - Primary development environment
- **Jupyter Notebooks** - Experimentation and analysis
- **Pytest** - Testing framework
- **Pre-commit** - Code quality and formatting

## Quick Start

### 1. Set Up Environment Variables

```bash
# Required: Fresh Alert API authentication
export FRESH_ALERT_BEARER_TOKEN="your_fresh_alert_bearer_token"

# Required: LLM API key (choose one)
export GROQ_API_KEY="your_groq_api_key"           # Recommended for development
export OPENAI_API_KEY="your_openai_api_key"       # Alternative option
export ANTHROPIC_API_KEY="your_anthropic_api_key" # Alternative option

# Optional: Recipe functionality
export SPOONACULAR_API_KEY="your_spoonacular_api_key"
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 3. Run the Agent

```bash
# Activate virtual environment
source .venv/bin/activate

# Run demo conversations
python fresh_alert_demo.py

# Run interactive mode
python fresh_alert_demo.py --interactive

# Run tests
python test_agent.py
```

### 4. LangGraph Studio

The agent is configured for LangGraph Studio:

```bash
# Start LangGraph Studio
langgraph dev

# Navigate to the studio interface
# Graph: fresh_alert_agent
```

### 5. Example Usage

```python
from src.studio.freshalert_agent import run_fresh_alert_agent

# Run a single conversation
response = await run_fresh_alert_agent(
    message="What items are expiring in the next 3 days?",
    bearer_token="your_fresh_alert_token",
    spoonacular_key="your_spoonacular_key",  # Optional
    thread_id="user_session_123"
)

print(response)
```

## Project Structure

```
fresh-alert-agent/
├── src/
│   ├── utils/                      # API Client Libraries
│   │   ├── freshalert/            # Fresh Alert API wrapper
│   │   │   ├── __init__.py        # Public API exports
│   │   │   ├── client.py          # Main FreshAlertClient
│   │   │   ├── base_client.py     # HTTP client with retries
│   │   │   ├── config.py          # Configuration management
│   │   │   ├── exceptions.py      # Custom exception classes
│   │   │   ├── models/            # Pydantic data models
│   │   │   ├── api/               # API endpoint modules
│   │   │   └── README.md          # Client documentation
│   │   └── spoonacular/           # Spoonacular API wrapper
│   │       ├── client.py          # Main SpoonacularClient
│   │       ├── base_client.py     # HTTP client foundation
│   │       ├── config.py          # API configuration
│   │       ├── models/            # Data models and enums
│   │       └── api/               # Endpoint implementations
│   ├── mcps/                      # MCP Tool Integrations
│   │   ├── freshalert/           # Fresh Alert MCP tools
│   │   │   ├── fresh_alert_mcp.py        # Core MCP tools
│   │   │   ├── test_fresh_alert_mcp.py   # Comprehensive tests
│   │   │   ├── fresh_alert_mcp_example.py # Usage examples
│   │   │   └── README.md                 # Tool documentation
│   │   └── spoonacular/          # Spoonacular MCP tools
│   │       ├── spoonacular_mcp.py        # Recipe search tools
│   │       ├── spoonacular_agent_tools.py # Formatted responses
│   │       └── test_spoonacular_tools.py  # Test suite
│   └── studio/                    # LangGraph Agent Implementation
│       ├── freshalert_agent.py    # Main agent definition
│       ├── langgraph.json         # LangGraph configuration
│       └── config/                # Agent configuration
│           ├── states.py          # State management
│           ├── models.py          # AI model configuration
│           ├── prompts.py         # Agent prompts
│           ├── edges.py           # Workflow transitions
│           └── nodes/             # Agent action nodes
├── freshalert_agent.ipynb         # Jupyter notebook for development
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Authentication & Security

### **Bearer Token Authentication**
The system uses Bearer tokens passed through request headers for secure API access:

```typescript
// Frontend (Chat UI)
const streamValue = useTypedStream({
  apiUrl: process.env.NEXT_PUBLIC_API_URL,
  assistantId: process.env.NEXT_PUBLIC_ASSISTANT_ID,
  defaultHeaders: {
    Authentication: `Bearer ${userToken}`, // User's authentication token
  },
});
```

```python
# Backend (LangGraph Agent)
def get_auth_token(config: RunnableConfig) -> str | None:
    """Extract authentication token from request headers"""
    configurable = config.get("configurable", {})
    headers = configurable.get("headers", {})
    auth_header = headers.get("Authentication")
    
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    return None

# Use in agent functions
async def agent_node(state: Dict[str, Any], config: RunnableConfig):
    token = get_auth_token(config)
    
    # Use with Fresh Alert tools
    products = await fresh_alert_get_user_products(token)
    expiring = await fresh_alert_get_expired_products(token, days=7)
```

## Getting Started

### **Prerequisites**
- Python 3.11 or higher
- Fresh Alert API access and Bearer token
- Spoonacular API key (optional, for recipe features)
- OpenAI or Anthropic API key (for LLM processing)

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fresh-alert-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables** (optional, for development):
   ```bash
   export FRESH_ALERT_BASE_URL="https://api.freshalert.com"
   export SPOONACULAR_API_KEY="your-spoonacular-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   ```

### **Usage Examples**

#### **Fresh Alert API Client**
```python
from src.utils.freshalert import FreshAlertClient, FreshAlertConfig

async def main():
    config = FreshAlertConfig(bearer_token="user-token-from-headers")
    
    async with FreshAlertClient(config) as client:
        # Get user's products
        products = await client.get_my_products()
        
        # Get products expiring soon
        expiring = await client.get_expiring_products(days=7)
```

#### **MCP Tools Integration**
```python
from src.mcps.freshalert import fresh_alert_get_user_products

# Direct tool usage (for LangGraph agents)
products = await fresh_alert_get_user_products(bearer_token)
print(f"Found {products['total_products']} products")
```

#### **Spoonacular Recipe Search**
```python
from src.mcps.spoonacular import spoonacular_complex_search

# Search for recipes
recipes = await spoonacular_complex_search(
    query="chicken curry",
    cuisine="indian",
    max_ready_time=45,
    number=5
)
```

## Use Cases

### **1. Food Waste Prevention**
- Monitor expiration dates across user's inventory
- Send proactive alerts for items expiring soon
- Suggest recipes to use expiring ingredients
- Track waste patterns and provide insights

### **2. Smart Meal Planning**
- Plan meals around available and expiring ingredients
- Consider dietary restrictions and preferences
- Optimize grocery shopping based on current inventory
- Generate shopping lists with smart recommendations

### **3. Recipe Discovery**
- Find recipes using available ingredients
- Filter by dietary needs and time constraints
- Get detailed nutritional information
- Discover new cuisines and cooking techniques

### **4. Inventory Management**
- Track product quantities and locations
- Monitor consumption patterns
- Automate reorder suggestions
- Maintain optimal stock levels

## API Endpoints

### **Fresh Alert API**
- `GET /product/user` - Retrieve all user products
- `GET /product/user/expired?days=7` - Get expiring products

### **Spoonacular API**
- Complex recipe search with advanced filtering
- Detailed recipe information with instructions
- Nutritional analysis and dietary compatibility
- Ingredient substitution suggestions

## Development

### **Testing**
```bash
# Test Fresh Alert MCP tools
cd src/mcps/freshalert
export FRESH_ALERT_BEARER_TOKEN="your-token"
python test_fresh_alert_mcp.py

# Test Spoonacular tools
cd src/mcps/spoonacular
export SPOONACULAR_API_KEY="your-key"
python test_spoonacular_tools.py
```

### **Running Examples**
```bash
# Fresh Alert examples
python src/mcps/freshalert/fresh_alert_mcp_example.py

# Spoonacular examples
python src/utils/spoonacular/spoonacular_examples.py
```

### **Jupyter Development**
```bash
# Start Jupyter for interactive development
jupyter notebook freshalert_agent.ipynb
```

## Contributing

1. **Code Structure**: Follow the established patterns in `src/utils/` and `src/mcps/`
2. **Testing**: Add comprehensive tests for new features
3. **Documentation**: Update README files and add docstrings
4. **Type Safety**: Use Pydantic models and type hints
5. **Error Handling**: Implement graceful error handling and logging

## License

This project is part of the Fresh Alert ecosystem for intelligent food management.

## Next Steps

- [ ] Implement the LangGraph agent in `src/studio/freshalert_agent.py`
- [ ] Add conversation state management
- [ ] Integrate both Fresh Alert and Spoonacular tools
- [ ] Add meal planning and waste prevention logic
- [ ] Create comprehensive agent testing suite
- [ ] Deploy and test with real chat UI integration