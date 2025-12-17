import os
import requests
import json
from dotenv import load_dotenv
import streamlit as st
import time

def get_phi_4_mini():
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    req_data = {
        "model": "microsoft/phi-4-mini-reasoning",
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
    }

    t1 = time.perf_counter()
    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    resp = response.json()
    text = resp["choices"][0]["message"]["content"]
    final_answer = text.split("</think>")[-1].replace("\\boxed{", "").replace("}", "").strip()
    t2 = time.perf_counter()
    return final_answer, t2 - t1





def get_groq():
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    req_data = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
    }

    t1 = time.perf_counter()
    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    chat_output = response.json()
    t2 = time.perf_counter()
    return chat_output["choices"][0]["message"]["content"], t2 - t1




load_dotenv()
api_key = "dummy-key"
API_KEY = os.getenv("GROQ_API_KEY")

st.title("My Chatbot")

if "msg" not in st.session_state:
    st.session_state.msg = []

if "model" not in st.session_state:
    st.session_state.model = None

for chat in st.session_state.msg:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

user_prompt = st.chat_input("Ask anything:")

with st.sidebar:
    st.title("Model Section")
    st.session_state.model = st.selectbox(
        "Models",
        ("Groq", "Phi 4 Mini"),
        index=None,
        placeholder="Select a model"
    )

if user_prompt and st.session_state.model is None:
    st.warning("Select a model from model section")

if user_prompt and st.session_state.model:
    st.session_state.msg.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.model == "Phi 4 Mini":
                reply, elapsed = get_phi_4_mini()
            else:
                reply, elapsed = get_groq()
            st.write(reply)
            st.caption(f"Response in {elapsed:.2f} seconds")

    st.session_state.msg.append({"role": "assistant", "content": reply})
