from openai import OpenAI
import streamlit as st
import google.generativeai as genai
import anthropic

with st.sidebar:
    provider = st.selectbox(
        "Select LLM Provider",
        options=["OpenAI", "Gemini", "Claude"],
        key="llm_provider"
    )
    if provider == "OpenAI":
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    elif provider == "Gemini":
        gemini_api_key = st.text_input("Gemini API Key", key="gemini_api_key", type="password")
        "[Get a Gemini API key](https://aistudio.google.com/app/apikey)"
    elif provider == "Claude":
        claude_api_key = st.text_input("Claude API Key", key="claude_api_key", type="password")
        "[Get a Claude API key](https://console.anthropic.com/settings/keys)"

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if provider == "OpenAI":
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    elif provider == "Gemini":
        if not gemini_api_key:
            st.info("Please add your Gemini API key to continue.")
            st.stop()
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        gemini_messages = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages
        ]
        response = model.generate_content(gemini_messages)
        msg = response.text
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    elif provider == "Claude":
        if not claude_api_key:
            st.info("Please add your Claude API key to continue.")
            st.stop()
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        client = anthropic.Anthropic(api_key=claude_api_key)
        claude_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=claude_messages
        )
        msg = response.content[0].text
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)