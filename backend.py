# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup Pydantic Model (Schema Validation)
from pydantic import BaseModel
from typing import List


class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


#Step2: Setup AI Agent from FrontEnd Request
from fastapi import FastAPI
from ai_agent import get_response_from_ai_agent

# Only Groq models (free developer tier)
ALLOWED_MODEL_NAMES = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
]

app = FastAPI(title="LangGraph AI Agent")


@app.get("/")
def root():
    return {"status": "AI Agent backend is running!"}


@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API Endpoint to interact with the Chatbot using LangGraph and search tools.
    It dynamically selects the model specified in the request
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": f"Invalid model name. Choose from: {ALLOWED_MODEL_NAMES}"}

    llm_id = request.model_name
    query = request.messages[-1]
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    # Create AI Agent and get response
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    print("DEBUG FINAL RESPONSE:", response)
    return {"response": response}


#Step3: Run app & Explore Swagger UI Docs
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 9999))
    uvicorn.run(app, host="0.0.0.0", port=port)
