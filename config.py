# Configuration settings for KKH Nursing Chatbot

# LM Studio Configuration
LM_STUDIO_CONFIG = {
    "base_url": "http://localhost:1234",
    "model_name": "OpenHermes-2.5-Mistral-7B",
    "timeout": 30,
    "default_temperature": 0.7,
    "max_tokens": 500
}

# Embedding Model Configuration
EMBEDDING_CONFIG = {
    "model_name": "intfloat/multilingual-e5-large-instruct",
    "similarity_threshold": 0.1,
    "top_k_results": 1
}

# PDF Processing Configuration
PDF_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "min_chunk_length": 20,
    "embeddings_file": "embedded_knowledge.json"
}

# Quiz Configuration
QUIZ_CONFIG = {
    "max_questions": 15,
    "question_types": ["mcq", "true_false", "open_ended"],
    "mcq_options": 4,
    "min_chunk_length_for_quiz": 50
}

# Fluid Calculator Configuration
FLUID_CALC_CONFIG = {
    "weight_range": {"min": 0.1, "max": 100.0},
    "age_range": {"min": 0, "max": 18},
    "scenarios": ["Maintenance", "Resuscitation", "Deficit (5%)", "Deficit (10%)"]
}

# UI Configuration
UI_CONFIG = {
    "page_title": "KKH Nursing Chatbot",
    "page_icon": "🏥",
    "layout": "wide",
    "sidebar_state": "expanded",
    "theme": {
        "primary_color": "#0066cc",
        "secondary_color": "#004499",
        "background_color": "#f8f9fa"
    }
}

# File Paths
PATHS = {
    "pdf_file": "data/KKH Information file.pdf",
    "logo": "logo/photo_2025-06-16_15-57-21.jpg",
    "embeddings": "embedded_knowledge.json",
    "chat_history": "chat_history.json"
}

# System Messages
SYSTEM_MESSAGES = {
    "default": "You are a helpful nursing chatbot. Only answer based on the context provided.",
    "detailed": "You are an expert nursing educator. Provide detailed, evidence-based answers using only the context provided. Include step-by-step procedures when applicable.",
    "quick": "You are a nursing assistant. Provide concise, actionable answers based on the context provided. Focus on immediate actions and key points."
}
