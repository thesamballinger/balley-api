import functools
from typing import Dict, List, Callable, Any, Optional
import logging
import traceback

logger = logging.getLogger("agent.tool_validation")

class ToolRegistry:
    """Registry to track tool dependencies and execution context."""
    
    def __init__(self):
        # Define which tools require other tools to be called first
        self.tool_dependencies = {
            "send_tenant_invites": ["get_current_leases_by_landlord_id"],
            "update_maintenance_request": ["get_maintenance_requests"],
            "submit_landlord_review": ["get_landlord_by_id"],
            # Add other dependencies as needed
        }
        
        # Track which tools have been executed in the current session
        self.execution_history = []
        
        self.reset()
    
    def validate_tool_execution(self, tool_name: str) -> bool:
        """Check if a tool can be executed based on previous tool calls."""
        if tool_name not in self.tool_dependencies:
            return True  # No dependencies
            
        required_tools = self.tool_dependencies[tool_name]
        for req_tool in required_tools:
            if req_tool not in self.execution_history:
                return False
                
        return True
        
    def record_execution(self, tool_name: str):
        """Record that a tool was executed."""
        self.execution_history.append(tool_name)
        
    def reset(self):
        """Reset execution history and tool calls."""
        self.execution_history = []
        self.tool_calls = {}
        self.validation_errors = {}
    
    def register_tool_call(self, tool_name: str, args: Dict[str, Any]):
        """Register a tool call with its arguments."""
        if tool_name not in self.tool_calls:
            self.tool_calls[tool_name] = []
        
        self.tool_calls[tool_name].append(args)
        logger.info(f"Tool call registered: {tool_name} with args {args}")
    
    def register_validation_error(self, tool_name: str, error: str, args: Dict[str, Any]):
        """Register a validation error for a tool call."""
        if tool_name not in self.validation_errors:
            self.validation_errors[tool_name] = []
        
        self.validation_errors[tool_name].append({"error": error, "args": args})
        logger.error(f"Validation error for {tool_name}: {error} with args {args}")
    
    def get_tool_calls(self, tool_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tool calls or calls for a specific tool."""
        if tool_name:
            return {tool_name: self.tool_calls.get(tool_name, [])}
        return self.tool_calls
    
    def get_validation_errors(self, tool_name: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Get all validation errors or errors for a specific tool."""
        if tool_name:
            return {tool_name: self.validation_errors.get(tool_name, [])}
        return self.validation_errors

# Global registry instance
tool_registry = ToolRegistry()

def validate_parameters(func):
    """Decorator to validate parameters before executing a tool."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if any required parameters are empty
        empty_params = []
        for param_name, param_value in kwargs.items():
            if param_value is None or (isinstance(param_value, (list, dict, str)) and len(param_value) == 0):
                empty_params.append(param_name)
        
        if empty_params:
            return f"Error: Missing required parameters: {', '.join(empty_params)}. Please provide values for these parameters."
        
        return func(*args, **kwargs)
    
    return wrapper

def requires_tools(required_tools: List[str]):
    """Decorator to enforce tool dependencies."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for tool in required_tools:
                if tool not in tool_registry.execution_history:
                    return f"Error: Before using {func.__name__}, you must first call: {tool}"
            
            tool_registry.record_execution(func.__name__)
            return func(*args, **kwargs)
        return wrapper
    return decorator
