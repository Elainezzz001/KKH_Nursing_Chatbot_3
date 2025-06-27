# Configuration file for KKH Nursing Chatbot

# LLM Settings
LLM_API_URL = "http://localhost:1234/v1/chat/completions"
LLM_MODEL_NAME = "OpenHermes-2.5-Mistral-7B"
LLM_TEMPERATURE = 0.3
LLM_MAX_TOKENS = 500

# Embedding Model Settings
EMBEDDING_MODEL = "intfloat/multilingual-e5-large-instruct"

# File Paths
PDF_PATH = "data/KKH Information file.pdf"
EMBEDDINGS_PATH = "embedded_knowledge.json"
LOGO_PATH = "logo/photo_2025-06-16_15-57-21.jpg"

# Quiz Settings
MAX_QUIZ_QUESTIONS = 15
MIN_SENTENCE_LENGTH = 20
MIN_OPEN_ENDED_ANSWER_LENGTH = 10

# Fluid Calculation Settings (Holliday-Segar method)
# Weight ranges and rates are built into the algorithm
# No configuration needed

# UI Settings
CHAT_HISTORY_LIMIT = 100  # Maximum number of messages to keep in memory

# System Messages
SYSTEM_MESSAGE = "You are a helpful nursing chatbot. Only answer based on the context provided. Be concise and accurate."

# App Metadata
APP_TITLE = "KKH Nursing Chatbot"
APP_ICON = "🏥"
APP_DESCRIPTION = "Your AI assistant for nursing knowledge and pediatric care"
