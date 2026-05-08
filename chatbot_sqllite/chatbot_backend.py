from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import sqlite3

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
) 


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
     messages = state['messages']
     response = model.invoke(messages)
     return {'messages':[response]}

#checkpoinetr
#it's work only single thread that's why assign False
conn = sqlite3.connect(database = 'chatbot.db', check_same_thread = False)

checkpointer = SqliteSaver(conn = conn)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    return sorted(list(all_threads), reverse=True)


def get_thread_title(thread_id):

    state = chatbot.get_state(
    config={
        'configurable': {
            'thread_id': thread_id
        }
    }
)

    messages = state.values.get('messages', [])

    for msg in messages:

        if msg.type == "human":
            return msg.content[:30]

    return "New Chat"
          

