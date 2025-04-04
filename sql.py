import os
import sqlite3
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing GOOGLE_API_KEY in .env file")

genai.configure(api_key=api_key)

# Function to get Gemini response
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel(model_name="gemini-pro")  # 'gemini-pro' works here if your API key has access
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        print("Error from Gemini:", e)
        return None

# Function to query the SQLite DB
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return []

# SQL Prompt definition
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION

    For example:
    Example 1 - How many entries of records are present?
    The SQL command will be: SELECT COUNT(*) FROM STUDENT;

    Example 2 - Tell me all the students studying in Data Science class?
    The SQL command will be: SELECT * FROM STUDENT WHERE CLASS="Data Science";

    Please provide only the SQL query without ``` or any prefix like 'sql'.
    """
]

# Streamlit UI
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and question:
    with st.spinner("Generating SQL with Gemini..."):
        sql_query = get_gemini_response(question, prompt)

    if sql_query:
        st.subheader("Generated SQL Query:")
        st.code(sql_query)

        with st.spinner("Running SQL query on student.db..."):
            result = read_sql_query(sql_query, "student.db")

        st.subheader("Query Results:")
        if result:
            for row in result:
                st.write(row)
        else:
            st.write("No results or an error occurred while querying the database.")
    else:
        st.error("Failed to get a response from Gemini API. Please check your API key or model access.")
