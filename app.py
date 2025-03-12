import streamlit as st
from langchain_deepseek import ChatDeepSeek
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
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

st.title("AI-Powered Cover Letter Builder")





# --- File Upload Section ---
st.subheader("Upload your resume(s)")
st.write("Upload a document (TXT, PDF, DOCX)")
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
st.write("Load a saved file")
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


print('App ready')


# --- Build the cover letter ---
st.subheader("Build your cover letter")

job_description = st.text_area("Enter the job description:")

user_input = st.text_input("Enter your prompt:", value="Write a cover letter for the given position. Write up to three paragraphs, while using  simple, personable and heartfelt language. ")

user_input = job_description + "\n" + user_input

# Add a button to submit the query
if st.button("Generate") and user_input and text:
    # Initialize LLM
    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=0.7
    )

    prompt = f"Use the following text to answer: {text}\n\nQuestion: {user_input}"
    response = llm.invoke([("human", prompt)])

    st.write("### Response:")
    st.write(response.content)

