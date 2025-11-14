#!/usr/bin/env python3
"""
QuizBot - Simplified Streamlit Interface (No ChromaDB dependency issues)
Uses direct file reading instead of vector database for maximum compatibility
"""
import streamlit as st
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# Add nsrag to path
sys.path.insert(0, str(Path(__file__).parent / "nsrag"))

from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
import random
import time
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="QuizBot - AI Quiz Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Question card styling */
    .question-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .question-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    /* Correct answer styling */
    .correct-answer {
        background-color: #d4edda !important;
        border: 2px solid #28a745 !important;
        color: #155724 !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 8px !important;
    }
    
    /* Wrong answer styling */
    .wrong-answer {
        background-color: #f8d7da !important;
        border: 2px solid #dc3545 !important;
        color: #721c24 !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        margin: 0.5rem 0 !important;
        border-radius: 8px !important;
    }
    
    /* Neutral option styling */
    .neutral-option {
        background: #f8f9fa;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        color: #495057;
    }
    
    /* Button-style quiz options */
    div[data-testid="column"] button {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
        color: #2c3e50 !important;
        border: 2px solid #d0d0d0 !important;
        border-radius: 15px !important;
        padding: 1.25rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
        text-align: left !important;
        height: auto !important;
        min-height: 70px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
    }
    
    div[data-testid="column"] button:hover {
        border-color: #667eea !important;
        background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    div[data-testid="column"] button:active {
        transform: translateY(0) !important;
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #e0e0e0;
        border-radius: 10px;
        height: 25px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Timer display */
    .timer-display {
        background: #fff3cd;
        border: 2px solid #ffc107;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        color: #856404;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'parsed_questions' not in st.session_state:
    st.session_state.parsed_questions = []
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = {}
if 'quiz_history' not in st.session_state:
    st.session_state.quiz_history = []
if 'total_quizzes' not in st.session_state:
    st.session_state.total_quizzes = 0
if 'total_correct' not in st.session_state:
    st.session_state.total_correct = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'difficulty_level' not in st.session_state:
    st.session_state.difficulty_level = "Medium"
if 'timer_enabled' not in st.session_state:
    st.session_state.timer_enabled = False
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
if 'parsed_questions' not in st.session_state:
    st.session_state.parsed_questions = []
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = {}

# Initialize model
@st.cache_resource
def load_model():
    return Ollama(model="llama3.2:latest")

@st.cache_data
def load_pdf_content():
    """Load PDF content directly"""
    try:
        from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
        loader = PyPDFDirectoryLoader("nsrag/data")
        documents = loader.load()
        return "\n\n---\n\n".join([doc.page_content for doc in documents[:50]])  # Limit for performance
    except:
        # Fallback: use pre-loaded context (silently)
        return """Network security covers cryptography, authentication, protocols, and security mechanisms.
Key topics include: RSA encryption, symmetric/asymmetric encryption, hash functions, digital signatures,
TLS/SSL protocols, key exchange mechanisms, and various attack vectors."""

try:
    model = load_model()
    pdf_content = load_pdf_content()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

def parse_mcq_questions(text):
    """Parse MCQ questions from text"""
    questions = []
    lines = text.strip().split('\n')
    current_question = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a question line
        if line.startswith('Question') or (line[0].isdigit() and '.' in line[:3]):
            if current_question:
                questions.append(current_question)
            current_question = {
                'question': line.split(':', 1)[-1].strip() if ':' in line else line,
                'options': []
            }
        # Check if it's an option
        elif current_question and line and line[0] in ['A', 'B', 'C', 'D'] and (line[1] == ')' or line[1] == '.'):
            option_text = line[2:].strip()
            current_question['options'].append((line[0], option_text))
    
    if current_question and current_question['options']:
        questions.append(current_question)
    
    return questions

def parse_tf_questions(text):
    """Parse True/False questions from text"""
    questions = []
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a question line
        if line.startswith('Question') or (line[0].isdigit() and '.' in line[:3]):
            question_text = line.split(':', 1)[-1].strip() if ':' in line else line
            # Remove question number if present
            if question_text and question_text[0].isdigit():
                question_text = question_text.split('.', 1)[-1].strip()
            questions.append({
                'question': question_text,
                'options': [('True', 'True'), ('False', 'False')]
            })
    
    return questions

def export_quiz_results():
    """Export quiz results to JSON"""
    if st.session_state.quiz_history:
        export_data = {
            'total_quizzes': st.session_state.total_quizzes,
            'total_questions': st.session_state.total_questions,
            'total_correct': st.session_state.total_correct,
            'accuracy': (st.session_state.total_correct / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0,
            'quiz_history': st.session_state.quiz_history
        }
        return json.dumps(export_data, indent=2)
    return None

def calculate_time_taken():
    """Calculate time taken for quiz"""
    if st.session_state.quiz_start_time:
        return int(time.time() - st.session_state.quiz_start_time)
    return 0

def get_difficulty_context(difficulty):
    """Get context modifier based on difficulty"""
    if difficulty == "Easy":
        return "Generate straightforward questions with clear, direct answers."
    elif difficulty == "Hard":
        return "Generate challenging questions that require deep understanding and critical thinking."
    else:
        return "Generate moderately challenging questions."

def display_progress_stats():
    """Display user progress statistics"""
    if st.session_state.total_quizzes > 0:
        accuracy = (st.session_state.total_correct / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <p class="stats-number">{st.session_state.total_quizzes}</p>
                <p class="stats-label">Quizzes Taken</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <p class="stats-number">{st.session_state.total_correct}/{st.session_state.total_questions}</p>
                <p class="stats-label">Correct Answers</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <p class="stats-number">{accuracy:.1f}%</p>
                <p class="stats-label">Overall Accuracy</p>
            </div>
            """, unsafe_allow_html=True)

def display_timer():
    """Display quiz timer"""
    if st.session_state.timer_enabled and st.session_state.quiz_start_time:
        elapsed = calculate_time_taken()
        minutes = elapsed // 60
        seconds = elapsed % 60
        st.markdown(f"""
        <div class="timer-display">
            Time Elapsed: {minutes:02d}:{seconds:02d}
        </div>
        """, unsafe_allow_html=True)

# Topics list
TOPICS = [
    "OSI architecture", "Symmetric Encryption", "Rijndael", "Entropy",
    "Pseudorandom Number Generator", "Block and Stream Ciphers", "RC4 Stream Cipher",
    "Public-Key Cryptography", "RSA", "Homomorphic encryption",
    "Message authentication", "Hash functions", "Secure Hash Function",
    "Length Extension Attacks", "Message Authentication Code", "HMAC",
    "Authenticated Encryption", "TLS 1.0 Lucky 13 Attack", "Digital Signatures",
    "Hybrid Encryption", "Symmetric key distribution", "Diffie-Hellman Key Exchange"
]

# Header
st.markdown("""
<div class="main-header">
    <h1>QuizBot</h1>
    <p>AI-Powered Network Security Quiz Generator</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Navigation")
    page = st.radio(
        "Choose a mode:",
        ["Generate Quiz", "Ask Questions", "Quiz History", "About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Settings")
    
    if page == "Generate Quiz":
        quiz_type = st.selectbox(
            "Quiz Type",
            ["Multiple Choice (MCQ)", "True/False"],
            key="quiz_type"
        )
        
        topic_mode = st.radio(
            "Topic Selection",
            ["Random Topics", "Specific Topic"],
            key="topic_mode"
        )
        
        if topic_mode == "Specific Topic":
            selected_topic = st.selectbox("Choose Topic", TOPICS, key="selected_topic")
        
        num_questions = st.slider("Number of Questions", 3, 10, 5, key="num_questions")
        
        st.markdown("---")
        st.markdown("### Advanced Options")
        
        difficulty = st.select_slider(
            "Difficulty Level",
            options=["Easy", "Medium", "Hard"],
            value=st.session_state.difficulty_level,
            key="difficulty_selector"
        )
        st.session_state.difficulty_level = difficulty
        
        timer_enabled = st.checkbox("Enable Timer", value=st.session_state.timer_enabled)
        st.session_state.timer_enabled = timer_enabled
        
        if st.session_state.quiz_history:
            st.markdown("---")
            if st.button("Export Results"):
                export_data = export_quiz_results()
                if export_data:
                    st.download_button(
                        label="Download JSON",
                        data=export_data,
                        file_name=f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            if st.button("Clear History"):
                st.session_state.quiz_history = []
                st.session_state.total_quizzes = 0
                st.session_state.total_correct = 0
                st.session_state.total_questions = 0
                st.rerun()
    
    st.markdown("---")
    st.markdown("### Statistics")
    st.metric("Topics Available", len(TOPICS))
    st.metric("Model", "llama3.2")
    
    if st.session_state.total_quizzes > 0:
        accuracy = (st.session_state.total_correct / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0
        st.metric("Overall Accuracy", f"{accuracy:.1f}%")
        st.metric("Quizzes Completed", st.session_state.total_quizzes)

# Main content
if page == "Generate Quiz":
    st.markdown("## Quiz Generator")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Generate New Quiz", use_container_width=True):
            with st.spinner("Generating quiz..."):
                try:
                    # Create prompt based on settings
                    if st.session_state.topic_mode == "Random Topics":
                        topics = random.sample(TOPICS, 2)
                        topic_text = f"on the topics: {', '.join(topics)}"
                    else:
                        topic_text = f"on the topic: {st.session_state.selected_topic}"
                    
                    # Add difficulty context
                    difficulty_context = get_difficulty_context(st.session_state.difficulty_level)
                    
                    if st.session_state.quiz_type == "Multiple Choice (MCQ)":
                        prompt = f"""{difficulty_context}

Based on network security concepts, generate {st.session_state.num_questions} multiple-choice questions {topic_text}.

Each question should have:
- A clear question
- 4 options labeled A, B, C, D
- DO NOT show the correct answer in the output

Format:
Question 1: [question text]
A) [option]
B) [option]
C) [option]
D) [option]

Generate the quiz now (without showing correct answers):"""
                    else:
                        prompt = f"""Based on network security concepts, generate {st.session_state.num_questions} true/false questions {topic_text}.

Format:
Question 1: [statement]

DO NOT show the answers. Generate the quiz now:"""
                    
                    # Use PDF content as context
                    full_prompt = f"Context from network security materials:\n{pdf_content[:3000]}\n\n{prompt}"
                    
                    response = model.invoke(full_prompt)
                    
                    # Parse questions
                    if st.session_state.quiz_type == "Multiple Choice (MCQ)":
                        parsed = parse_mcq_questions(response)
                    else:
                        parsed = parse_tf_questions(response)
                    
                    st.session_state.quiz_data = {
                        'questions': response,
                        'type': st.session_state.quiz_type,
                        'difficulty': st.session_state.difficulty_level,
                        'topics': topics if st.session_state.topic_mode == "Random Topics" else [st.session_state.selected_topic]
                    }
                    st.session_state.parsed_questions = parsed
                    st.session_state.user_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.correct_answers = {}
                    
                    # Initialize timer
                    if st.session_state.timer_enabled:
                        st.session_state.quiz_start_time = time.time()
                    
                    st.success("Quiz generated successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        if st.session_state.quiz_data and not st.session_state.quiz_submitted:
            if st.button("Submit Quiz", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.rerun()
    
    # Display quiz
    if st.session_state.quiz_data and st.session_state.get('parsed_questions'):
        st.markdown("---")
        
        if not st.session_state.quiz_submitted:
            st.markdown("### Your Quiz")
            
            # Display timer if enabled
            if st.session_state.timer_enabled:
                display_timer()
            
            # Display progress
            answered = len(st.session_state.user_answers)
            total = len(st.session_state.parsed_questions)
            progress = (answered / total * 100) if total > 0 else 0
            
            st.markdown(f"""
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress}%">
                    {answered}/{total} Answered
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display each question with button-style options
            for idx, q in enumerate(st.session_state.parsed_questions):
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-text">Question {idx + 1}: {q['question']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                if q['options']:
                    # Create columns for button-style options
                    cols = st.columns(len(q['options']))
                    for col_idx, (opt_letter, opt_text) in enumerate(q['options']):
                        with cols[col_idx]:
                            if st.button(
                                f"{opt_letter}) {opt_text}",
                                key=f"q_{idx}_opt_{opt_letter}",
                                use_container_width=True
                            ):
                                st.session_state.user_answers[idx] = opt_letter
                    
                    # Show selected answer
                    if idx in st.session_state.user_answers:
                        st.info(f"Selected: {st.session_state.user_answers[idx]}")
                
                st.markdown("<br>", unsafe_allow_html=True)
        
        else:
            # Get correct answers first
            if not st.session_state.correct_answers:
                with st.spinner("Evaluating your answers..."):
                    try:
                        # Build answer string
                        user_ans_str = ", ".join([f"{i+1}. {st.session_state.user_answers.get(i, 'No answer')}" 
                                                  for i in range(len(st.session_state.parsed_questions))])
                        
                        eval_prompt = f"""You are a quiz evaluator. 

Here are the quiz questions:
{st.session_state.quiz_data['questions']}

The user's answers are:
{user_ans_str}

For each question, provide ONLY:
1. The correct answer (just the letter for MCQ or True/False)
2. A brief explanation (one sentence)

Format your response as:
Question 1: Correct Answer: [X], Explanation: [brief explanation]
Question 2: Correct Answer: [X], Explanation: [brief explanation]
etc."""
                        
                        evaluation = model.invoke(eval_prompt)
                        
                        # Parse correct answers
                        for idx, line in enumerate(evaluation.split('\n')):
                            if 'Correct Answer:' in line:
                                try:
                                    correct = line.split('Correct Answer:')[1].split(',')[0].strip()
                                    # Extract just the letter/answer
                                    correct = correct.replace('[', '').replace(']', '').strip()
                                    if correct and correct[0] in ['A', 'B', 'C', 'D', 'T', 'F']:
                                        st.session_state.correct_answers[idx] = correct[0]
                                except:
                                    pass
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            # Display results with color coding
            st.markdown("### Quiz Results")
            
            correct_count = 0
            for idx, q in enumerate(st.session_state.parsed_questions):
                user_answer = st.session_state.user_answers.get(idx, 'No answer')
                correct_answer = st.session_state.correct_answers.get(idx, '?')
                is_correct = user_answer == correct_answer
                
                if is_correct:
                    correct_count += 1
                
                # Display question
                st.markdown(f"""
                <div class="question-card">
                    <div class="question-text">Question {idx + 1}: {q['question']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Display options with color coding
                for opt_letter, opt_text in q['options']:
                    is_user_choice = opt_letter == user_answer
                    is_correct_answer = opt_letter == correct_answer
                    
                    if is_correct_answer:
                        style_class = "correct-answer"
                        indicator = " ✓ Correct Answer"
                    elif is_user_choice and not is_correct:
                        style_class = "wrong-answer"
                        indicator = " ✗ Your Answer"
                    else:
                        style_class = "neutral-option"
                        indicator = ""
                    
                    st.markdown(f"""
                    <div class="{style_class}">
                        <strong>{opt_letter})</strong> {opt_text}{indicator}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
            
            # Show score
            total = len(st.session_state.parsed_questions)
            percentage = (correct_count / total * 100) if total > 0 else 0
            time_taken = calculate_time_taken() if st.session_state.timer_enabled else None
            
            st.markdown("---")
            score_text = f"### Score: {correct_count}/{total} ({percentage:.1f}%)"
            if time_taken:
                minutes = time_taken // 60
                seconds = time_taken % 60
                score_text += f" | Time: {minutes:02d}:{seconds:02d}"
            st.markdown(score_text)
            
            # Save to history (only once)
            if 'quiz_saved' not in st.session_state or not st.session_state.quiz_saved:
                quiz_record = {
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'type': st.session_state.quiz_data['type'],
                    'difficulty': st.session_state.quiz_data.get('difficulty', 'Medium'),
                    'topics': st.session_state.quiz_data.get('topics', []),
                    'total_questions': total,
                    'correct_answers': correct_count,
                    'percentage': percentage,
                    'time_taken': time_taken
                }
                st.session_state.quiz_history.append(quiz_record)
                st.session_state.total_quizzes += 1
                st.session_state.total_questions += total
                st.session_state.total_correct += correct_count
                st.session_state.quiz_saved = True
            
            # Display overall progress
            st.markdown("---")
            display_progress_stats()
            
            if st.button("Generate New Quiz"):
                st.session_state.quiz_data = None
                st.session_state.parsed_questions = []
                st.session_state.user_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.correct_answers = {}
                st.session_state.quiz_start_time = None
                st.session_state.quiz_saved = False
                st.rerun()

elif page == "Ask Questions":
    st.markdown("## Ask Questions")
    
    # Chat history
    for question, answer in st.session_state.chat_history:
        with st.container():
            st.markdown(f"**You:** {question}")
            st.markdown(f"**QuizBot:** {answer}")
            st.markdown("---")
    
    # Question input
    with st.form("question_form", clear_on_submit=True):
        question = st.text_input("Your question:", placeholder="e.g., What is RSA encryption?")
        submitted = st.form_submit_button("Ask", use_container_width=True)
        
        if submitted and question:
            with st.spinner("Thinking..."):
                try:
                    prompt = f"""Based on network security concepts, answer this question:

Question: {question}

Context from materials:
{pdf_content[:2000]}

Provide a clear, detailed answer:"""
                    
                    answer = model.invoke(prompt)
                    st.session_state.chat_history.append((question, answer))
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "Quiz History":
    st.markdown("## Quiz History")
    
    if st.session_state.quiz_history:
        # Display overall stats
        display_progress_stats()
        
        st.markdown("---")
        st.markdown("### Recent Quizzes")
        
        # Display each quiz in history (most recent first)
        for idx, quiz in enumerate(reversed(st.session_state.quiz_history)):
            with st.expander(f"Quiz {len(st.session_state.quiz_history) - idx} - {quiz['date']} - Score: {quiz['percentage']:.1f}%"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {quiz['type']}")
                    st.write(f"**Difficulty:** {quiz['difficulty']}")
                    st.write(f"**Topics:** {', '.join(quiz['topics'])}")
                
                with col2:
                    st.write(f"**Questions:** {quiz['total_questions']}")
                    st.write(f"**Correct:** {quiz['correct_answers']}")
                    if quiz.get('time_taken'):
                        minutes = quiz['time_taken'] // 60
                        seconds = quiz['time_taken'] % 60
                        st.write(f"**Time:** {minutes:02d}:{seconds:02d}")
                
                # Progress bar for this quiz
                progress = quiz['percentage']
                color = "#28a745" if progress >= 70 else "#ffc107" if progress >= 50 else "#dc3545"
                st.markdown(f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress}%; background: {color}">
                        {progress:.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Export and clear options
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            export_data = export_quiz_results()
            if export_data:
                st.download_button(
                    label="Export All Results",
                    data=export_data,
                    file_name=f"quiz_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        
        with col2:
            if st.button("Clear All History", use_container_width=True):
                if st.session_state.get('confirm_clear'):
                    st.session_state.quiz_history = []
                    st.session_state.total_quizzes = 0
                    st.session_state.total_correct = 0
                    st.session_state.total_questions = 0
                    st.session_state.confirm_clear = False
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm deletion")
    else:
        st.info("No quiz history yet. Take a quiz to see your progress here!")

else:  # About page
    st.markdown("## About QuizBot")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Topics", len(TOPICS))
    with col2:
        st.metric("Model", "llama3.2")
    with col3:
        st.metric("Interfaces", "5")
    
    st.markdown("---")
    
    st.markdown("""
    ### Features
    
    - **Quiz Generation**: MCQ and True/False quizzes
    - **Q&A System**: Ask questions and get detailed answers
    - **AI-Powered**: Uses llama3.2 for accurate responses
    - **100% Local**: All processing on your machine
    
    ### Technology
    
    - **LLM**: Ollama (llama3.2)
    - **UI**: Streamlit
    - **Framework**: LangChain
    - **Backend**: Python
    
    ### Getting Started
    
    1. Select "Generate Quiz" to create a quiz
    2. Choose your preferences in the sidebar
    3. Click "Generate New Quiz"
    4. Answer the questions and submit!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 1rem;">
    <p>QuizBot - Powered by llama3.2 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)
