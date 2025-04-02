import os
import streamlit as st
from llama_index.llms.groq import Groq
from llama_index.core import SQLDatabase
from dotenv import load_dotenv
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine, text
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings

# Page config
st.set_page_config(page_title="State Data Assistant", page_icon="🌎", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load environment variables and setup
load_dotenv()

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Database connection
db_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_uri)
sql_database = SQLDatabase(engine=engine, include_tables=['states'])

# Initialize LLM
llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

# Initialize query engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["states"], llm=llm
)

# Define query function
def queryDB(query_str):
    response = query_engine.query(query_str)
    return response

# Streamlit UI
st.title("📊 State Data Assistant")
st.markdown("""
Ask questions about Indian states' demographics and statistics.
Examples:
- Which state has the highest population?
- What is the literacy rate in Kerala?
- Show me the top 5 states by population density
""")

# Display database connection status
with st.sidebar:
    st.header("Database Status")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM states"))
            st.success(f"✅ Connected | {result.fetchone()[0]} states in database")
    except Exception as e:
        st.error("❌ Database connection failed")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about the states of India..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = queryDB(prompt)
            st.markdown(response)
            # Add assistant message to chat history
            st.session_state.messages.append({"role": "assistant", "content": str(response)})

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()