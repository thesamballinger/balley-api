from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict, Any, List, Optional
import uuid
import re

# Dictionary to store conversation memories by session ID
session_memories = {}
# Dictionary to store user context by session ID
user_context = {}

def get_memory_for_session(session_id: str):
    """Get or create a memory instance for a specific session"""
    if session_id not in session_memories:
        session_memories[session_id] = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
    return session_memories[session_id]

def set_user_context(session_id: str, key: str, value: Any):
    """Store context information for a user session"""
    if session_id not in user_context:
        user_context[session_id] = {}
    user_context[session_id][key] = value

def get_user_context(session_id: str, key: str, default=None) -> Any:
    """Retrieve context information for a user session"""
    if session_id not in user_context:
        return default
    return user_context[session_id].get(key, default)

def extract_user_id_from_query(query: str) -> Optional[int]:
    """Extract user ID from a query string"""
    # Look for patterns like "USER ID 123" or "user id is 123"
    patterns = [
        r"USER ID (\d+)",
        r"user id (\d+)",
        r"user id is (\d+)",
        r"landlord with id (\d+)",
        r"landlord id (\d+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None

def process_initial_message(session_id: str, message: str):
    """Process an initial message to extract context information"""
    # This is a placeholder for any preprocessing you might want to do
    pass
