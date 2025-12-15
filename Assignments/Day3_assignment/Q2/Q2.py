import streamlit as st

st.title("Login")
inp=st.text_input("Enter the Username ")
pas=st.text_input("Enter the Password ")

if st.button("Login"):
    if inp and pas:
        if inp=="darshancfr" and pas=="Dc@12345678":
            st.toast("Login successful")
            
            st.switch_page("pages/weather_app.py")

        else:
            st.toast("Invalid Username or Password")

    else:
        st.warning("Please fill all the fields")  



