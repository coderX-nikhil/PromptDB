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


from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from streamlit_lottie import st_lottie
import requests

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()

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
        st.error(f"SQL Error: {e}")
        return []

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    
    The SQL database has the name STUDENT and has the following columns: NAME, CLASS, SECTION, and MARKS.

    For example,
    Example 1 - How many entries of records are present?
    The SQL command will be something like: SELECT COUNT(*) from STUDENT;

    Example 2 - Tell me all the students studying in Data science class?
    The SQL command will be: SELECT * FROM STUDENT WHERE CLASS = 'Data Science';

    The SQL code should not have any `sql` word or ``` in output.
    """
]

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Streamlit UI setup
st.set_page_config(page_title="PromptDB", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main {
        background: #ffffff;
        padding: 3rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# Page layout
col1, col2 = st.columns([2, 1])

with col1:
    st.title("PromptDB: SQL using Simple Prompts")
    st.write("Convert your natural language questions into SQL queries with ease!")

    question = st.text_input("Enter your question:", key="Input")
    submit = st.button("Generate SQL Query")

with col2:
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_qp1q7mct.json"
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, height=200)

# Execution logic when the user submits a prompt
if submit:
    with st.spinner("Generating SQL query..."):
        response = get_gemini_response(question, prompt)
    
    st.subheader("Generated SQL Query:")
    st.code(response, language="sql")
    
    with st.spinner("Executing query..."):
        data = read_sql_query(response, "student.db")
    
    st.subheader("Query Result:")
    if data:
        st.dataframe(data)
    else:
        st.info("No data returned or query error.")

# Add some extra information or tips
st.sidebar.header("Tips")
st.sidebar.info(
    "Try asking questions like:\n"
    "1. How many students are there?\n"
    "2. Show me all students in the Science class.\n"
    "3. What's the average mark for each section?"
)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ by Your Name")