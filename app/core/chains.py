from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.llm import create_chat_llm
from app.core.tools import get_all_tools
from app.core.memory import get_memory_for_session

def create_agent(session_id: str = None):
    """Create a LangChain agent with all available tools and memory"""
    # Get the LLM
    llm = create_chat_llm()
    
    # Get all tools
    tools = get_all_tools()
    
    # Create message list, starting with system message
    messages = [
        ("system", """You are an AI assistant for a payroll management application.
        You have access to various API endpoints to help users manage employees, 
        earning rates, and other payroll-related tasks.
        
        Use the available tools to respond to user queries accurately and efficiently.
        Always provide helpful and concise responses based on the data you retrieve.
        If you need to make multiple queries to answer a question, do so step by step.
        
        Remember important user information throughout the conversation.
        """)
    ]
    
    # Add chat history placeholder if we have a session
    if session_id:
        memory = get_memory_for_session(session_id)
        messages.append(MessagesPlaceholder(variable_name="chat_history"))
    else:
        memory = None
    
    # Add user input and agent scratchpad
    messages.append(("user", "{input}"))
    messages.append(MessagesPlaceholder(variable_name="agent_scratchpad"))
    
    # Create prompt from messages
    prompt = ChatPromptTemplate.from_messages(messages)
    
    # Create an agent with the tools
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create an agent executor with memory if available
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )
    
    return agent_executor

# Create the agent
agent = create_agent()