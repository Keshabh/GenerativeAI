#Here we will be using LLM to generate SQL from text and use it fetch the data from the db.
#we will be using sqllite3, which is lightweight, serverless, requires no database engine, no configurations.
#sqllite3 can be used for small applicatons, for dev, for test  and is stored as a file.

#In prompt, we will specify that it has to do text to sql conversion, table name, column names will be provided
#and some examples will also be given

from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import sqlite3
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-pro")

def get_gemini_response(input, prompt):
    response = model.generate_content([prompt, input])
    return response.text

def retrieve_data_using_sql_query(sql, table):
    conn = sqlite3.connect(table)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt = """
You are an expert in converting a given english text into a SQL query.
The SQL database name is STUDENT, with following schema details:
NAME VARCHAR(30), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT\n
Take following as the examples: \n
Example 1 - Tell me the count of all the students in the table, then the SQL query would be like "SELECT COUNT(*) FROM STUDENT"\n
Example 2- Give me all students wose marks is greater than 70, then the SQL query would be like "SELECT * FROM STUDENT WHERE MARKS > 70"\n
also make sure SQL does not have ''' in the beigining or end.
"""

st.header("AI Powered Smart Data Fetcher")
input = st.text_input("Enter what kind of data do you want to fetch from Student table.")

if input:
    sql = get_gemini_response(input, prompt)
    print(sql)
    rows = retrieve_data_using_sql_query(sql, 'student.db')
    for row in rows:
        st.write(row)
