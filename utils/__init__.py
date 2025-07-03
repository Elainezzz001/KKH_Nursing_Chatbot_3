"""
Utility functions for the KKH Nursing Chatbot
"""

from .pdf_processor import *
from .fluid_calculator import *
from .quiz_generator import *
from .llm_interface import *

__all__ = [
    # PDF Processing
    'extract_text_from_pdf',
    'create_embeddings',
    'save_embeddings',
    'load_embeddings',
    'find_relevant_chunk',
    'preprocess_text_for_embedding',
    'chunk_text_by_sentences',
    
    # Fluid Calculator
    'calculate_maintenance_fluid',
    'calculate_resuscitation_fluid',
    'calculate_deficit_fluid',
    'calculate_replacement_fluid',
    'get_fluid_recommendations',
    
    # Quiz Generator
    'generate_quiz_questions',
    'validate_question_quality',
    'shuffle_quiz_questions',
    'calculate_quiz_score',
    'get_quiz_feedback',
    
    # LLM Interface
    'query_lm_studio',
    'format_nursing_prompt',
    'check_lm_studio_connection',
    'get_available_models',
    'generate_nursing_response',
    'validate_response_quality'
]
