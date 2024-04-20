import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Function to create database table if not exists
def create_table():
    conn = sqlite3.connect('student_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, dob TEXT, marks INTEGER, phone TEXT)''')
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(name, dob, marks, phone):
    conn = sqlite3.connect('student_data.db')
    c = conn.cursor()
    c.execute('''INSERT INTO students (name, dob, marks, phone) VALUES (?, ?, ?, ?)''', (name, dob, marks, phone))
    conn.commit()
    conn.close()

# Function to fetch all data from the database
def fetch_data():
    conn = sqlite3.connect('student_data.db')
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()
    return df

# Main Streamlit app
def main():
    create_table()
    st.title("Student Database Management System")

    # Input fields for adding new student data
    name = st.text_input("Enter Name:")
    dob = st.date_input("Enter Date of Birth:")
    marks = st.number_input("Enter Marks Obtained:")
    phone = st.text_input("Enter Phone Number:")

    if st.button("Add Student"):
        insert_data(name, dob, marks, phone)
        st.success("Student added successfully!")

    # Display current student data
    st.subheader("Current Student Data:")
    df = fetch_data()
    st.dataframe(df)

    # Data querying
    st.subheader("Query Student Data:")
    query = st.text_input("Enter SQL Query:")
    if st.button("Run Query"):
        conn = sqlite3.connect('student_data.db')
        queried_df = pd.read_sql_query(query, conn)
        conn.close()
        st.dataframe(queried_df)

    # Bar plot of marks obtained by students
    st.subheader("Bar Plot of Marks Obtained:")
    marks_df = df[['name', 'marks']]
    plt.figure(figsize=(10, 6))
    plt.bar(marks_df['name'], marks_df['marks'])
    plt.xlabel('Student Name')
    plt.ylabel('Marks Obtained')
    plt.xticks(rotation=45)
    st.pyplot(plt)

if __name__ == "__main__":
    main()
