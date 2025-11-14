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

## Database Management

### Rebuild Database

If you need to rebuild the vector database:

```bash
cd nsrag
python3 populate_database.py --reset
```

This will:
1. Clear existing database
2. Load all PDFs from `nsrag/data/`
3. Generate embeddings
4. Store in ChromaDB

## Troubleshooting

### Ollama Not Running
```bash
# Check status
pgrep -fl ollama

# Start Ollama (macOS)
open -a Ollama
```

### Models Not Found
```bash
# List installed models
ollama list

# Install missing models
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Port Already in Use
```bash
# Use different port
streamlit run streamlit_simple.py --server.port 8502
```

### Database Issues
```bash
# Rebuild database
cd nsrag
python3 populate_database.py --reset
```

## Performance

- **First Load**: 5-10 seconds (model initialization)
- **Quiz Generation**: 10-30 seconds
- **Question Answering**: 5-15 seconds
- **Database**: 281 document chunks indexed

## Features in Detail

### Quiz Interface
- Rounded button options for better UX
- Hover effects and animations
- Color-coded results after submission
- Score display with percentage
- Detailed explanations for each answer

### Q&A System
- Context-aware responses using RAG
- Chat history maintained during session
- Detailed answers with examples
- Based on 30 PDF documents

## Contributing

This is an educational project for network security learning. Feel free to:
- Add more PDF documents to `nsrag/data/`
- Customize topics in `streamlit_simple.py`
- Modify prompts in `nsrag/prompt_templates.py`
- Enhance the UI styling

## License

Educational use only.

## Acknowledgments

- Built with Ollama and LangChain
- Uses llama3.2 for text generation
- Powered by ChromaDB for vector storage
- UI created with Streamlit

---

**Start Learning**: `streamlit run streamlit_simple.py`
