# Cloud-optimized utility functions for Streamlit deployment
import os
import streamlit as st
from streamlit_config import get_cloud_config

def query_llm_cloud(context, question):
    """Cloud-compatible LLM querying with multiple fallback options"""
    config = get_cloud_config()
    
    # Option 1: Try OpenAI API if available
    if config["use_openai"]:
        try:
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            response = openai.ChatCompletion.create(
                model=config["openai_model"],
                messages=[
                    {"role": "system", "content": "You are a helpful nursing chatbot. Only answer based on the context provided. Be concise and accurate."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            st.warning(f"OpenAI API error: {e}")
    
    # Option 2: Try Hugging Face transformers
    try:
        from transformers import pipeline
        
        # Use a lighter conversational model
        generator = pipeline("text-generation", model="microsoft/DialoGPT-small", max_length=200)
        
        prompt = f"Context: {context[:500]}...\nQuestion: {question}\nAnswer:"
        response = generator(prompt, max_length=len(prompt) + 100, num_return_sequences=1)
        
        # Extract the generated part
        generated_text = response[0]['generated_text']
        answer = generated_text[len(prompt):].strip()
        return answer if answer else "I'm processing your question based on the available information."
        
    except Exception as e:
        st.warning(f"Hugging Face model error: {e}")
    
    # Option 3: Fallback to context-based responses
    if config["use_fallback"]:
        return generate_fallback_response(context, question)
    
    return "I'm sorry, I'm unable to process your question at the moment. Please try again later."

def generate_fallback_response(context, question):
    """Generate a simple response based on context matching"""
    question_lower = question.lower()
    context_lower = context.lower()
    
    # Simple keyword matching for common nursing topics
    if any(word in question_lower for word in ['fever', 'temperature']):
        if 'fever' in context_lower or 'temperature' in context_lower:
            return f"Based on the available information: {context[:300]}..."
    
    elif any(word in question_lower for word in ['medication', 'drug', 'medicine']):
        if any(word in context_lower for word in ['medication', 'drug', 'medicine', 'dose']):
            return f"Regarding medication: {context[:300]}..."
    
    elif any(word in question_lower for word in ['fluid', 'hydration', 'dehydration']):
        if any(word in context_lower for word in ['fluid', 'hydration', 'dehydration']):
            return f"About fluid management: {context[:300]}..."
    
    elif any(word in question_lower for word in ['pediatric', 'child', 'infant']):
        if any(word in context_lower for word in ['pediatric', 'child', 'infant', 'baby']):
            return f"For pediatric care: {context[:300]}..."
    
    # Default response with context
    return f"Based on the available information: {context[:400]}... Please consult official protocols for specific guidance."

@st.cache_data
def load_embeddings_cloud():
    """Cloud-optimized embedding loading with caching"""
    from utils import load_embeddings
    try:
        return load_embeddings("embedded_knowledge.json")
    except:
        return [], []

def create_lightweight_app():
    """Create a version of the app optimized for cloud deployment"""
    st.set_page_config(
        page_title="KKH Nursing Chatbot",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 KKH Nursing Chatbot (Cloud)")
    st.caption("AI-powered nursing assistant deployed on Streamlit Cloud")
    
    # Add deployment info
    with st.expander("ℹ️ Deployment Information"):
        st.info("""
        This is a cloud-deployed version of the KKH Nursing Chatbot with optimized performance:
        - ✅ PDF knowledge base processing
        - ✅ Pediatric fluid calculator  
        - ✅ Interactive nursing quiz
        - ⚠️ LLM responses may be limited (see options below)
        """)
        
        config = get_cloud_config()
        if config["use_openai"]:
            st.success("🤖 Using OpenAI GPT for responses")
        elif not config["use_openai"]:
            st.warning("🔄 Using fallback response system (add OpenAI API key for better responses)")
    
    return config
