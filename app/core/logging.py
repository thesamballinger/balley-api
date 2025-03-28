import logging
from typing import Dict, Any, List, Optional
from langchain.callbacks.base import BaseCallbackHandler
import json
import traceback
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("agent_logs.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("agent")

class DetailedLoggingCallbackHandler(BaseCallbackHandler):
    """Callback handler for logging detailed information about agent execution."""
    
    def __init__(self, session_id: str):
        """Initialize with session ID for tracking."""
        self.session_id = session_id
        self.start_time = None
        self.steps = []
        
    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Log when a chain starts."""
        chain_type = serialized.get("name", "Unknown Chain")
        logger.info(f"[{self.session_id}] Starting {chain_type}")
        logger.info(f"[{self.session_id}] Inputs: {json.dumps(inputs, default=str)}")
        self.start_time = time.time()
    
    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Log when a chain ends."""
        duration = time.time() - self.start_time if self.start_time else 0
        logger.info(f"[{self.session_id}] Chain completed in {duration:.2f}s")
        logger.info(f"[{self.session_id}] Outputs: {json.dumps(outputs, default=str)}")
    
    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Log when a chain errors."""
        logger.error(f"[{self.session_id}] Chain error: {str(error)}")
        logger.error(f"[{self.session_id}] Traceback: {traceback.format_exc()}")
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> None:
        """Log when a tool starts."""
        tool_name = serialized.get("name", "Unknown Tool")
        logger.info(f"[{self.session_id}] Starting tool: {tool_name}")
        logger.info(f"[{self.session_id}] Tool input: {input_str}")
    
    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Log when a tool ends."""
        logger.info(f"[{self.session_id}] Tool output: {output}")
        self.steps.append({"type": "tool", "output": output})
    
    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Log when a tool errors."""
        logger.error(f"[{self.session_id}] Tool error: {str(error)}")
        logger.error(f"[{self.session_id}] Traceback: {traceback.format_exc()}")
        self.steps.append({"type": "tool_error", "error": str(error)})
    
    def on_text(self, text: str, **kwargs: Any) -> None:
        """Log when text is generated."""
        logger.info(f"[{self.session_id}] Generated text: {text}")
        self.steps.append({"type": "text", "content": text})
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> None:
        """Log when LLM starts."""
        llm_name = serialized.get("name", "Unknown LLM")
        logger.info(f"[{self.session_id}] Starting LLM: {llm_name}")
        for i, prompt in enumerate(prompts):
            logger.info(f"[{self.session_id}] Prompt {i+1}: {prompt}")
    
    def on_llm_end(self, response, **kwargs: Any) -> None:
        """Log when LLM ends."""
        logger.info(f"[{self.session_id}] LLM response: {response}")
