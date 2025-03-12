import streamlit as st
import os
import fitz  # PyMuPDF
import docx

# Ensure data folder exists
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# Set the page title and sidebar title
st.set_page_config(page_title="File Management", page_icon="📂")  
# st.sidebar.title("📂 File Management")

st.title("📂 File Management")

# --- File Upload Section ---
st.subheader("Upload Your Resume(s)")
st.write("Upload a document (TXT, PDF, DOCX)")
uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    file_path = os.path.join(DATA_FOLDER, uploaded_file.name)

    # Save uploaded file permanently
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved: `{file_path}`")

# --- List and Delete Existing Files ---
st.subheader("Manage Uploaded Files")
existing_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(("txt", "pdf", "docx"))]

if existing_files:
    selected_file = st.selectbox("Select a file to delete:", existing_files)
    if st.button("Delete Selected File"):
        os.remove(os.path.join(DATA_FOLDER, selected_file))
        st.success(f"Deleted `{selected_file}`")
        st.experimental_rerun()
else:
    st.info("No files uploaded yet.")
