from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question]) 
    return response.text 


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


prompt=[
    """
    You are an expert in converting English questions to SQL query! 
    The SQL database has the name STUDENT and has the following column - NAME, CLASS, SECTION and MARKS \n\nFor example, \nExample 1 - How many entries of records are present?, the SQL command will be something like this SELECT COUNT(*) from STUDENT; \n Example 2 - Tell me all the student studying in Data science class?, The SQL command will be something like this SELECT * FROM STUDENT WHERE CLASS= "Data Science"; Also, the SQL code should not have ``` in the beginning or end and sql word in output
"""
] 

st.set_page_config(page_title="PromptDB ")
# st.header ("PromptDB ")
st.image("logo.png",use_column_width=True, output_format="auto", caption="SQl using Simple Prompts...")
question=st.text_input("Input Prompt:",key="Input")
submit=st.button("Execute Prompt")
if submit: 
    # response=get_gemini_response(question,prompt)
    # print(response)
    # data=read_sql_query(response,"student.db")
    # st.subheader("The response is")
    # for row in data:
    #     print(row)
    #     st.header(row)

    # response = get_gemini_response(question, prompt)
    # st.subheader("The response is")
    # data = read_sql_query(response, "student.db")
    # st.table(data)


    response = get_gemini_response(question, prompt)
    st.subheader("The generated SQL query is:")
    st.code(response)
    data = read_sql_query(response, "student.db")
    st.subheader("The response is")
    st.table(data)

