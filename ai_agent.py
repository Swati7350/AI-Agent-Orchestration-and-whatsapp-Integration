# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup API Keys for Groq, OpenAI and Tavily
import os
from pyexpat.errors import messages
from langchain_core import messages
from urllib import response
from langchain_core.messages import HumanMessage

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")

#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
#from langchain_tavily import TavilySearch

openai_llm=ChatOpenAI(model="gpt-4o-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

#Step3: Setup AI Agent with Search tool functionality
#from langchain import create_react_agent
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage


# search_tool = TavilySearchResults(max_results=2)

# DEFAULT_SYSTEM_PROMPT = "Act as an AI chatbot who is smart and friendly"

# # Agent
# agent = create_react_agent(
#     model=groq_llm,
#     tools=[search_tool], 
#     state_modifier=DEFAULT_SYSTEM_PROMPT
# )

# query = "Tell me about crypto markets"

# state = {
#     "messages": [HumanMessage(content=query)] 
# }

# response = agent.invoke(state)

# print(response)
def get_response_from_ai_agent(llm_id, query, allow_search, DEFAULT_SYSTEM_PROMPT, provider):
    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model=llm_id)

    search_tool = (
        [TavilySearchResults(max_results=2)] if allow_search else []
    )

    agent = create_react_agent(
        model=llm,
        tools=search_tool,
        state_modifier=DEFAULT_SYSTEM_PROMPT
    )

    state = {
        "messages": [HumanMessage(content=query)]
    }

    response = agent.invoke(state)
    #print("DEBUG RESPONSE:", response)
    messages = response.get("messages", [])
    message = messages[-1] if messages else None
    print("DEBUG MESSAGE:",message.content)
    return message.content if message else None


#get_response_from_ai_agent("llama-3.3-70b-versatile", "what is the capital of France?", False, "Act as helpful AI", "Groq")