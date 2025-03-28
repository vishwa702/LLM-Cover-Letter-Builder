import streamlit as st
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import PromptTemplate
import os
import docx
import fitz  # PyMuPDF for PDFs
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()

# Get API key from environment
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    st.error("API key not found! Make sure to set it in the .env file.")
else:
    os.environ["DEEPSEEK_API_KEY"] = api_key  # Optional: Explicitly set for LangChain

# Initialize session state
if 'cover_letter' not in st.session_state:
    st.session_state['cover_letter'] = ''
if 'resume_content' not in st.session_state:
    st.session_state['resume_content'] = ''
if 'job_description' not in st.session_state:
    st.session_state['job_description'] = ''

# Initialize ChromaDB
@st.cache_resource
def get_chroma_db():
    """Initialize and return a persistent ChromaDB instance."""
    chroma_client = chromadb.PersistentClient(path="vector_db")
    return chroma_client

chroma_client = get_chroma_db()
collection = chroma_client.get_or_create_collection(name="documents")

# Initialize LLM
llm = ChatDeepSeek(model="deepseek-chat", temperature=0.7)

# ------- Begin Page -------
st.title("Cover Letter Builder with AI 🤖📝")

# Create a placeholder for the cover letter text area
cover_letter_placeholder = st.empty()

if not st.session_state.cover_letter:
    # --- Build the Cover Letter ---
    st.subheader("Build Your Cover Letter")
    job_description = st.text_area("Enter the job description:", height=120, placeholder='This position is for the role of...')
    st.session_state['job_description'] = job_description

    if job_description.strip():
        # Extract keywords from job description
        keyword_prompt = "Extract the most relevant keywords from this job description that would help match a resume to it. Return just a comma-separated list of keywords."
        keyword_response = llm.invoke([("human", f"{keyword_prompt}\n\nJob Description:\n{job_description}")])
        keywords = [kw.strip() for kw in keyword_response.content.split(',')]
        
        # Display extracted keywords
        st.write("Extracted Keywords:", ", ".join(keywords))
        
        # Use keywords to search vector database
        search_query = " ".join(keywords)
        results = collection.query(
            query_texts=[search_query],
            n_results=3
        )
        
        if results and results['documents'] and results['documents'][0]:
            # Show relevant resume content
            with st.expander("View Relevant Resume Content"):
                for i, (doc, metadata) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
                    st.write(f"**Relevant Section {i+1}:**")
                    st.text_area(f"Content {i+1}", doc, height=150, key=f"resume_section_{i}")
                    st.write(f"Source: {metadata.get('filename', 'Unknown')}")
                    st.write("---")
            
            # Combine relevant resume content for the cover letter
            resume_content = "\n\n".join(results['documents'][0])
            st.session_state['resume_content'] = resume_content
        else:
            st.warning("No matching resume content found. Please upload your resume in the File Management page.")
            resume_content = ""
            st.session_state['resume_content'] = ""

        default_prompt = ("Write a cover letter for the given position. Write up to three paragraphs, "
                         "using simple, personable, and heartfelt language. Use the provided resume content "
                         "to highlight relevant experience and skills.")
        user_input = st.text_area("Enter your prompt:", value=default_prompt, height=80)

        if st.button("Generate") and user_input.strip():
            # Combine all context for the cover letter
            full_prompt = f"""Job Description:
{job_description}

Relevant Resume Content:
{resume_content}

Instructions:
{user_input}

Generate a professional cover letter that highlights the candidate's relevant experience and skills from the resume while addressing the job requirements."""
            
            response = llm.invoke([("human", full_prompt)])

            # Update session state cover letter
            st.session_state.cover_letter = response.content
            st.success("Cover Letter Generated!")

# Display the generated cover letter
if st.session_state.cover_letter:
    cover_letter_placeholder.text_area("Cover Letter", value=st.session_state.cover_letter, height=300)

    # --- Refine the Cover Letter ---
    st.subheader("Refine Your Cover Letter")
    edit_prompt = st.text_input("Give an instruction to improve the letter (e.g., 'Make it more concise'):")

    if st.button("Edit Cover Letter") and edit_prompt.strip():
        edit_template = PromptTemplate(
            input_variables=["existing_letter", "edit_instruction", "job_description", "resume_content"],
            template=(
                "You are refining a cover letter. Here is the current version:\n\n{existing_letter}\n\n"
                "Job Description:\n{job_description}\n\n"
                "Relevant Resume Content:\n{resume_content}\n\n"
                "User's instruction: {edit_instruction}\n\n"
                "Generate the improved version. Return the entire letter, not just a section. Return only the letter, no other text."
            )
        )
        # Combine the prompt template with the LLM using the runnable sequence operator
        edit_chain = edit_template | llm

        response = edit_chain.invoke({
            "existing_letter": st.session_state.cover_letter,
            "edit_instruction": edit_prompt,
            "job_description": st.session_state['job_description'],
            "resume_content": st.session_state['resume_content']
        })

        # Update session state with the new version
        st.session_state.cover_letter = response.content

        # Update the same placeholder with the updated cover letter
        cover_letter_placeholder.text_area("Cover Letter", value=st.session_state.cover_letter, height=300)

        st.success("Cover Letter Updated!")

# Add a button to manage files
if st.button('Manage Files'):
    st.switch_page('pages/File_Management.py')