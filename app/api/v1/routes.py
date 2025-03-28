from fastapi import APIRouter, HTTPException
from app.core.chains import create_agent
from app.core.tool_validation import tool_registry
from app.core.memory import process_initial_message, get_user_context
from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse
from app.core.logging import DetailedLoggingCallbackHandler, logger
import uuid
import traceback

router = APIRouter(prefix="/llm", tags=["llm"])

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a natural language query using the AI agent.
    
    The agent will intelligently choose between direct LLM responses
    or using tools based on the query.
    """
    try:
        # Generate a session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Create a callback handler for this session
        callback_handler = DetailedLoggingCallbackHandler(session_id)
        
        # Log the incoming request
        logger.info(f"[{session_id}] Received query: {request.query}")
        
        # Reset tool registry for each new query
        tool_registry.reset()
        
        # Process the message to extract context
        process_initial_message(session_id, request.query)
        
        # Create agent with memory for this session
        agent = create_agent(session_id)
        
        # Run the agent with the query and callbacks
        response = agent.invoke(
            {"input": request.query},
            callbacks=[callback_handler]
        )
        
        # Log the final response
        logger.info(f"[{session_id}] Final response: {response['output']}")
        
        # Return the response with session ID
        return {"response": response["output"], "session_id": session_id}
    except Exception as e:
        # Log the full exception with traceback
        logger.error(f"Error processing query: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "message": "Agent is ready to process queries"}