import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Set your OpenAI API key

load_dotenv()  # load variables from .env file
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful medical assistant chatbot."}
    ]

# Streamlit App Layout
st.title("Healthcare AI Chatbot 💬 (GPT-3.5 Version)")
st.write("Ask your medical questions below:")

# User Input Form
with st.form(key="ask_form"):
    user_input = st.text_input("Enter your question:")
    ask_button = st.form_submit_button("Ask")

if ask_button:
    if user_input.strip() != "":
        # Add User's Message to Chat History
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get GPT-3.5 Response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.2,
            max_tokens=250,
        )

        bot_reply = response.choices[0].message.content

        # Add Bot's Reply to Chat History
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    else:
        st.warning("Please enter a question!")

# Reset Chat Button (Separate)
if st.button("Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful medical assistant chatbot."}
    ]
    st.success("Chat history has been cleared! Start fresh now.")

# Display Chat History
if len(st.session_state.messages) > 1:
    st.markdown("---")
    st.subheader("🧵 Chat History:")

    for msg in st.session_state.messages[1:]:  # Skip system message
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div style='background-color:#DCF8C6;padding:10px;border-radius:10px;margin-bottom:5px;width:fit-content;'>
                <b>🧑 You:</b> {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='background-color:#F1F0F0;padding:10px;border-radius:10px;margin-bottom:5px;width:fit-content;'>
                <b>🤖 AI:</b> {msg['content']}
                </div>
                """,
                unsafe_allow_html=True,
            )
