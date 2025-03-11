import streamlit as st
from langchain_deepseek import ChatDeepSeek
import os
import docx
import fitz  # PyMuPDF for PDFs

from dotenv import load_dotenv
load_dotenv()



# Get API key from environment
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    st.error("API key not found! Make sure to set it in the .env file.")
else:
    os.environ["DEEPSEEK_API_KEY"] = api_key  # Optional: Explicitly set for LangChain






# Ensure data folder exists
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

st.title("RAG Chatbot with Document Upload!")





# --- File Upload Section ---
st.subheader("Upload a document (TXT, PDF, DOCX)")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

text = ""

if uploaded_file is not None:
    file_path = os.path.join(DATA_FOLDER, uploaded_file.name)

    # Save uploaded file permanently
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved: `{file_path}`")

    # Extract text from the file
    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif file_type == "pdf":
        pdf_document = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in pdf_document])
    elif file_type == "docx":
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    st.text_area("Extracted Document Text", text, height=200)





# --- Load Existing Files ---
st.subheader("Previously Uploaded Files")
existing_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(("txt", "pdf", "docx"))]

selected_file = st.selectbox("Select a file to load:", ["None"] + existing_files)

if selected_file != "None":
    file_path = os.path.join(DATA_FOLDER, selected_file)
    file_type = selected_file.split(".")[-1]

    if file_type == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif file_type == "pdf":
        pdf_document = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in pdf_document])
    elif file_type == "docx":
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    st.text_area("Loaded Document Text", text, height=200)
    st.info(f"Loaded text from `{selected_file}`")





# --- Ask Question Based on File ---
st.subheader("Ask a Question Based on the Document")
user_input = st.text_input("Enter your question:")

# Add a button to submit the query
if st.button("Ask Question") and user_input and text:
    # Initialize LLM
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.7
    )

    prompt = f"Use the following text to answer: {text}\n\nQuestion: {user_input}"
    response = llm.invoke([("human", prompt)])

    st.write("### Response:")
    st.write(response.content)

