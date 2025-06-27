import streamlit as st
import os
from PIL import Image
from utils import *
from config import *

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .quiz-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dee2e6;
    }
    
    .fluid-calc-container {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffeaa7;
    }
    
    .metric-container {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        text-align: center;
    }
    
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'knowledge_embeddings' not in st.session_state:
        st.session_state.knowledge_embeddings = []
    
    if 'knowledge_chunks' not in st.session_state:
        st.session_state.knowledge_chunks = []
    
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

# Load knowledge base
@st.cache_data
def load_knowledge_base():
    if os.path.exists(PDF_PATH):
        embeddings, chunks = initialize_knowledge_base()
        return embeddings, chunks
    else:
        st.error(f"PDF file not found: {PDF_PATH}")
        return [], []

# Main chatbot function
def chatbot_interface():
    # Create header with logo and title
    logo_html = ""
    if os.path.exists(LOGO_PATH):
        try:
            import base64
            with open(LOGO_PATH, "rb") as img_file:
                logo_base64 = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" style="height: 60px; margin-right: 20px; vertical-align: middle;">'
        except:
            pass
    
    st.markdown(f'''
    <div class="main-header">
        <h1 style="display: inline-flex; align-items: center; justify-content: center; margin: 0;">
            {logo_html}{APP_TITLE}
        </h1>
        <p style="margin: 10px 0 0 0;">{APP_DESCRIPTION}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Load knowledge base
    if not st.session_state.knowledge_embeddings:
        with st.spinner("Loading knowledge base..."):
            embeddings, chunks = load_knowledge_base()
            st.session_state.knowledge_embeddings = embeddings
            st.session_state.knowledge_chunks = chunks
    
    # Chat interface
    st.subheader("💬 Chat with the Nursing Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message"><strong>Nursing Assistant:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask me anything about nursing care, procedures, or pediatric guidelines...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Find relevant information and get response
        with st.spinner("Searching knowledge base..."):
            if st.session_state.knowledge_embeddings and st.session_state.knowledge_chunks:
                relevant_chunk = find_most_relevant_chunk(
                    user_input, 
                    st.session_state.knowledge_embeddings, 
                    st.session_state.knowledge_chunks
                )
                
                # Query LLM
                response = query_llm(relevant_chunk, user_input)
                
                # Add bot response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            else:
                response = "Sorry, the knowledge base is not available. Please check if the PDF file exists."
                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()

# Fluid calculator sidebar
def fluid_calculator_sidebar():
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.subheader("💧 Pediatric Fluid Calculator")
    
    with st.sidebar.form("fluid_calculator"):
        weight = st.number_input("Weight (kg)", min_value=0.1, max_value=100.0, value=10.0, step=0.1)
        age = st.number_input("Age (years)", min_value=0, max_value=18, value=5)
        
        scenario = st.selectbox(
            "Scenario",
            ["Maintenance", "Resuscitation", "5% Dehydration", "10% Dehydration"]
        )
        
        calculate_button = st.form_submit_button("Calculate Fluids")
        
        if calculate_button:
            if scenario == "Maintenance":
                fluids_per_day = calculate_maintenance_fluids(weight)
                fluids_per_hour = fluids_per_day / 24
                st.success(f"**Maintenance Fluids:**\n- {fluids_per_day:.0f} mL/day\n- {fluids_per_hour:.1f} mL/hour")
                
            elif scenario == "Resuscitation":
                bolus = calculate_resuscitation_fluids(weight)
                st.success(f"**Resuscitation Bolus:**\n- {bolus:.0f} mL bolus\n- Give over 10-20 minutes")
                
            elif scenario == "5% Dehydration":
                deficit = calculate_deficit_fluids(weight, 5)
                maintenance = calculate_maintenance_fluids(weight)
                total_per_day = deficit + maintenance
                total_per_hour = total_per_day / 24
                st.success(f"**5% Dehydration:**\n- Deficit: {deficit:.0f} mL\n- Maintenance: {maintenance:.0f} mL\n- Total: {total_per_day:.0f} mL/day\n- Rate: {total_per_hour:.1f} mL/hour")
                
            elif scenario == "10% Dehydration":
                deficit = calculate_deficit_fluids(weight, 10)
                maintenance = calculate_maintenance_fluids(weight)
                total_per_day = deficit + maintenance
                total_per_hour = total_per_day / 24
                st.success(f"**10% Dehydration:**\n- Deficit: {deficit:.0f} mL\n- Maintenance: {maintenance:.0f} mL\n- Total: {total_per_day:.0f} mL/day\n- Rate: {total_per_hour:.1f} mL/hour")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Quiz sidebar
def quiz_sidebar():
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.subheader("📚 Nursing Knowledge Quiz")
    
    # Generate quiz if not exists
    if not st.session_state.quiz_questions and st.session_state.knowledge_chunks:
        if st.sidebar.button("Start New Quiz", type="primary"):
            with st.spinner("Generating quiz questions..."):
                st.session_state.quiz_questions = generate_quiz_questions(st.session_state.knowledge_chunks, 15)
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
                st.session_state.quiz_active = True
            st.rerun()
    
    # Display quiz if active
    if st.session_state.quiz_active and st.session_state.quiz_questions:
        current_q_index = st.session_state.quiz_index
        total_questions = len(st.session_state.quiz_questions)
        
        if current_q_index < total_questions:
            question = st.session_state.quiz_questions[current_q_index]
            
            st.sidebar.markdown(f"**Question {current_q_index + 1} of {total_questions}**")
            st.sidebar.markdown(f"*Score: {st.session_state.quiz_score}/{current_q_index}*")
            
            with st.sidebar.form(f"quiz_question_{current_q_index}"):
                st.markdown(f"**{question['question']}**")
                
                user_answer = None
                
                if question['type'] == 'mcq':
                    user_answer = st.radio(
                        "Choose your answer:",
                        options=range(len(question['options'])),
                        format_func=lambda x: question['options'][x],
                        key=f"mcq_{current_q_index}"
                    )
                
                elif question['type'] == 'true_false':
                    user_answer = st.radio(
                        "Choose your answer:",
                        options=[True, False],
                        format_func=lambda x: "True" if x else "False",
                        key=f"tf_{current_q_index}"
                    )
                
                elif question['type'] == 'open_ended':
                    user_answer = st.text_area(
                        "Your answer:",
                        key=f"open_{current_q_index}",
                        height=100
                    )
                
                submitted = st.form_submit_button("Next Question")
                
                if submitted:
                    # Check answer
                    correct = False
                    if question['type'] == 'mcq':
                        correct = user_answer == question['correct']
                    elif question['type'] == 'true_false':
                        correct = user_answer == question['correct']
                    elif question['type'] == 'open_ended':
                        # For open-ended, give credit if answer is not empty
                        correct = len(str(user_answer).strip()) > 10
                    
                    if correct:
                        st.session_state.quiz_score += 1
                    
                    st.session_state.quiz_answers.append({
                        'question': question['question'],
                        'user_answer': user_answer,
                        'correct': correct,
                        'type': question['type']
                    })
                    
                    st.session_state.quiz_index += 1
                    st.rerun()
        
        else:
            # Quiz completed
            st.sidebar.markdown("### 🎉 Quiz Completed!")
            final_score = st.session_state.quiz_score
            total_q = len(st.session_state.quiz_questions)
            percentage = (final_score / total_q) * 100
            
            st.sidebar.markdown(f"**Final Score: {final_score}/{total_q} ({percentage:.1f}%)**")
            
            if percentage >= 80:
                st.sidebar.success("Excellent work! 🌟")
            elif percentage >= 60:
                st.sidebar.info("Good job! 👍")
            else:
                st.sidebar.warning("Keep studying! 📖")
            
            if st.sidebar.button("Retake Quiz"):
                st.session_state.quiz_questions = []
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
                st.session_state.quiz_active = False
                st.rerun()
    
    elif not st.session_state.knowledge_chunks:
        st.sidebar.info("Quiz will be available once the knowledge base is loaded.")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Additional features sidebar
def additional_features_sidebar():
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.subheader("⚙️ Additional Features")
    
    if st.sidebar.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    if st.sidebar.button("Reload Knowledge Base"):
        st.session_state.knowledge_embeddings = []
        st.session_state.knowledge_chunks = []
        st.cache_data.clear()
        st.rerun()
    
    # Display knowledge base stats
    if st.session_state.knowledge_chunks:
        st.sidebar.info(f"📊 Knowledge Base: {len(st.session_state.knowledge_chunks)} chunks loaded")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Main app
def main():
    initialize_session_state()
    
    # Sidebar
    st.sidebar.title("🏥 KKH Nursing Tools")
    
    # Fluid calculator
    fluid_calculator_sidebar()
    
    # Quiz
    quiz_sidebar()
    
    # Additional features
    additional_features_sidebar()
    
    # Main chatbot interface
    chatbot_interface()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>KKH Nursing Chatbot • Built with Streamlit • Powered by AI</p>
            <p><small>For educational purposes only. Always consult official protocols and senior staff.</small></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
