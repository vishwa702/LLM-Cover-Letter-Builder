# LLM Cover Letter Builder

A Streamlit-based web application that helps users create professional cover letters using advanced language models. The application leverages RAG (Retrieval Augmented Generation) technology to generate personalized and contextually relevant cover letters.

## Features

- **Cover Letter Generation**: Create professional cover letters using the DeepSeek language model
- **File Management**: Upload and manage resumes and job descriptions
- **Vector Database Integration**: Efficient storage and retrieval of document embeddings
- **Modern UI**: Clean and intuitive Streamlit interface

## Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LLM-Cover-Letter-Builder.git
cd LLM-Cover-Letter-Builder
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your DeepSeek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```

## Project Structure

```
LLM-Cover-Letter-Builder/
├── app.py                 # Main Streamlit application entry point
├── pages/                 # Streamlit pages directory
│   ├── 1_Resume_Builder.py    # Cover letter generation page
│   └── 2_File_Management.py   # File management page
├── data/                  # Directory for storing uploaded files
├── vector_db/            # Vector database for document embeddings
├── requirements.txt      # Project dependencies
└── .env                  # Environment variables (API keys)
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Use the navigation sidebar to access different features:
   - Cover Letter Builder: Generate personalized cover letters
   - File Management: Upload and manage your documents

## Dependencies

- **RAG and LLM Libraries**:
  - spacy
  - openai
  - chromadb
  - sentence-transformers
  - langchain
  - langchain-community
  - langchain-huggingface
  - langchain-deepseek

- **Application Libraries**:
  - streamlit
  - python-docx
  - PyMuPDF

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- DeepSeek for providing the language model
- Streamlit for the web framework
- LangChain for the RAG implementation 