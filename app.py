import os
import streamlit as st
from llama_index.llms.gemini import Gemini
from llama_index.core import SQLDatabase
from dotenv import load_dotenv
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Database connection
db_uri = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_uri)
sql_database = SQLDatabase(engine=engine, include_tables=['states'])

# Test database connection
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM states"))
    st.write("Database connection successful. Number of states:", result.fetchone()[0])

# Initialize LLM
llm = Gemini(
    model="models/gemini-2.0-flash",
    # api_key="some key",  # uses GOOGLE_API_KEY env var by default
)

# Initialize query engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["states"], llm=llm
)

# Define query function
def queryDB(query_str):
    response = query_engine.query(query_str)
    return response

# Streamlit app
st.title("State Population Query App")

query_str = st.text_input("Enter your query:", "Which state has the highest population?")
if st.button("Submit"):
    response = queryDB(query_str)
    st.write("Response:", response)