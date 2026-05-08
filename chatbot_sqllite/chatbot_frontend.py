import streamlit as st
from chatbot_backend import (
    chatbot,
    retrieve_all_threads,
    get_thread_title
)

from langchain_core.messages import HumanMessage
import uuid


# -------------------------------- Utility --------------------------------

def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():

    st.session_state['thread_id'] = generate_thread_id()


def load_conversation(thread_id):

    state = chatbot.get_state(
        config={
            'configurable': {
                'thread_id': thread_id
            }
        }
    )

    return state.values.get('messages', [])


# -------------------------------- Session Setup --------------------------------

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()


# -------------------------------- Sidebar --------------------------------

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")


all_threads = retrieve_all_threads()

for thread_id in all_threads:

    title = get_thread_title(thread_id)

    if st.sidebar.button(title):

        st.session_state['thread_id'] = thread_id

        st.rerun()


# -------------------------------- Main Chat UI --------------------------------

messages = load_conversation(
    st.session_state['thread_id']
)

for msg in messages:

    if isinstance(msg, HumanMessage):
        role = "user"
    else:
        role = "assistant"

    with st.chat_message(role):
        st.text(msg.content)


# -------------------------------- User Input --------------------------------

user_input = st.chat_input("Type Here...")


if user_input:

    with st.chat_message("user"):
        st.text(user_input)

    CONFIG = {
        'configurable': {
            'thread_id': st.session_state['thread_id']
        }
    }

    with st.chat_message("assistant"):

        st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {
                    'messages': [
                        HumanMessage(content=user_input)
                    ]
                },
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.rerun()