from langchain_openai import OpenAI, ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.config import get_settings
from app.core.tools import get_all_tools

settings = get_settings()

def create_llm():
    """Return a basic OpenAI LLM instance without tools"""
    return OpenAI(api_key=settings.openai_api_key, model=settings.default_model)

def create_chat_llm():
    """Return a ChatOpenAI instance for use with agents"""
    return ChatOpenAI(
        api_key=settings.openai_api_key,
        model=settings.default_model,
        temperature=0.2,
        streaming=True
    )

def get_llm_with_tools():
    """Return an LLM with tools for API interaction"""
    # Use ChatOpenAI for tools support
    llm = create_chat_llm()
    
    # Get all available tools
    tools = get_all_tools()
    
    # Create a prompt template with agent_scratchpad
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI assistant for a payroll management application.
        You have access to various API endpoints to help users manage employees, 
        earning rates, and other payroll-related tasks.
        Use the available tools to respond to user queries accurately and efficiently.
        Always provide helpful and concise responses."""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    # Create an agent with the tools
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create an agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def process_question(question: str):
    """Process a question using the LLM"""
    llm = create_llm()
    return llm.invoke(question)

# For backward compatibility
def get_llm(question: str = None):
    """
    Backward compatibility function.
    If called with a question, processes the question.
    If called without arguments, returns a basic LLM instance.
    """
    if question is not None:
        return process_question(question)
    return create_llm()