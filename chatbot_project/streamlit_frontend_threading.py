import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#---------------------------------------Utility methods---------------------------------------------------------------
def generate_thread_id():
    """
    This fxn give random new thread_id for each new conversation. 
    """
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    """
    This genearte a thread_id and then replace old thread_id, and also reset the chat history.
    """
    thread_id = generate_thread_id()  
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []


def add_thread(thread_id, title = 'New Chat'):
    """ This method add the thread_id in chat_threads if that thread_id not available in chat_threads"""
    if  thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'][thread_id] = title



def load_conversation(thread_id):
    return chatbot.get_state(config = {'configurable': {'thread_id': thread_id}}).values['messages']

# ----------------------------------------------Session Setup--------------------------------------------------------

# st.session_state -> dict -> not erase after enter to run each time
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = {}


#---------------------------------------Sidebar UI-------------------------------------------------------------------

st.sidebar.title('LangGraph_chatbot')   #Title show when open browser

if st.sidebar.button('New Chat'):       #button come for new chat
    reset_chat()          

st.sidebar.header('My Conversation')    #All old conversation show inside my conversation


for thread_id, title in reversed(list(st.session_state['chat_threads'].items())):
    if st.sidebar.button(title):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)              #Each old conversation show their thread_id

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})
        
        st.session_state['message_history'] = temp_messages

#-----------------------------------------MAIN UI--------------------------------------------------------------------

# Loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input('Typed Here: ')

if user_input:
    # first add the message in history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    
    # create title from first message
    if len(st.session_state['message_history']) == 1:

        title = user_input[:30]

        add_thread(st.session_state['thread_id'], title)
    CONFIG = {'configurable':{'thread_id': st.session_state['thread_id']}}
    
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {'messages': [HumanMessage(content = user_input)]},
              config = CONFIG,
              stream_mode = 'messages'
               )
        )

    st.session_state['message_history'].append({'role':'assistant', 'content': ai_message})