# LangGraph Streamlit Chatbot

A multi-threaded AI chatbot built using:

* Streamlit
* LangGraph
* LangChain
* Python

This project supports:

* Multiple chat conversations
* Persistent thread-based chat history
* Streaming AI responses
* Sidebar conversation navigation
* ChatGPT-style conversation titles

---

# Features

## Multi-Conversation Support

Each conversation gets a unique `thread_id`.

Users can:

* Create new chats
* Switch between old chats
* Continue previous conversations

---

## Streaming Responses

The chatbot streams responses token-by-token using:

```python
st.write_stream()
```

This creates a real-time typing effect similar to ChatGPT.

---

## Sidebar Conversation History

Conversation titles are automatically generated from the user's first message.

Example:

```text
How to use LangGraph?
Stock prediction help
Deploy Streamlit app
```

---

# Project Structure

```text
project/
│
├── chatbot_backend.py
├── streamlit_frontend_threading.py
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone <your_repo_url>
cd <project_folder>
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv myvenv
myvenv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Required Packages

Example `requirements.txt`

```text
streamlit
langchain
langgraph
openai
python-dotenv
```

Add any additional packages your backend uses.

---

# Running the App

```bash
streamlit run streamlit_frontend_threading.py
```

---

# How It Works

## Thread Management

Each new conversation gets a unique UUID:

```python
thread_id = uuid.uuid4()
```

This ID is used by LangGraph memory.

---

## Session State

Streamlit session state stores:

| Variable          | Purpose                 |
| ----------------- | ----------------------- |
| `message_history` | Current chat messages   |
| `thread_id`       | Current conversation ID |
| `chat_threads`    | All saved conversations |

---

## Chat Threads

Chat threads are stored as:

```python
{
    thread_id: conversation_title
}
```

Example:

```python
{
    "123abc": "How to use LangGraph",
    "456xyz": "Stock prediction help"
}
```

---

## Conversation Loading

Old conversations are restored using:

```python
chatbot.get_state(
    config={'configurable': {'thread_id': thread_id}}
)
```

---

# Streamlit Frontend Workflow

## User enters message

```python
user_input = st.chat_input()
```

---

## Message saved to history

```python
st.session_state['message_history'].append(...)
```

---

## LangGraph streams response

```python
chatbot.stream(...)
```

---

## AI response displayed

```python
st.write_stream()
```

---

# Important Concepts

## Why Session State?

Streamlit reruns the script after every interaction.

`st.session_state` preserves variables between reruns.

Without it:

* messages disappear
* threads reset
* conversations are lost

---

## Why Thread IDs?

LangGraph memory uses:

```python
configurable = {'thread_id': ...}
```

to maintain separate conversations.

Each thread keeps its own memory.

---

