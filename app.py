import streamlit as st
from main import rag_pipeline
from datetime import datetime

st.set_page_config(page_title="📄 RAG Chatbot", layout="wide")

# Custom CSS for better left-right layout and bubble style
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            background-color: #121212;
            color: #e0e0e0;
        }
        .chat-scroll {
            max-height: 70vh;
            overflow-y: auto;
            padding-right: 10px;
        }
        .chat-row {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1rem;
        }
        .chat-left {
            justify-content: flex-start;
            margin-right: 25%;
        }
        .chat-right {
            justify-content: flex-end;
            margin-left: 25%;
        }
        .bubble {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 16px;
            line-height: 1.5;
            margin: 0 10px;
            display: inline-block;
            word-wrap: break-word;
        }
        .user-bubble {
            background-color: #1e88e5;
            color: white;
            border-top-left-radius: 0;
            text-align: left;
        }
        .bot-bubble {
            background-color: #2e7d32;
            color: #fff;
            border-top-right-radius: 0;
            text-align: left;
        }
        .avatar {
            height: 40px;
            width: 40px;
            border-radius: 50%;
        }
        .timestamp {
            font-size: 0.7rem;
            color: #aaa;
            margin-top: 4px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🤖 Document RAG Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ask any question based on the uploaded documents</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for upload section
st.sidebar.header("📁 Upload Documents")
uploaded_files = st.sidebar.file_uploader("Upload PDF/DOCX files", type=["pdf", "docx"], accept_multiple_files=True)
if uploaded_files:
    st.sidebar.success(f"{len(uploaded_files)} document(s) uploaded")
else:
    st.sidebar.info("No documents uploaded yet")

# User input form
with st.form("user_input_form", clear_on_submit=True):
    query = st.text_input("Your Question", placeholder="Type your question here...")
    submit = st.form_submit_button("Send")

if submit and query.strip():
    with st.spinner("Searching..."):
        answer, source = rag_pipeline(query, uploaded_files)  # <-- handle both uploaded and default files
        timestamp = datetime.now().strftime("%I:%M %p")

        st.session_state.chat_history.append({
            "role": "user",
            "text": query,
            "time": timestamp
        })
        st.session_state.chat_history.append({
            "role": "bot",
            "text": answer,
            "source": source,
            "time": timestamp
        })

# Chat Display
st.markdown("<div class='chat-scroll'>", unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class='chat-row chat-left'>
                <img src='https://img.icons8.com/color/48/user-male-circle--v1.png' class='avatar'/>
                <div>
                    <div class='bubble user-bubble'>{msg['text']}</div>
                    <div class='timestamp'>{msg['time']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class='chat-row chat-right'>
                <div>
                    <div class='bubble bot-bubble'><div>{msg['text']}<br><small>📄 Source: {msg['source']}</small></div></div>
                    <div class='timestamp' style='text-align:right;'>{msg['time']}</div>
                </div>
                <img src='https://img.icons8.com/color/48/bot.png' class='avatar'/>
            </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Scroll to bottom
st.components.v1.html("""
<script>
    const chatContainer = window.parent.document.querySelector('.main .block-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
</script>
""", height=0)
