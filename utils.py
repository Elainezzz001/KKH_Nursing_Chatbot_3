# Helper functions for the KKH Nursing Chatbot
import json
import os
import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import re
import random
from config import *

def load_and_process_pdf(pdf_path):
    """Load PDF and extract text and tables"""
    chunks = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text()
                if text:                    # Clean and split text into sentences
                    sentences = text.replace('\n', ' ').split('.')
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if len(sentence) > MIN_SENTENCE_LENGTH:  # Only keep meaningful sentences
                            chunks.append(f"Page {page_num + 1}: {sentence}")
                
                # Extract tables
                tables = page.extract_tables()
                for table_num, table in enumerate(tables):
                    if table:
                        table_text = f"Table {table_num + 1} on Page {page_num + 1}:\n"
                        for row in table:
                            if row:
                                table_text += " | ".join([str(cell) if cell else "" for cell in row]) + "\n"
                        chunks.append(table_text)
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []
    
    return chunks

def create_embeddings(chunks, model_name=EMBEDDING_MODEL):
    """Create embeddings for text chunks"""
    if not chunks:
        return [], []
    
    try:
        model = SentenceTransformer(model_name)
        embeddings = model.encode(chunks, convert_to_tensor=False)
        return embeddings.tolist(), chunks
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        return [], chunks

def save_embeddings(embeddings, chunks, filepath="embedded_knowledge.json"):
    """Save embeddings and chunks to JSON file"""
    data = {
        "embeddings": embeddings,
        "chunks": chunks
    }
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving embeddings: {e}")
        return False

def load_embeddings(filepath="embedded_knowledge.json"):
    """Load embeddings and chunks from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["embeddings"], data["chunks"]
    except Exception as e:
        print(f"Error loading embeddings: {e}")
        return [], []

def find_most_relevant_chunk(question, embeddings, chunks, model_name=EMBEDDING_MODEL):
    """Find the most relevant chunk for a given question"""
    if not embeddings or not chunks:
        return "No knowledge base available."
    
    try:
        model = SentenceTransformer(model_name)
        question_embedding = model.encode([question], convert_to_tensor=False)
        
        # Calculate cosine similarities
        similarities = cosine_similarity(question_embedding, embeddings)[0]
        
        # Find the most similar chunk
        best_idx = np.argmax(similarities)
        
        return chunks[best_idx]
    except Exception as e:
        print(f"Error finding relevant chunk: {e}")
        return "Error retrieving relevant information."

def query_llm(context, question, api_url=LLM_API_URL):
    """Query the LLM with context and question"""
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": LLM_MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        "temperature": LLM_TEMPERATURE,
        "max_tokens": LLM_MAX_TOKENS
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        return f"Error connecting to LLM: {e}"
    except Exception as e:
        return f"Error processing LLM response: {e}"

def calculate_maintenance_fluids(weight_kg):
    """Calculate maintenance fluids using Holliday-Segar method"""
    if weight_kg <= 10:
        return weight_kg * 100  # 100 mL/kg/day
    elif weight_kg <= 20:
        return 1000 + (weight_kg - 10) * 50  # 1000 + 50 mL/kg/day for kg 11-20
    else:
        return 1500 + (weight_kg - 20) * 20  # 1500 + 20 mL/kg/day for kg >20

def calculate_resuscitation_fluids(weight_kg):
    """Calculate resuscitation fluids (20 mL/kg bolus)"""
    return weight_kg * 20

def calculate_deficit_fluids(weight_kg, dehydration_percent):
    """Calculate deficit fluids based on dehydration percentage"""
    deficit_ml = weight_kg * 1000 * (dehydration_percent / 100)
    return deficit_ml

def generate_quiz_questions(chunks, num_questions=15):
    """Generate quiz questions from PDF content"""
    if not chunks:
        return []
    
    questions = []
    used_chunks = set()
    
    # Question templates
    mcq_templates = [
        "According to the information, what is the primary {topic}?",
        "Which of the following is correct regarding {topic}?",
        "What should a nurse do when {topic}?",
        "The recommended approach for {topic} is:",
    ]
    
    true_false_templates = [
        "True or False: {statement}",
        "Is this statement correct: {statement}?",
    ]
    
    open_ended_templates = [
        "Explain the procedure for {topic}.",
        "What are the key considerations when {topic}?",
        "Describe the nursing care required for {topic}.",
    ]
    
    # Extract key topics and statements from chunks
    for i in range(min(num_questions, len(chunks))):
        if i in used_chunks:
            continue
            
        chunk = chunks[i]
        used_chunks.add(i)
        
        # Clean the chunk
        clean_chunk = re.sub(r'Page \d+:', '', chunk).strip()
        
        if len(clean_chunk) < 30:
            continue
        
        # Generate different types of questions
        question_type = random.choice(['mcq', 'true_false', 'open_ended'])
        
        if question_type == 'mcq':
            # Extract a key concept
            words = clean_chunk.split()
            if len(words) > 10:
                topic = ' '.join(words[:5])
                template = random.choice(mcq_templates)
                question_text = template.format(topic=topic.lower())
                
                # Generate options (simplified for demo)
                correct_answer = clean_chunk[:100] + "..."
                wrong_answers = [
                    "This is not mentioned in the guidelines",
                    "The opposite of the recommended approach",
                    "An outdated practice no longer recommended"
                ]
                
                options = [correct_answer] + wrong_answers
                random.shuffle(options)
                correct_index = options.index(correct_answer)
                
                questions.append({
                    'type': 'mcq',
                    'question': question_text,
                    'options': options,
                    'correct': correct_index,
                    'context': clean_chunk
                })
        
        elif question_type == 'true_false':
            # Create a true/false statement
            template = random.choice(true_false_templates)
            statement = clean_chunk.split('.')[0] if '.' in clean_chunk else clean_chunk[:50]
            question_text = template.format(statement=statement)
            
            questions.append({
                'type': 'true_false',
                'question': question_text,
                'correct': True,  # Since we're using actual content, it's true
                'context': clean_chunk
            })
        
        else:  # open_ended
            words = clean_chunk.split()
            if len(words) > 5:
                topic = ' '.join(words[:3])
                template = random.choice(open_ended_templates)
                question_text = template.format(topic=topic.lower())
                
                questions.append({
                    'type': 'open_ended',
                    'question': question_text,
                    'answer': clean_chunk,
                    'context': clean_chunk
                })
    
    return questions[:num_questions]

def initialize_knowledge_base(pdf_path=PDF_PATH, embeddings_path=EMBEDDINGS_PATH):
    """Initialize the knowledge base if it doesn't exist"""
    if not os.path.exists(embeddings_path):
        print("Creating knowledge base...")
        chunks = load_and_process_pdf(pdf_path)
        if chunks:
            embeddings, _ = create_embeddings(chunks)
            if embeddings:
                save_embeddings(embeddings, chunks, embeddings_path)
                print(f"Knowledge base created with {len(chunks)} chunks")
                return embeddings, chunks
        print("Failed to create knowledge base")
        return [], []
    else:
        print("Loading existing knowledge base...")
        return load_embeddings(embeddings_path)
