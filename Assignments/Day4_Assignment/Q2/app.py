import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CSV Explorer App")

USERS_FILE = "users.csv"
FILES_HISTORY = "userfiles.csv"

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(FILES_HISTORY):
    pd.DataFrame(columns=["username", "filename", "uploaded_at"]).to_csv(FILES_HISTORY, index=False)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

def load_users():
    return pd.read_csv(USERS_FILE)

def save_user(username, password):
    df = load_users()
    df.loc[len(df)] = [username, password]
    df.to_csv(USERS_FILE, index=False)

def authenticate(username, password):
    df = load_users()
    return not df[(df.username == username) & (df.password == password)].empty

def save_file_history(username, filename):
    df = pd.read_csv(FILES_HISTORY)
    df.loc[len(df)] = [username, filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    df.to_csv(FILES_HISTORY, index=False)

st.sidebar.title("Menu")

if not st.session_state.logged_in:
    menu = st.sidebar.radio("Navigation", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Navigation", ["Explore CSV", "See History", "Logout"])

if menu == "Home":
    st.title("Home")
    st.write("Welcome! Please login or register to explore CSV files.")

elif menu == "Register":
    st.title("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        df = load_users()
        if username in df.username.values:
            st.error("User already exists")
        else:
            save_user(username, password)
            st.success("Registration successful! Please login.")

elif menu == "Login":
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

elif menu == "Explore CSV":
    st.title("Explore CSV")

    uploaded_file = st.file_uploader("Upload CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.subheader("Preview")
        st.dataframe(df)

        save_file_history(st.session_state.username, uploaded_file.name)
        st.success("File uploaded and history saved")

elif menu == "See History":
    st.title("Upload History")

    df = pd.read_csv(FILES_HISTORY)
    user_history = df[df.username == st.session_state.username]

    if user_history.empty:
        st.info("No uploads yet")
    else:
        st.dataframe(user_history)

elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = None
    st.success("Logged out successfully")
    st.rerun()
