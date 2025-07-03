import streamlit as st
import os
import sys
from PIL import Image
from sentence_transformers import SentenceTransformer

# Add the current directory to the path to import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import *
    from config import *
except ImportError as e:
    st.error(f"Failed to import utilities: {e}")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title=UI_CONFIG["page_title"],
    page_icon=UI_CONFIG["page_icon"],
    layout=UI_CONFIG["layout"],
    initial_sidebar_state=UI_CONFIG["sidebar_state"]
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #0066cc, #004499);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
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
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'embeddings_loaded' not in st.session_state:
        st.session_state.embeddings_loaded = False
    if 'chunks' not in st.session_state:
        st.session_state.chunks = []
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
    return SentenceTransformer(EMBEDDING_CONFIG["model_name"])

def setup_knowledge_base(model):
    """Setup the knowledge base from PDF"""
    chunks, embeddings = load_embeddings(PDF_CONFIG["embeddings_file"])
    
    if not chunks:
        # Extract from PDF and create embeddings
        pdf_path = PATHS["pdf_file"]
        if os.path.exists(pdf_path):
            chunks = extract_text_from_pdf(pdf_path)
            if chunks:
                embeddings = create_embeddings(chunks, model)
                save_embeddings(chunks, embeddings, PDF_CONFIG["embeddings_file"])
                st.success("Knowledge base created successfully!")
            else:
                st.error("Failed to extract text from PDF")
        else:
            st.error("PDF file not found")
    
    return chunks, embeddings

def render_fluid_calculator():
    """Render the fluid calculator in sidebar"""
    st.header("🧮 Fluid Calculator")
    
    with st.expander("Pediatric Fluid Calculator", expanded=True):
        with st.form("fluid_calc_form"):
            weight = st.number_input(
                "Weight (kg)", 
                min_value=FLUID_CALC_CONFIG["weight_range"]["min"], 
                max_value=FLUID_CALC_CONFIG["weight_range"]["max"], 
                value=10.0, 
                step=0.1
            )
            age = st.number_input(
                "Age (years)", 
                min_value=FLUID_CALC_CONFIG["age_range"]["min"], 
                max_value=FLUID_CALC_CONFIG["age_range"]["max"], 
                value=5, 
                step=1
            )
            scenario = st.selectbox("Scenario", FLUID_CALC_CONFIG["scenarios"])
            
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

def render_quiz_interface():
    """Render the quiz interface in sidebar"""
    st.header("📚 Nursing Knowledge Quiz")
    
    if not st.session_state.quiz_active:
        if st.button("Start Quiz"):
            if st.session_state.chunks:
                with st.spinner("Generating quiz questions..."):
                    st.session_state.quiz_questions = generate_quiz_questions(
                        st.session_state.chunks, 
                        QUIZ_CONFIG["max_questions"]
                    )
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
            correct, total = st.session_state.quiz_score, total_questions
            feedback = get_quiz_feedback(correct, total)
            
            st.markdown(f"""
            <div class="fluid-calc-result">
                <h3>Quiz Completed! 🎉</h3>
                <p><strong>Score:</strong> {correct}/{total}</p>
                <p><strong>Percentage:</strong> {(correct/total)*100:.1f}%</p>
                <p><strong>Feedback:</strong> {feedback}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Retake Quiz"):
                st.session_state.quiz_active = False
                st.session_state.quiz_questions = []
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
                st.rerun()

def render_chat_message(message, is_user=True):
    """Render a single chat message"""
    if is_user:
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-avatar">👤</div>
            <div class="message-content">
                <strong>You:</strong><br>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <strong>KKH Assistant:</strong><br>
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

def handle_user_query(prompt, model):
    """Handle user query and generate response"""
    relevant_chunk = find_relevant_chunk(
        prompt, 
        st.session_state.chunks, 
        st.session_state.embeddings, 
        model,
        threshold=EMBEDDING_CONFIG["similarity_threshold"]
    )
    
    if relevant_chunk:
        # Check if LM Studio is available
        if check_lm_studio_connection():
            response = generate_nursing_response(prompt, relevant_chunk)
        else:
            response = f"Based on the KKH guidelines:\n\n{relevant_chunk[:500]}...\n\n(Note: LM Studio is not available for enhanced responses)"
    else:
        response = "I couldn't find relevant information in the KKH knowledge base to answer your question. Please try rephrasing your question or ask about specific nursing protocols, procedures, or guidelines."
    
    return response

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 KKH Nursing Chatbot</h1>
        <p>Your intelligent nursing assistant for KKH protocols and guidelines</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load embedding model
    model = load_embedding_model()
    
    # Initialize embeddings if not loaded
    if not st.session_state.embeddings_loaded:
        with st.spinner("Loading knowledge base..."):
            chunks, embeddings = setup_knowledge_base(model)
            st.session_state.chunks = chunks
            st.session_state.embeddings = embeddings
            st.session_state.embeddings_loaded = True
    
    # Sidebar
    with st.sidebar:
        render_fluid_calculator()
        render_quiz_interface()
    
    # Main chat interface
    st.header("💬 Chat with KKH Nursing Assistant")
    
    # Check LM Studio connection status
    if check_lm_studio_connection():
        st.success("✅ LM Studio connected and ready")
    else:
        st.warning("⚠️ LM Studio not connected - responses will be basic")
    
    # Display chat history
    for message in st.session_state.messages:
        render_chat_message(message["content"], message["role"] == "user")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about KKH nursing protocols..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_chat_message(prompt, is_user=True)
        
        # Generate response
        with st.spinner("Thinking..."):
            response = handle_user_query(prompt, model)
            
            # Add bot response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            render_chat_message(response, is_user=False)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()
