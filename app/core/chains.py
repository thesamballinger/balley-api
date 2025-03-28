from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.core.llm import create_chat_llm
from app.core.tools import get_all_tools
from app.core.tool_validation import tool_registry
from app.core.memory import get_memory_for_session

def create_agent(session_id: str = None):
    """Create a LangChain agent with all available tools and memory"""
    # Get the LLM
    llm = create_chat_llm()
    
    # Get all tools
    tools = get_all_tools()
    
    # Create message list, starting with system message
    messages = [
        ("system", """You are an AI assistant for a property management application called Dwelio. 
        You have access to various API endpoints and database queries to help users manage properties, 
        tenants, payments, maintenance requests, and more.
        
        IMPORTANT: When executing functions, ALWAYS follow these steps in order:
        1. THINK: Identify what information you need to complete the task
        2. GATHER: Use appropriate query tools to retrieve necessary data
        3. VALIDATE: Ensure you have all required parameters for the function
        4. EXECUTE: Only then call the action function with complete parameters
        
        Never call action functions with empty parameters. Always gather context first.
        
        DATABASE SCHEMA AWARENESS:
        - Properties are linked to landlords via property.landlord_id
        - Tenants are linked to properties via leases (leaseinfo table)
        - To find all tenants for a landlord, first get the landlord's properties, then get leases for those properties
        - Maintenance requests are linked to properties via maintenance.property_id
        - Payments are linked to leases via payment.lease_id
        
        For example, if asked to "remind tenants to pay rent":
        - First use get_current_leases_by_landlord_id to retrieve lease information including tenant IDs
        - Extract tenant IDs from the lease data
        - Then use send_tenant_invites with the specific tenant IDs and a payment reminder message
        
        Use the available tools to respond to user queries accurately and efficiently.
        For database queries, use the db_tools.
        For API calls to external services, use the api_tools.
        For financial operations, use the financial_tools.
        
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