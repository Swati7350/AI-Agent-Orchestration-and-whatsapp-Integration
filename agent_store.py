import json
import os

FILE = "agents.json"
CHAT_HISTORY_FILE = "chat_history.json"


# =====================================
# CHAT HISTORY
# =====================================
def save_chat_history(chats):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(chats, f, indent=4)


def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    return {}


# =====================================
# AGENTS
# =====================================
def load_agents():
    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r") as f:
        return json.load(f)


def save_agent(agent_data):
    agents = load_agents()

    agents[agent_data["name"]] = {
        "model_name": agent_data["model_name"],
        "model_provider": agent_data["model_provider"],
        "system_prompt": agent_data["system_prompt"],
        "allow_search": agent_data["allow_search"]
    }

    with open(FILE, "w") as f:
        json.dump(agents, f, indent=4)


def save_all_agents(agents):
    with open(FILE, "w") as f:
        json.dump(agents, f, indent=4)


def get_agent(name):
    agents = load_agents()
    return agents.get(name)


# =====================================
# ROUTING
# =====================================
def route_agent(query: str, llm, agents: dict):

    router_prompt = f"""
You are an intelligent router.

Your job is to select the MOST suitable agent from the available list.

AVAILABLE AGENTS:
{list(agents.keys())}

RULES:
- Choose ONLY from the agent names above
- Understand intent
- Return ONLY the agent name
- No explanation

User query:
{query}
"""

    response = llm.invoke(router_prompt)

    agent_name = response.content.strip()

    # fallback safety
    if agent_name not in agents:
        agent_name = list(agents.keys())[0]

    return agent_name


# =====================================
# RUN AGENT
# =====================================
def run_agent(agent, user_input, llm, chat_history=None):

    messages = [
        {
            "role": "system",
            "content": agent["system_prompt"]
        }
    ]

    # add previous conversation
    if chat_history:
        messages.extend(chat_history)

    # current user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    response = llm.invoke(messages)

    return response.content