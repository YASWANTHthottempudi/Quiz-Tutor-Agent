# QuizBot - AI-Powered Network Security Quiz Generator

An intelligent quiz generation system powered by llama3.2 that creates interactive quizzes on network security topics.

## Features

- **Interactive Quiz Interface**: Beautiful Streamlit web UI with rounded button options
- **Multiple Quiz Types**: Multiple Choice Questions (MCQ) and True/False
- **Smart Topic Selection**: Choose from 22+ topics or let AI pick randomly
- **Instant Evaluation**: Color-coded results (Green for correct, Red for incorrect)
- **Q&A System**: Ask open-ended questions about network security
- **100% Local**: All processing happens on your machine, no internet required

## Quick Start

### Prerequisites

1. **Ollama** installed and running
2. **Python 3.9+** with required packages
3. **Models installed**:
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

### Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure Ollama is running:
   ```bash
   # macOS
   open -a Ollama
   
   # Check if running
   pgrep -fl ollama
   ```

### Launch

```bash
streamlit run streamlit_simple.py
```

Access at: **http://localhost:8501**

## Usage

### Generate a Quiz

1. Select quiz type (MCQ or True/False)
2. Choose topic mode:
   - **Random Topics**: AI selects 2 topics automatically
   - **Specific Topic**: Choose from dropdown
3. Set number of questions (3-10)
4. Click "Generate New Quiz"
5. Click rounded buttons to select answers
6. Submit to see results with explanations

### Ask Questions

1. Navigate to "Ask Questions" tab
2. Type your question about network security
3. Get detailed AI-generated answers

## Topics Covered

- OSI Architecture
- Symmetric & Asymmetric Encryption
- RSA, AES, Rijndael
- Hash Functions (SHA, MD5, HMAC)
- Digital Signatures
- TLS/SSL Protocols
- Diffie-Hellman Key Exchange
- Message Authentication
- Cryptographic Attacks
- And 13+ more topics

## Project Structure

```
QuizBot-main/
├── streamlit_simple.py          # Main Streamlit application
├── run_streamlit.sh             # Launch script
├── START_HERE.txt               # Quick start guide
├── requirements.txt             # Python dependencies
├── nsrag/
│   ├── data/                    # PDF documents (30 files)
│   ├── chroma/                  # Vector database
│   ├── populate_database.py    # Database builder
│   ├── get_embedding_function.py
│   └── prompt_templates.py
└── nsreact/                     # React frontend (optional)
```

## Technology Stack

- **LLM**: Ollama (llama3.2:latest)
- **Embeddings**: nomic-embed-text
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **UI**: Streamlit
- **Backend**: Python




