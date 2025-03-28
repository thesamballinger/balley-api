from langchain.tools import tool
from app.core.memory import get_user_context
from typing import Optional

@tool
def get_current_user_id() -> Optional[int]:
    """Get the ID of the current user from conversation context."""
    from langchain.globals import get_llm_cache
    
    # Get the current session ID from the agent's context
    # This is a placeholder - in a real implementation, you'd need to pass the session ID
    session_id = get_llm_cache().get("current_session_id", "default_session")
    
    user_id = get_user_context(session_id, "user_id")
    if not user_id:
        return "Error: User ID not found in context"
    
    return user_id
