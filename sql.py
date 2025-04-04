from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key="AIzaSyB-4NIkdRvAcOxq70gUJkArLTa6dky5ewI")

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.textfrom dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI API Key securely
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key not found. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()
genai.configure(api_key=api_key)

# Function to get response from Gemini
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content("\n".join([prompt, question]))
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in AI model: {str(e)}")
        return None

# Function to execute SQL query
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return []

# Define prompt
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database is named STUDENT with columns: NAME, CLASS, SECTION.

Example Queries:
1. "How many entries are there?" → SELECT COUNT(*) FROM STUDENT;
2. "Show students in Data Science class." → SELECT * FROM STUDENT WHERE CLASS="Data Science";

Ensure the output is a valid SQL query, without ` ``` ` or sql.
"""

# Streamlit UI
st.set_page_config(page_title="SQL Query Generator")
st.header("Generate SQL Queries with Gemini AI")

question = st.text_input("Enter your question in English:", key="input")
submit = st.button("Generate SQL Query")

# Handle submission
if submit and question:
    response = get_gemini_response(question, prompt)
    
    if response:
        st.subheader("Generated SQL Query:")
        st.code(response, language="sql")

        # Run SQL query
        results = read_sql_query(response, "student.db")
        
        if results:
            st.subheader("Query Results:")
            for row in results:
                st.write(row)
        else:
            st.warning("No results found or error in query execution.")

## Fucntion To retrieve query from the database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

## Define Your Prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response,"student.db")
    st.subheader("The REsponse is")
    for row in response:
        print(row)
        st.header(row)









