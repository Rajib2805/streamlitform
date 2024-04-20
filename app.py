import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('userdata.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, dob DATE, email TEXT)''')
conn.commit()

# Function to add user data to the database
def add_user(name, dob, email):
    c.execute("INSERT INTO users (name, dob, email) VALUES (?, ?, ?)", (name, dob, email))
    conn.commit()

# Function to update user data in the database
def update_user(user_id, name, dob, email):
    c.execute("UPDATE users SET name=?, dob=?, email=? WHERE id=?", (name, dob, email, user_id))
    conn.commit()

# Function to delete user data from the database
def delete_user(user_id):
    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

# Function to retrieve all user data from the database
def get_all_users():
    c.execute("SELECT * FROM users")
    return c.fetchall()

# Streamlit app
def main():
    st.title("User Management App")

    # Form to add or update user data
    st.subheader("Add or Update User")
    name = st.text_input("Name")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")

    add_update_button = st.button("Add/Update User")

    if add_update_button:
        add_user(name, dob, email)
        st.success("User added/updated successfully!")

    # Display all users
    st.subheader("All Users")
    users = get_all_users()
    for user in users:
        st.write(f"ID: {user[0]}, Name: {user[1]}, DOB: {user[2]}, Email: {user[3]}")

    # Form to delete user data
    st.subheader("Delete User")
    user_id_to_delete = st.number_input("Enter User ID to delete")
    delete_button = st.button("Delete User")

    if delete_button:
        delete_user(user_id_to_delete)
        st.success("User deleted successfully!")

if __name__ == "__main__":
    main()



