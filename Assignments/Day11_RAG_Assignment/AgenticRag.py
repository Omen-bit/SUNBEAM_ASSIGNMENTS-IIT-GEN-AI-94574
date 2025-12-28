import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

load_dotenv()

st.set_page_config(page_title="Agentic Resume RAG", layout="wide")
st.title("Agentic Resume Intelligence")

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
        source = doc.metadata.get("source", "")
        doc.metadata["resume_id"] = os.path.basename(source) if source else "Unknown"
        doc.metadata["candidate_name"] = extract_candidate_name(source) if source else "Unknown"
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = Chroma(
        embedding_function=embeddings,
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

@tool
def resume_retrieval_tool(query: str) -> str:
    """
    Retrieve and search through resume documents based on semantic similarity.
    
    This tool searches through a vector database of resume documents and returns
    the most relevant resumes based on the input query. It performs semantic search
    to find resumes that match the query context, skills, experience, or qualifications.
    
    Args:
        query (str): The search query describing what to look for in resumes.
                    Examples: "Python developer with 5 years experience",
                             "candidate with machine learning skills",
                             "software engineer with AWS certification"
    
    Returns:
        str: A formatted string containing the top 4 most relevant resume excerpts.
             Each result includes:
             - Resume file name
             - Candidate name
             - Relevant content from the resume
             Returns "No relevant resume information found." if no matches are found.
    
    Use this tool when:
    - Searching for candidates with specific skills or qualifications
    - Looking for experience in particular technologies or domains
    - Finding resumes that match job requirements
    - Comparing multiple candidates based on criteria
    - Extracting information about specific candidates
    """
    results = vector_store.similarity_search(query=query, k=4)
    
    if not results:
        return "No relevant resume information found."
    
    combined_content = ""
    for idx, doc in enumerate(results, 1):
        resume_id = doc.metadata.get('resume_id', 'Unknown')
        candidate_name = doc.metadata.get('candidate_name', 'Unknown')
        combined_content += f"Resume {idx} - File: {resume_id}, Candidate: {candidate_name}\n"
        combined_content += doc.page_content + "\n\n"
    
    return combined_content.strip()

system_message = SystemMessage(content="""You are an intelligent resume analysis agent.

Rules:
- If the question is resume-related, you MUST use resume_retrieval_tool.
- Answer ONLY from retrieved resume content.
- If information is missing, say: I don't know.
- Format answers as:
  Full Name:
  Resume File Name:
  Resume Summary:
- If multiple resumes are involved, add a final section titled 'Opinion' with professional suggestions for each candidate.
- If the question is not resume-related, answer normally.
""")

agent = create_react_agent(llm, [resume_retrieval_tool])

data = []
if os.path.exists(PDF_FOLDER):
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
        st.success("Resume added. Refresh the page.")
    
    if delete_file != "Select":
        if st.button("Confirm Delete"):
            os.remove(os.path.join(PDF_FOLDER, delete_file))
            st.success("Resume deleted. Refresh the page.")
    
    if update_file != "Select" and updated_pdf:
        with open(os.path.join(PDF_FOLDER, update_file), "wb") as f:
            f.write(updated_pdf.getbuffer())
        st.success("Resume updated. Refresh the page.")

query = st.chat_input("Ask a resume-related question")

if query:
    response = agent.invoke({"messages": [system_message, {"role": "user", "content": query}]})
    
    st.markdown("### Answer")
    
    final_message = response["messages"][-1]
    st.write(final_message.content)