# Configuration for Streamlit Cloud deployment
import os

# Cloud deployment settings
IS_CLOUD_DEPLOYMENT = True

# LLM Settings for Cloud
# Option 1: Use OpenAI API (requires API key)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set this in Streamlit Cloud secrets
OPENAI_MODEL = "gpt-3.5-turbo"

# Option 2: Use Hugging Face transformers (slower but free)
HF_MODEL_NAME = "microsoft/DialoGPT-medium"

# Option 3: Fallback to rule-based responses
USE_FALLBACK_RESPONSES = True

# Cloud-optimized settings
EMBEDDING_MODEL_CLOUD = "sentence-transformers/all-MiniLM-L6-v2"  # Smaller, faster model
MAX_CHUNKS_CLOUD = 100  # Limit chunks for faster processing
CACHE_EMBEDDINGS = True

# File paths (relative for cloud)
PDF_PATH_CLOUD = "data/KKH Information file.pdf"
LOGO_PATH_CLOUD = "logo/photo_2025-06-16_15-57-21.jpg"
EMBEDDINGS_PATH_CLOUD = "embedded_knowledge.json"

def get_cloud_config():
    """Get configuration optimized for cloud deployment"""
    return {
        "embedding_model": EMBEDDING_MODEL_CLOUD,
        "pdf_path": PDF_PATH_CLOUD,
        "logo_path": LOGO_PATH_CLOUD,
        "embeddings_path": EMBEDDINGS_PATH_CLOUD,
        "max_chunks": MAX_CHUNKS_CLOUD,
        "cache_embeddings": CACHE_EMBEDDINGS,
        "use_openai": bool(OPENAI_API_KEY),
        "openai_model": OPENAI_MODEL,
        "hf_model": HF_MODEL_NAME,
        "use_fallback": USE_FALLBACK_RESPONSES
    }
