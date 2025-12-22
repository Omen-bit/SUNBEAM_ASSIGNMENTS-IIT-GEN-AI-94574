from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import streamlit as st
import pandas as pd

load_dotenv()

chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)
driver.get("https://www.sunbeaminfo.in/internship")
driver.implicitly_wait(5)

table = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[@id='collapseSix']//table")
    )
)

rows = table.find_elements(By.XPATH, ".//tbody/tr")

with open("table_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        writer.writerow([cell.get_attribute("textContent").strip() for cell in cells])

table2 = wait.until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, "table-responsive")
    )
)

rows2 = table2.find_elements(By.XPATH, ".//tbody/tr")

with open("day9_q1.csv", "w", newline="", encoding="utf-8") as file2:
    writer2 = csv.writer(file2)
    for row in rows2:
        cells2 = row.find_elements(By.TAG_NAME, "td")
        writer2.writerow([cell.get_attribute("textContent").strip() for cell in cells2])

driver.quit()

df = pd.read_csv(r"D:\Sunbeam\SUNBEAM_ASSIGNMENTS-IIT-GEN-AI-94574\Assignments\Day9_Assignment\day9_q1.csv")

st.title("Data Scrapper")
st.dataframe(df)

file_path = r"D:\Sunbeam\SUNBEAM_ASSIGNMENTS-IIT-GEN-AI-94574\Assignments\Day9_Assignment\day9_q1.csv"

@tool
def read_file(file_path: str) -> str:
    """Read CSV and return content as text"""
    return df.to_string()

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="non-needed"
)

agent = create_agent(
    model=llm,
    tools=[read_file],
    system_prompt="You are a helpful assistant which answers questions based on the CSV data"
)

user_input = st.chat_input("You:")

if user_input:
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })
    llm_output = result["messages"][-1]
    st.write("You:", user_input)
    st.write("AI:", llm_output.content)
