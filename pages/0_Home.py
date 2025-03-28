import streamlit as st

# Page configuration
st.set_page_config(
    page_title="LLM Cover Letter Builder - Home",
    page_icon="📝",
    layout="wide"
)

# Main title and description
st.title("📝 LLM Cover Letter Builder")
st.markdown("""
### Your AI-Powered Cover Letter Assistant

Welcome to the LLM Cover Letter Builder, an intelligent tool that helps you create personalized and compelling cover letters using your professional documents and AI technology.

## How It Works

1. **Upload Your Documents**
   - Add multiple versions of your resume or CV
   - Include relevant blogs, articles, and research papers
   - All your documents are securely stored and processed

2. **Build Your Cover Letter**
   - Navigate to the Cover Letter Builder
   - Our AI analyzes your documents to understand your experience
   - Generate tailored cover letters that highlight your relevant skills

## Get Started

Choose an option below to begin:
""")

# Create columns for buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("📁 Go to File Management", use_container_width=True):
        st.switch_page("pages/2_File_Management.py")

with col2:
    if st.button("✍️ Go to Cover Letter Builder", use_container_width=True):
        st.switch_page("pages/1_Resume_Builder.py")

# Additional information
st.markdown("""
---
### Why Choose Our Tool?

- **Smart Analysis**: Our AI understands your professional background from your documents
- **Personalized Content**: Generate cover letters that match your experience and the job requirements
- **Multiple Versions**: Upload different versions of your resume to create varied cover letters
- **Comprehensive Support**: Include all relevant professional content to strengthen your application

### Need Help?

Check out the File Management page to upload your documents, or head directly to the Cover Letter Builder to start creating your personalized cover letter.
""") 