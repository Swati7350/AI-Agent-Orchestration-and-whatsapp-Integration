# if you dont use pipenv uncomment the following:
import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq

from agent_store import (
    save_agent,
    load_agents,
    route_agent,
    run_agent,
    save_all_agents,
    load_chat_history,
    save_chat_history
)
# ===================================
# PAGE CONFIG
# ===================================
st.set_page_config(
    page_title="LangGraph Agent UI",
    layout="wide"
)
# ===================================
# NEW CHAT
# ===================================
def create_new_chat():
    chat_id = f"chat_{len(st.session_state.chats) + 1}"
    st.session_state.chats[chat_id] = []
    st.session_state.current_chat = chat_id

def switch_chat(chat_id):
    st.session_state.current_chat = chat_id
    st.session_state.active_agent = None
# ===================================
# SESSION STATE
# ===================================

if "agents" not in st.session_state:
    st.session_state.agents = load_agents()

if "show_agents" not in st.session_state:
    st.session_state.show_agents = False

if "show_manage_agents" not in st.session_state:
    st.session_state.show_manage_agents = False

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

if "active_agent" not in st.session_state:
    st.session_state.active_agent = None

if "show_whatsapp" not in st.session_state:
    st.session_state.show_whatsapp = False

if "chats" not in st.session_state:
    st.session_state.chats = load_chat_history()

if not isinstance(st.session_state.chats, dict):
    st.session_state.chats = {}

if "current_chat" not in st.session_state:

    if st.session_state.chats:
        # always open latest chat
        latest_chat = list(
            st.session_state.chats.keys()
        )[-1]

        st.session_state.current_chat = (
            latest_chat
        )

    else:
        st.session_state.current_chat = (
            "chat_1"
        )

if "chat_1" not in st.session_state.chats:
    st.session_state.chats["chat_1"] = []
# ===================================
# SIDEBAR → VIEW AGENTS
# ===================================
with st.sidebar:

    if st.button("📂 View All Agents"):
        st.session_state.show_agents = (
            not st.session_state.show_agents
        )

    if st.session_state.show_agents:

        agents = st.session_state.agents

        if not agents:
            st.info("No agents found.")

        else:
            for name, config in agents.items():

                with st.expander(f"🤖 {name}"):

                    st.write(
                        f"**Model:** "
                        f"{config['model_name']}"
                    )

                    st.write(
                        f"**Provider:** "
                        f"{config['model_provider']}"
                    )

                    st.write(
                        f"**Search:** "
                        f"{config['allow_search']}"
                    )

                    st.write("**Prompt:**")

                    st.text_area(
                        "Prompt",
                        value=config["system_prompt"],
                        height=120,
                        disabled=True,
                        key=f"prompt_{name}"
                    )


# ===================================
# SIDEBAR → MANAGE AGENTS
# ===================================
with st.sidebar:

    if st.button("⚙️ Manage Agents"):
        st.session_state.show_manage_agents = (
            not st.session_state.show_manage_agents
        )

    if st.session_state.show_manage_agents:

        action = st.selectbox(
            "Action",
            ["Edit Agent", "Delete Agent"]
        )

        agents = st.session_state.agents

        # ---------------- EDIT ----------------
        if action == "Edit Agent":

            agent_name = st.selectbox(
                "Select Agent",
                list(agents.keys())
            )

            model = st.text_input(
                "Model Name",
                agents[agent_name]["model_name"]
            )

            provider = st.text_input(
                "Provider",
                agents[agent_name]["model_provider"]
            )

            prompt = st.text_area(
                "System Prompt",
                agents[agent_name]["system_prompt"]
            )

            if st.button("💾 Update"):

                agents[agent_name][
                    "model_name"
                ] = model

                agents[agent_name][
                    "model_provider"
                ] = provider

                agents[agent_name][
                    "system_prompt"
                ] = prompt

                st.session_state.agents = (
                    agents
                )

                save_agent({
                    "name": agent_name,
                    **agents[agent_name]
                })

                st.success(
                    f"Agent '{agent_name}' updated!"
                )

        # ---------------- DELETE ----------------
        elif action == "Delete Agent":

            agent_name = st.selectbox(
                "Select Agent to Delete",
                list(agents.keys())
            )

            if st.button("🗑️ Delete"):

                del agents[agent_name]

                st.session_state.agents = (
                    agents
                )

                save_all_agents(agents)

                st.success(
                    f"Agent '{agent_name}' deleted!"
                )

# ===================================
# SIDEBAR → CONTACT
# ===================================
with st.sidebar:
    st.divider()
    st.markdown("### 👩‍💻 About the Developer")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            "assets/Gemini_Generated_Image_t2wcwpt2wcwpt2wc.png",
            width=60
        )
    with col2:
        st.markdown("**Swati Gupta**")
        st.markdown("🤖 AI | ML | Agentic AI Developer")

    st.markdown(
        "📧 [swati.3999@gmail.com](mailto:swati.3999@gmail.com)"
    )
    st.markdown(
        "🐙 [GitHub](https://github.com/Swati7350)"
    )


# ===================================
# MAIN LAYOUT
# ===================================
left_col, right_col = st.columns([6, 4])


