# from app.core.tools.api_tools import get_api_tools
# from app.core.tools.db_tools import get_db_tools

def get_all_tools():
    """Return all available tools for the LLM to use"""
    tools = []
    # tools.extend(get_api_tools())
    # tools.extend(get_db_tools())
    return tools
