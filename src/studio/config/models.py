import os
from typing import TypedDict, List, Callable, Optional, Dict, Any

from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig




class ModelConfig(TypedDict):
    provider: str
    model_name: str


def get_model(model_config: ModelConfig = None):
    """
    Get the appropriate LLM model based on configuration.

    Args:
        model_config: Optional model configuration with provider and model_name

    Returns:
        Configured LLM instance
    """

    env = os.getenv("ENVIRONMENT", "dev").lower()

    # Always create new model based on config (no global caching)
    if not model_config:
        if env == "prod":
            model_name = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
            return ChatAnthropic(model=model_name, temperature=0)
        else:
            model_name = os.getenv("OPENAI_MODEL", "gpt-5-mini")
            return ChatOpenAI(model=model_name, temperature=0)

    # Create model based on user selection
    provider = model_config.get("provider", "groq")
    model_name = model_config.get("model_name", "llama-3.1-8b-instant")

    if provider == "anthropic":
        return ChatAnthropic(model=model_name, temperature=0)

    if provider == "openai":
        return ChatOpenAI(model=model_name, temperature=0)

    return ChatGroq(model=model_name, temperature=0)


async def get_tools(config: Optional[RunnableConfig] = None) -> List:
    """
    Get all available tools for the agent with dynamic authentication.

    Args:
        config: RunnableConfig containing authentication tokens

    Returns:
        List of available tools
    """

    fresh_alert_mcp_url = os.getenv("FRESH_ALERT_MCP", "")
    spoonacular_mcp_url = os.getenv("SPOONACULAR_MCP", "")

    fresh_alert_token = ""
    headers = {}
    
    # print("config: ", config)
    
    if config and "configurable" in config:
        
        configurable = config.get("configurable", {})
    
        fresh_alert_token = configurable.get("freshalert-token")
        
        # user_config = config["configurable"].get("langgraph_auth_user", {})
        
        # fresh_alert_token = user_config.get("freshalert-token", "")
        
        headers = {"authorization": f"{fresh_alert_token}"}        

    client = MultiServerMCPClient(
        {
            "fresh_alert_mcp": {
                "transport": "streamable_http",
                "url": fresh_alert_mcp_url,
                "headers": headers,
            },
            "spoonacular_mcp": {
                "url": spoonacular_mcp_url,
                "transport": "streamable_http",
            },
        }
    )

    return await client.get_tools()
