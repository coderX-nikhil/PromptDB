# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import sqlite3

# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

# def get_gemini_response(question,prompt):
#     model=genai.GenerativeModel('gemini-pro')
#     response=model.generate_content([prompt[0],question]) 
#     return response.text 


# def read_sql_query(sql,db):
#     conn=sqlite3.connect(db) 
#     cur=conn.cursor()
#     cur.execute(sql) 
#     rows=cur.fetchall() 
#     conn.commit()
#     conn.close()
#     for row in rows:
#         print(row)
#     return rows


# prompt=[
#     """
#     You are an expert in converting English questions to SQL query! 
#     The SQL database has the name STUDENT and has the following column - NAME, CLASS, SECTION and MARKS \n\nFor example, \nExample 1 - How many entries of records are present?, the SQL command will be something like this SELECT COUNT(*) from STUDENT; \n Example 2 - Tell me all the student studying in Data science class?, The SQL command will be something like this SELECT * FROM STUDENT WHERE CLASS= "Data Science"; Also, the SQL code should not have ``` in the beginning or end and sql word in output
# """
# ] 

# st.set_page_config(page_title="PromptDB ")
# # st.header ("PromptDB ")
# st.image("logo.png",use_column_width=True, output_format="auto", caption="SQl using Simple Prompts...")
# question=st.text_input("Input Prompt:",key="Input")
# submit=st.button("Execute Prompt")
# if submit: 
#     # response=get_gemini_response(question,prompt)
#     # print(response)
#     # data=read_sql_query(response,"student.db")
#     # st.subheader("The response is")
#     # for row in data:
#     #     print(row)
#     #     st.header(row)

#     # response = get_gemini_response(question, prompt)
#     # st.subheader("The response is")
#     # data = read_sql_query(response, "student.db")
#     # st.table(data)


#     response = get_gemini_response(question, prompt)
#     st.subheader("The generated SQL query is:")
#     st.code(response)
#     data = read_sql_query(response, "student.db")
#     st.subheader("The response is")
#     st.table(data)

# from dotenv import load_dotenv
# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai

# load_dotenv()

# # Configure Gemini API
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
#     return response.text.strip()  # Strip any leading/trailing whitespace

# def read_sql_query(sql, db):
#     try:
#         # Open the SQLite connection
#         conn = sqlite3.connect(db)
#         cur = conn.cursor()
        
#         # Try to execute the query
#         cur.execute(sql)
#         rows = cur.fetchall()
        
#         # Commit and close the connection
#         conn.commit()
#         conn.close()
        
#         # Print the rows for debugging
#         for row in rows:
#             print(row)
#         return rows

#     except sqlite3.Error as e:
#         # Print the error and return an empty list if there's an SQL issue
#         st.error(f"SQL Error: {e}")
#         return []

# # The prompt used for SQL generation
# prompt = [
#     """
#     You are an expert in converting English questions to SQL query! 
#     The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION, and MARKS. \n\nFor example, \nExample 1 - How many entries of records are present? The SQL command will be something like: SELECT COUNT(*) from STUDENT; \n Example 2 - Tell me all the students studying in Data science class? The SQL command will be: SELECT * FROM STUDENT WHERE CLASS = 'Data Science'; The SQL code should not have any `sql` word or ``` in output.
#     """
# ]

# # Streamlit UI setup
# st.set_page_config(page_title="PromptDB")
# st.image("logo.png", use_column_width=True, output_format="auto", caption="SQL using Simple Prompts...")
# question = st.text_input("Input Prompt:", key="Input")
# submit = st.button("Execute Prompt")

# # Execution logic when the user submits a prompt
# if submit:
#     response = get_gemini_response(question, prompt)
    
#     # Show the generated SQL query
#     st.subheader("The generated SQL query is:")
#     st.code(response)
    
#     # Read and execute the query on the database
#     data = read_sql_query(response, "student.db")
    
#     # Display the result in a table
#     st.subheader("The response is:")
#     if data:
#         st.table(data)
#     else:
#         st.write("No data returned or query error.")

import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

def read_sql_query(sql, conn):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    except sqlite3.Error as e:
        st.error(f"SQL Error: {e}")
        return []

def analyze_schema(conn):
    try:
        cur = conn.cursor()
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        cur.execute(query)
        tables = cur.fetchall()
        
        schema_info = {}
        for table in tables:
            table_name = table[0]
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()
            schema_info[table_name] = [col[1] for col in columns]  # Extracting column names
        return schema_info
    except sqlite3.Error as e:
        st.error(f"Error analyzing schema: {e}")
        return {}

def display_schema(schema_info):
    with st.sidebar:
        st.subheader("Database Schema")
        for table, columns in schema_info.items():
            st.write(f"**{table}**")
            st.write(", ".join(columns))

# The prompt template
prompt_template = """
You are an expert in converting English questions to SQL query!
The SQL database has the following structure: \n{schema}\n
For example, \nExample 1 - How many entries of records are present in TableName? 
The SQL command will be something like: SELECT COUNT(*) FROM TableName; \n
Example 2 - List all records in TableName where ColumnName is 'SomeValue'? 
The SQL command will be: SELECT * FROM TableName WHERE ColumnName = 'SomeValue';
"""

# Streamlit UI setup
st.set_page_config(page_title="PromptDB with Upload")
st.image("logo.png", use_column_width=True, output_format="auto", caption="SQL using Simple Prompts...")

# File upload feature
uploaded_file = st.file_uploader("Upload a .DB file", type=["db"])

if uploaded_file:
    # Load the SQLite database
    conn = sqlite3.connect(uploaded_file)
    
    # Analyze the schema of the uploaded database
    schema_info = analyze_schema(conn)
    
    # Display the schema in the sidebar
    display_schema(schema_info)
    
    # Generate prompt based on schema
    schema_description = "\n".join([f"Table: {table}, Columns: {', '.join(columns)}" for table, columns in schema_info.items()])
    prompt = [prompt_template.format(schema=schema_description)]
    
    # Question input and execution
    question = st.text_input("Input Prompt:", key="Input")
    submit = st.button("Execute Prompt")

    if submit:
        # Get the Gemini AI response
        response = get_gemini_response(question, prompt)
        
        # Show the generated SQL query
        st.subheader("The generated SQL query is:")
        st.code(response)
        
        # Execute the SQL query on the uploaded database
        data = read_sql_query(response, conn)
        
        # Display the result in a table
        st.subheader("The response is:")
        if data:
            df = pd.DataFrame(data)
            st.table(df)
        else:
            st.write("No data returned or query error.")
else:
    st.write("Please upload a .DB file to analyze and generate queries.")
