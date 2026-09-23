# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup API Keys for Groq and Tavily
import os
from langchain_core import messages
from langchain_core.messages import HumanMessage

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

#Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage


def get_response_from_ai_agent(llm_id, query, allow_search, DEFAULT_SYSTEM_PROMPT, provider):
    # Always use Groq regardless of provider
    llm = ChatGroq(model=llm_id)

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
    messages = response.get("messages", [])
    message = messages[-1] if messages else None
    print("DEBUG MESSAGE:", message.content if message else "No message")
    return message.content if message else None