# ===================================
# LEFT → CREATE AGENT
# ===================================
with left_col:

    st.title("AI Chatbot Agents")
    st.write(
        "Create and Interact with AI Agents!"
    )

    agent_name = st.text_input(
        "Agent Name"
    )

    system_prompt = st.text_area(
        "Define your AI System Prompt:",
        height=100
    )

    MODEL_NAMES_GROQ = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
    ]

    provider = st.radio(
        "Select Provider:",
        ("Groq",)
    )

    selected_model = st.selectbox(
        "Select Groq Model:",
        MODEL_NAMES_GROQ
    )

    allow_web_search = st.checkbox(
        "Allow Web Search"
    )

    spacer, button_col = st.columns([3, 2])

    with button_col:

        if st.button(
            "💾 Save Agent",
            use_container_width=True
        ):

            if agent_name.strip():

                agent_data = {
                    "name": agent_name,
                    "model_name":
                        selected_model,
                    "model_provider":
                        provider,
                    "system_prompt":
                        system_prompt,
                    "allow_search":
                        allow_web_search
                }

                save_agent(agent_data)

                # refresh session
                st.session_state.agents = (
                    load_agents()
                )

                st.success(
                    "Agent saved!"
                )

            else:
                st.error(
                    "Enter agent name"
                )

    # ===================================
    # 📲 SHARE DISCUSSION
    # ===================================
    st.divider()

    st.markdown("### 📲 Share Discussion")

    st.info(
        "Send your finalized details to WhatsApp.\n\n"
        "✔ Enter 10-digit mobile number (India)\n\n"
        "✔ Or include country code (+91XXXXXXXXXX)\n\n"
        "✔ Click send to receive your discussion instantly"
    )

    phone = st.text_input(
        "WhatsApp Number",
        placeholder="9876543210"
    )

    if phone.strip():
        itinerary = None
        messages = st.session_state.chats[st.session_state.current_chat]
        if isinstance(messages, list):
            for msg in reversed(messages):
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    itinerary = msg.get("content")
                    break

        if itinerary:
            import urllib.parse
            clean_phone = phone.strip().replace(" ", "").replace("-", "")
            if not clean_phone.startswith("+"):
                if len(clean_phone) == 10:
                    clean_phone = "91" + clean_phone
            else:
                clean_phone = clean_phone.lstrip("+")

            encoded_msg = urllib.parse.quote(itinerary[:1000])
            whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"

            st.markdown(
                f'<a href="{whatsapp_url}" target="_blank">'
                f'<button style="background-color:#25D366;color:white;'
                f'border:none;padding:10px 20px;border-radius:5px;'
                f'font-size:16px;cursor:pointer;display:flex;align-items:center;gap:8px;">'
                f'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white">'
                f'<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>'
                f'<path d="M12 0C5.373 0 0 5.373 0 12c0 2.127.558 4.126 1.532 5.862L.057 23.428a.75.75 0 00.921.921l5.569-1.474A11.942 11.942 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.891 0-3.666-.5-5.198-1.377l-.372-.215-3.304.875.876-3.307-.234-.385A9.956 9.956 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/>'
                f'</svg>'
                f' Open WhatsApp & Send</button></a>',
                unsafe_allow_html=True
            )
        else:
            st.caption("Chat with an agent first, then share the response via WhatsApp.")

def toggle_chats():
    st.session_state.show_chats = (
        not st.session_state.show_chats
    )
# ===================================
# RIGHT → CHAT
# ===================================
with right_col:
    
    header_left, header_right = st.columns([5, 3])

    with header_right:
        st.button("➕ New Chat", on_click=create_new_chat)
        st.button(
                "📂 View Chat History",
                on_click=toggle_chats
            )
        if "show_chats" not in st.session_state:
            st.session_state.show_chats = False
        if st.session_state.show_chats:

                chat_ids = list(st.session_state.chats.keys())[-5:]

                for chat_id in reversed(chat_ids):

                    is_active = chat_id == st.session_state.current_chat
                    label = f"👉 {chat_id}"

                    st.button(
                        label,
                        key=f"chat_{chat_id}",
                        on_click=switch_chat,
                        args=(chat_id,),
                        use_container_width=True
                    )
    st.subheader(
        "💬 Chat With Agent"
    )
    
    current_chat = st.session_state.current_chat
    if current_chat not in st.session_state.chats:
        st.session_state.chats[current_chat] = []

    for msg in st.session_state.chats[current_chat]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


    user_message = st.chat_input(
        "e.g. Help me with travel plans from Delhi to Rishikesh"
    )
    
    if user_message:

        # 1. store user message
        st.session_state.chats[current_chat].append({
            "role": "user",
            "content": user_message
        })
        llm = ChatGroq(
            model="openai/gpt-oss-20b"
        )

        agents = st.session_state.agents

        if st.session_state.active_agent is None:

            agent_name = route_agent(user_message, llm, agents)

            if agent_name is None or agent_name not in agents:

                st.warning("⚠️ No related agent found for your query.")

                st.session_state.chats[st.session_state.current_chat].append({
                    "role": "assistant",
                    "content": "⚠️ Sorry, no suitable agent found for your request. Please create an agent or refine your query."
                })

                st.rerun()

            st.session_state.active_agent = (
                agent_name
            )

        agent = agents[
            st.session_state.active_agent
        ]
    # 3. generate response
        response = run_agent(
            agent,
            user_message,
            llm,
            st.session_state.chats[current_chat]
        )
         # 4. store assistant message
        st.session_state.chats[current_chat].append({
            "role": "assistant",
            "content": response
        })
        save_chat_history(st.session_state.chats)
        # trigger whatsapp UI
        if "whatsapp" in response.lower():
            st.session_state.show_whatsapp = True

        st.rerun()
