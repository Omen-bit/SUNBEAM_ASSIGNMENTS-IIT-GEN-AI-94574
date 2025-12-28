import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model

load_dotenv()

st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("Resume RAG Analyzer")

PDF_FOLDER = r"D:\Sunbeam\SUNBEAM_ASSIGNMENTS-IIT-GEN-AI-94574\Assignments\Day11_RAG_Assignment\Pdfs"
CHROMA_DIR = "Chroma_db_full_docs"

def extract_candidate_name(pdf_path):
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        words = pages[0].page_content.strip().split()
        return " ".join(words[:2])
    except:
        return "Unknown"

@st.cache_resource
def load_vector_store():
    loader = DirectoryLoader(PDF_FOLDER, glob="*.pdf", loader_cls=PyPDFLoader)
    docs = list(loader.lazy_load())
    for doc in docs:
        source = doc.metadata["source"]
        doc.metadata["resume_id"] = os.path.basename(source)
        doc.metadata["candidate_name"] = extract_candidate_name(source)
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=CHROMA_DIR,
        collection_name="resumes_full"
    )
    if vector_store._collection.count() == 0:
        vector_store.add_documents(docs)
    return vector_store

vector_store = load_vector_store()

llm = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

data = []
for file in os.listdir(PDF_FOLDER):
    if file.lower().endswith(".pdf"):
        path = os.path.join(PDF_FOLDER, file)
        data.append({"PDF File": file, "Candidate Name": extract_candidate_name(path)})

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

with st.sidebar:
    st.title("Resume Management")
    uploaded_file = st.file_uploader("Add Resume", type=["pdf"])
    delete_file = st.selectbox("Delete Resume", ["Select"] + df["PDF File"].tolist())
    update_file = st.selectbox("Update Resume", ["Select"] + df["PDF File"].tolist())
    updated_pdf = st.file_uploader("Upload Updated PDF", type=["pdf"], key="update")

if uploaded_file:
    with open(os.path.join(PDF_FOLDER, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Resume added. Refresh page.")

if delete_file != "Select":
    if st.button("Confirm Delete"):
        os.remove(os.path.join(PDF_FOLDER, delete_file))
        st.success("Resume deleted. Refresh page.")

if update_file != "Select" and updated_pdf:
    with open(os.path.join(PDF_FOLDER, update_file), "wb") as f:
        f.write(updated_pdf.getbuffer())
    st.success("Resume updated. Refresh page.")

user_query = st.chat_input("Ask a question")

if user_query:
    results = vector_store.similarity_search(query=user_query, k=3)
    context = ""
    for doc in results:
        context += f"\n\nResume File: {doc.metadata['resume_id']}\n"
        context += doc.page_content

    messages = [
        {
            "role": "system",
            "content": """
You are an intelligent assistant.

If the question is resume-related, answer strictly using the provided resumes.
Full Name:
Resume File Name:

Resume  Summary:

if there are multiple resumes at the end of the answer you should say 'opinion' and add your suggestions about all the displayed resumes 

If the question is general knowledge or unrelated to resumes, answer normally without using resume data.
If resume information is missing, respond with: I don't know.
"""
        },
        {
            "role": "user",
            "content": f"Resumes:\n{context}\n\nQuestion: {user_query}"
        }
    ]

    response = llm.invoke(messages)
    st.markdown("### Answer")
    st.write(response.content)