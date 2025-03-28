import streamlit as st
import os
import fitz  # PyMuPDF
import docx
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Ensure data folder exists
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Set page configuration
st.set_page_config(page_title="📂 File Management", page_icon="📂")
st.title("📂 File Management")

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

# --- Caching the ChromaDB connection ---
@st.cache_resource
def get_chroma_db():
    """Initialize and return a persistent ChromaDB instance."""
    chroma_client = chromadb.PersistentClient(path="vector_db")  # Stores vectors persistently
    return chroma_client

chroma_client = get_chroma_db()
collection = chroma_client.get_or_create_collection(name="documents")

embedding_model = HuggingFaceEmbeddings()

# --- Function to extract text from documents ---
def extract_text(file_path, file_type):
    """Extract text content from uploaded files."""
    if file_type == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_type == "pdf":
        pdf_document = fitz.open(file_path)
        return "\n".join([page.get_text() for page in pdf_document])
    elif file_type == "docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    return ""

# --- Upload and Store Files ---
st.subheader("📤 Upload Your Resume(s)")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    file_path = os.path.join(DATA_FOLDER, uploaded_file.name)
    
    # Save the file permanently
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved: `{file_path}`")

    # Extract text and add to vector DB
    file_text = extract_text(file_path, uploaded_file.name.split(".")[-1])
    if file_text:
        # Split text into chunks
        chunks = text_splitter.split_text(file_text)
        
        # Create unique IDs for each chunk
        chunk_ids = [f"{uploaded_file.name}_chunk_{i}" for i in range(len(chunks))]
        
        # Add chunks to ChromaDB
        collection.add(
            ids=chunk_ids,
            documents=chunks,
            metadatas=[{"filename": uploaded_file.name, "chunk_index": i} for i in range(len(chunks))]
        )
        st.success(f"✅ File `{uploaded_file.name}` split into {len(chunks)} chunks and added to ChromaDB!")
    else:
        st.warning("⚠️ Could not extract text from this file.")

# --- View and Delete Files ---
st.subheader("📂 Manage Uploaded Files")
existing_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(("txt", "pdf", "docx"))]

if existing_files:
    selected_file = st.selectbox("📄 Select a file to view or delete:", existing_files)

    # View file content
    if st.button("👀 View File"):
        file_path = os.path.join(DATA_FOLDER, selected_file)
        file_type = selected_file.split(".")[-1]
        file_text = extract_text(file_path, file_type)
        st.text_area("📄 File Content", file_text, height=250)

    # Delete file
    if st.button("🗑 Delete File"):
        # Delete the physical file
        os.remove(os.path.join(DATA_FOLDER, selected_file))
        
        # Get all chunks associated with this file
        results = collection.get(
            where={"filename": selected_file}
        )
        
        if results and results['ids']:
            # Delete all chunks from ChromaDB
            collection.delete(ids=results['ids'])
            st.success(f"🗑 Deleted `{selected_file}` and its {len(results['ids'])} chunks")
        else:
            st.warning(f"⚠️ No chunks found for `{selected_file}` in the database")
            
        st.rerun()
else:
    st.info("🚫 No files uploaded yet.")
