#!/bin/bash
# QuizBot Streamlit Launcher

echo "🎓 Starting QuizBot Streamlit Interface..."
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    open -a Ollama 2>/dev/null || echo "Please start Ollama manually"
    sleep 3
fi

# Check if models are installed
echo "🔍 Checking models..."
if ! ollama list | grep -q "llama3.2"; then
    echo "❌ llama3.2 model not found. Please run: ollama pull llama3.2"
    exit 1
fi

if ! ollama list | grep -q "nomic-embed-text"; then
    echo "❌ nomic-embed-text model not found. Please run: ollama pull nomic-embed-text"
    exit 1
fi

echo "✅ All models ready!"
echo ""
echo "🚀 Launching Streamlit app..."
echo "📱 The app will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
streamlit run streamlit_app.py
