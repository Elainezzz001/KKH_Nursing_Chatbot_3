import streamlit as st
import pdfplumber
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import re
import random
from PIL import Image
import os

# Configure Streamlit page
st.set_page_config(
    page_title="KKH Nursing Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0066cc, #004499);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
    }
    
    .main-header .logo {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid white;
        flex-shrink: 0;
    }
    
    .main-header .header-content {
        flex: 1;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        color: white;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
        color: white;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: flex-start;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .message-content {
        flex: 1;
        margin-left: 1rem;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .quiz-question {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin-bottom: 1rem;
    }
    
    .fluid-calc-result {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin-top: 1rem;
    }
    
    .sample-question-btn {
        background-color: #f0f8ff;
        border: 1px solid #0066cc;
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.2rem 0;
        text-align: left;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .sample-question-btn:hover {
        background-color: #e6f3ff;
        border-color: #004499;
    }
    
    .quick-start-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #0066cc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'embeddings_loaded' not in st.session_state:
    st.session_state.embeddings_loaded = False
if 'chunks' not in st.session_state:
    st.session_state.chunks = []
if 'process_sample_question' not in st.session_state:
    st.session_state.process_sample_question = None
if 'embeddings' not in st.session_state:
    st.session_state.embeddings = []
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'quiz_index' not in st.session_state:
    st.session_state.quiz_index = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False

# Load embedding model
@st.cache_resource
def load_embedding_model():
    """Load the multilingual embedding model"""
    try:
        return SentenceTransformer('intfloat/multilingual-e5-large-instruct')
    except Exception as e:
        st.error(f"Error loading embedding model: {e}")
        return None

# PDF Processing Functions
def extract_text_from_pdf(pdf_path):
    """Extract text and tables from PDF using pdfplumber"""
    text_chunks = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text()
                if text:
                    # Clean and split text into chunks
                    text = re.sub(r'\s+', ' ', text).strip()
                    # Split into sentences/chunks
                    sentences = re.split(r'[.!?]+', text)
                    for sentence in sentences:
                        if len(sentence.strip()) > 20:  # Filter out very short chunks
                            text_chunks.append(sentence.strip())
                
                # Extract tables
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        # Convert table to text
                        table_text = ""
                        for row in table:
                            if row:
                                table_text += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
                        if table_text.strip():
                            text_chunks.append(f"Table from page {page_num + 1}:\n{table_text.strip()}")
    
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return []
    
    return text_chunks

def create_embeddings(chunks, model):
    """Create embeddings for text chunks"""
    if not chunks or model is None:
        return []
    
    try:
        # Add instruction prefix for the embedding model
        instruction = "Represent this document for retrieval: "
        chunks_with_instruction = [instruction + chunk for chunk in chunks]
        
        embeddings = model.encode(chunks_with_instruction, convert_to_tensor=False)
        return embeddings.tolist()
    except Exception as e:
        st.error(f"Error creating embeddings: {e}")
        return []

def save_embeddings(chunks, embeddings, filename="embedded_knowledge.json"):
    """Save chunks and embeddings to JSON file"""
    try:
        data = {
            "chunks": chunks,
            "embeddings": embeddings
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving embeddings: {e}")

def load_embeddings(filename="embedded_knowledge.json"):
    """Load chunks and embeddings from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["chunks"], data["embeddings"]
    except FileNotFoundError:
        return [], []
    except Exception as e:
        st.error(f"Error loading embeddings: {e}")
        return [], []

def find_relevant_chunk(question, chunks, embeddings, model, top_k=1):
    """Find the most relevant chunk for a question"""
    if not chunks or not embeddings or model is None:
        return None
    
    try:
        # Embed the question
        instruction = "Represent this query for retrieval: "
        question_embedding = model.encode([instruction + question], convert_to_tensor=False)
        
        # Calculate cosine similarity
        embeddings_array = np.array(embeddings)
        similarities = cosine_similarity(question_embedding, embeddings_array)[0]
        
        # Get top k most similar chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        if similarities[top_indices[0]] < 0.1:  # Threshold for relevance
            return None
        
        return chunks[top_indices[0]]
    except Exception as e:
        st.error(f"Error finding relevant chunk: {e}")
        return None

def query_lm_studio(prompt, system_message="You are a helpful nursing chatbot. Only answer based on the context provided."):
    """Query LM Studio API"""
    url = "http://localhost:1234/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "OpenHermes-2.5-Mistral-7B",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error connecting to LM Studio: {str(e)}"

# Fluid Calculator Functions
def calculate_maintenance_fluid(weight_kg, age_years):
    """Calculate maintenance fluid using Holliday-Segar method"""
    if weight_kg <= 10:
        ml_per_day = weight_kg * 100
    elif weight_kg <= 20:
        ml_per_day = 1000 + (weight_kg - 10) * 50
    else:
        ml_per_day = 1500 + (weight_kg - 20) * 20
    
    ml_per_hour = ml_per_day / 24
    return ml_per_day, ml_per_hour

def calculate_resuscitation_fluid(weight_kg):
    """Calculate resuscitation fluid (20mL/kg bolus)"""
    bolus_ml = weight_kg * 20
    return bolus_ml

def calculate_deficit_fluid(weight_kg, dehydration_percent):
    """Calculate deficit fluid based on dehydration percentage"""
    deficit_ml = weight_kg * 1000 * (dehydration_percent / 100)
    return deficit_ml

# Quiz Functions
def generate_quiz_questions(chunks, num_questions=15):
    """Generate quiz questions from PDF chunks"""
    if not chunks:
        return []
    
    # Filter chunks that are suitable for questions (not too short, not tables)
    suitable_chunks = [chunk for chunk in chunks if len(chunk) > 50 and "Table from page" not in chunk]
    
    if len(suitable_chunks) < num_questions:
        num_questions = len(suitable_chunks)
    
    if num_questions == 0:
        return []
    
    selected_chunks = random.sample(suitable_chunks, min(num_questions, len(suitable_chunks)))
    
    questions = []
    question_types = ["mcq", "true_false", "open_ended"]
    
    for i, chunk in enumerate(selected_chunks):
        question_type = random.choice(question_types)
        
        if question_type == "mcq":
            # Generate MCQ
            question = {
                "type": "mcq",
                "question": f"Based on the following information, which statement is most accurate?\n\n{chunk[:200]}...",
                "options": [
                    "Option A: This is correct based on the context",
                    "Option B: This is partially correct",
                    "Option C: This is incorrect",
                    "Option D: This needs more information"
                ],
                "correct_answer": 0,
                "context": chunk
            }
        elif question_type == "true_false":
            # Generate True/False
            question = {
                "type": "true_false",
                "question": f"True or False: The following statement is accurate according to the nursing guidelines?\n\n{chunk[:150]}...",
                "correct_answer": True,
                "context": chunk
            }
        else:
            # Generate open-ended
            question = {
                "type": "open_ended",
                "question": f"Based on the following information, explain the key nursing considerations:\n\n{chunk[:200]}...",
                "context": chunk
            }
        
        questions.append(question)
    
    return questions

def check_lm_studio_connection():
    """Check if LM Studio is available"""
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        return response.status_code == 200
    except:
        return False

# Main Application
def main():
    # Load and display logo
    logo_path = "logo/photo_2025-06-16_15-57-21.jpg"
    
    # Header with integrated logo
    if os.path.exists(logo_path):
        try:
            import base64
            from io import BytesIO
            
            # Convert image to base64 for embedding in HTML
            logo_image = Image.open(logo_path)
            buffered = BytesIO()
            logo_image.save(buffered, format="PNG")
            logo_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Create header with logo and title using pure HTML
            st.markdown(f"""
            <div class="main-header">
                <div class="header-content">
                    <h1><img src="data:image/png;base64,{logo_base64}" class="logo" alt="KKH Logo"> KKH Nursing Chatbot</h1>
                    <p>Your intelligent nursing assistant for KKH protocols and guidelines</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error loading logo: {e}")
            # Fallback header without logo
            st.markdown("""
            <div class="main-header">
                <div class="header-content">
                    <h1>🏥 KKH Nursing Chatbot</h1>
                    <p>Your intelligent nursing assistant for KKH protocols and guidelines</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Fallback header without logo
        st.markdown("""
        <div class="main-header">
            <div class="header-content">
                <h1>🏥 KKH Nursing Chatbot</h1>
                <p>Your intelligent nursing assistant for KKH protocols and guidelines</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Load embedding model
    model = load_embedding_model()
    
    if model is None:
        st.error("Failed to load embedding model. Some features may not work.")
        return
    
    # Initialize embeddings if not loaded
    if not st.session_state.embeddings_loaded:
        with st.spinner("Loading knowledge base..."):
            chunks, embeddings = load_embeddings()
            
            if not chunks:
                # Extract from PDF and create embeddings
                pdf_path = "data/KKH Information file.pdf"
                if os.path.exists(pdf_path):
                    chunks = extract_text_from_pdf(pdf_path)
                    if chunks:
                        embeddings = create_embeddings(chunks, model)
                        save_embeddings(chunks, embeddings)
                        st.success("Knowledge base created successfully!")
                    else:
                        st.error("Failed to extract text from PDF")
                else:
                    st.error("PDF file not found")
            
            st.session_state.chunks = chunks
            st.session_state.embeddings = embeddings
            st.session_state.embeddings_loaded = True
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="quick-start-section">', unsafe_allow_html=True)
        st.header("💡 Quick Start Questions")
        
        with st.expander("Sample Nursing Questions", expanded=False):
            st.markdown("**Click on any question to ask the chatbot:**")
            
            sample_questions = [
                "What are the standard vital signs monitoring procedures?",
                "How do I calculate pediatric dosage for medications?",
                "What are the infection control protocols?",
                "How should I handle emergency situations in pediatric care?",
                "What are the proper hand hygiene procedures?",
                "How do I assess pain in pediatric patients?",
                "What are the wound care best practices?",
                "How do I manage IV therapy safely?",
                "What are the fall prevention strategies?",
                "How do I document patient care properly?"
            ]
            
            for i, question in enumerate(sample_questions):
                if st.button(f"❓ {question}", key=f"sample_q_{i}", use_container_width=True):
                    # Mark question for processing (don't add to messages yet)
                    st.session_state['process_sample_question'] = question
                    # Force immediate rerun to process the question
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.header("🧮 Fluid Calculator")
        
        with st.expander("Pediatric Fluid Calculator", expanded=True):
            with st.form("fluid_calc_form"):
                weight = st.number_input("Weight (kg)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
                age = st.number_input("Age (years)", min_value=0, max_value=18, value=5, step=1)
                scenario = st.selectbox("Scenario", ["Maintenance", "Resuscitation", "Deficit (5%)", "Deficit (10%)"])
                
                calculate_button = st.form_submit_button("Calculate")
                
                if calculate_button:
                    if scenario == "Maintenance":
                        ml_day, ml_hour = calculate_maintenance_fluid(weight, age)
                        st.markdown(f"""
                        <div class="fluid-calc-result">
                            <h4>Maintenance Fluid Requirements</h4>
                            <p><strong>Daily:</strong> {ml_day:.0f} mL/day</p>
                            <p><strong>Hourly:</strong> {ml_hour:.1f} mL/hour</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif scenario == "Resuscitation":
                        bolus_ml = calculate_resuscitation_fluid(weight)
                        st.markdown(f"""
                        <div class="fluid-calc-result">
                            <h4>Resuscitation Fluid</h4>
                            <p><strong>Bolus:</strong> {bolus_ml:.0f} mL (20mL/kg)</p>
                        </div>
                        """, unsafe_allow_html=True)
                    elif "Deficit" in scenario:
                        dehydration_percent = 5 if "5%" in scenario else 10
                        deficit_ml = calculate_deficit_fluid(weight, dehydration_percent)
                        st.markdown(f"""
                        <div class="fluid-calc-result">
                            <h4>Deficit Fluid ({dehydration_percent}% dehydration)</h4>
                            <p><strong>Deficit:</strong> {deficit_ml:.0f} mL</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        st.header("📚 Nursing Knowledge Quiz")
        
        if not st.session_state.quiz_active:
            if st.button("Start Quiz"):
                if st.session_state.chunks:
                    with st.spinner("Generating quiz questions..."):
                        st.session_state.quiz_questions = generate_quiz_questions(st.session_state.chunks)
                        st.session_state.quiz_index = 0
                        st.session_state.quiz_score = 0
                        st.session_state.quiz_answers = []
                        st.session_state.quiz_active = True
                        st.rerun()
                else:
                    st.error("No knowledge base loaded")
        
        if st.session_state.quiz_active and st.session_state.quiz_questions:
            current_q_index = st.session_state.quiz_index
            total_questions = len(st.session_state.quiz_questions)
            
            if current_q_index < total_questions:
                question = st.session_state.quiz_questions[current_q_index]
                
                st.markdown(f"""
                <div class="quiz-question">
                    <h4>Question {current_q_index + 1} of {total_questions}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form(f"quiz_form_{current_q_index}"):
                    st.write(question["question"])
                    
                    if question["type"] == "mcq":
                        answer = st.radio("Choose your answer:", question["options"], key=f"mcq_{current_q_index}")
                    elif question["type"] == "true_false":
                        answer = st.radio("Choose your answer:", ["True", "False"], key=f"tf_{current_q_index}")
                    else:
                        answer = st.text_area("Your answer:", key=f"open_{current_q_index}")
                    
                    if st.form_submit_button("Next Question"):
                        st.session_state.quiz_answers.append(answer)
                        
                        # Check answer for scoring
                        if question["type"] == "mcq":
                            if answer in question["options"]:
                                if question["options"].index(answer) == question["correct_answer"]:
                                    st.session_state.quiz_score += 1
                        elif question["type"] == "true_false":
                            if (answer == "True") == question["correct_answer"]:
                                st.session_state.quiz_score += 1
                        
                        st.session_state.quiz_index += 1
                        st.rerun()
            else:
                # Quiz completed
                st.markdown(f"""
                <div class="fluid-calc-result">
                    <h3>Quiz Completed! 🎉</h3>
                    <p><strong>Score:</strong> {st.session_state.quiz_score}/{total_questions}</p>
                    <p><strong>Percentage:</strong> {(st.session_state.quiz_score/total_questions)*100:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Retake Quiz"):
                    st.session_state.quiz_active = False
                    st.session_state.quiz_questions = []
                    st.session_state.quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answers = []
                    st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with KKH Nursing Assistant")
    
    # Check LM Studio connection
    if check_lm_studio_connection():
        st.success("✅ LM Studio connected - Enhanced responses available")
    else:
        st.warning("⚠️ LM Studio not connected - Basic responses only")
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <div class="message-avatar">👤</div>
                <div class="message-content">
                    <strong>You:</strong><br>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <strong>KKH Assistant:</strong><br>
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about KKH nursing protocols..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <strong>You:</strong><br>
                {prompt}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate response
        with st.spinner("Thinking..."):
            relevant_chunk = find_relevant_chunk(prompt, st.session_state.chunks, st.session_state.embeddings, model)
            
            if relevant_chunk:
                if check_lm_studio_connection():
                    # Create prompt for LM Studio
                    lm_prompt = f"Context:\n{relevant_chunk}\n\nQuestion: {prompt}"
                    response = query_lm_studio(lm_prompt)
                else:
                    # Basic response without LM Studio
                    response = f"Based on the KKH guidelines:\n\n{relevant_chunk[:500]}..."
            else:
                response = "I couldn't find relevant information in the KKH knowledge base to answer your question. Please try rephrasing your question or ask about specific nursing protocols, procedures, or guidelines."
            
            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display bot response
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <strong>KKH Assistant:</strong><br>
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Handle sample question processing
    if 'process_sample_question' in st.session_state and st.session_state['process_sample_question']:
        prompt = st.session_state['process_sample_question']
        
        # Clear the flag to prevent reprocessing
        st.session_state['process_sample_question'] = None
        
        # Add user message to chat history (only once)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <strong>You:</strong><br>
                {prompt}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate response
        with st.spinner("Thinking..."):
            relevant_chunk = find_relevant_chunk(prompt, st.session_state.chunks, st.session_state.embeddings, model)
            
            if relevant_chunk:
                if check_lm_studio_connection():
                    # Create prompt for LM Studio
                    lm_prompt = f"Context:\n{relevant_chunk}\n\nQuestion: {prompt}"
                    response = query_lm_studio(lm_prompt)
                else:
                    # Basic response without LM Studio
                    response = f"Based on the KKH guidelines:\n\n{relevant_chunk[:500]}..."
            else:
                response = "I couldn't find relevant information in the KKH knowledge base to answer your question. Please try rephrasing your question or ask about specific nursing protocols, procedures, or guidelines."
            
            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Display bot response
            st.markdown(f"""
            <div class="chat-message bot-message">
                <div class="message-avatar">🤖</div>
                <div class="message-content">
                    <strong>KKH Assistant:</strong><br>
                    {response}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
