import streamlit as st
import openai
from openai import AuthenticationError, RateLimitError

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# Sidebar for API key and system prompt
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
system_prompt = st.sidebar.text_area("System Prompt", value="You are a helpful assistant.", height=100)

# Button to reset chat
if st.sidebar.button("Reset Chat"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Chat input
user_input = st.text_input("Type your message and press Enter:", key="user_input")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("Bot is typing..."):
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            bot_message = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": bot_message})
        except AuthenticationError:
            st.error("Invalid API key. Please check your key in the sidebar.")
        except RateLimitError:
            st.error("Rate limit exceeded or insufficient quota. Check your OpenAI account.")
        except Exception as e:
            st.error(f"Error: {e}")
    st.rerun()  # This will clear the input box after sending

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Bot:** {msg['content']}")


