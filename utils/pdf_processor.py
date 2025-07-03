import pdfplumber
import re
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_from_pdf(pdf_path):
    """
    Extract text and tables from PDF using pdfplumber
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        list: List of text chunks extracted from the PDF
    """
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
        print(f"Error extracting text from PDF: {str(e)}")
        return []
    
    return text_chunks

def create_embeddings(chunks, model):
    """
    Create embeddings for text chunks
    
    Args:
        chunks (list): List of text chunks
        model: SentenceTransformer model
        
    Returns:
        list: List of embeddings
    """
    if not chunks:
        return []
    
    # Add instruction prefix for the embedding model
    instruction = "Represent this document for retrieval: "
    chunks_with_instruction = [instruction + chunk for chunk in chunks]
    
    embeddings = model.encode(chunks_with_instruction, convert_to_tensor=False)
    return embeddings.tolist()

def save_embeddings(chunks, embeddings, filename="embedded_knowledge.json"):
    """
    Save chunks and embeddings to JSON file
    
    Args:
        chunks (list): List of text chunks
        embeddings (list): List of embeddings
        filename (str): Output filename
    """
    data = {
        "chunks": chunks,
        "embeddings": embeddings,
        "metadata": {
            "total_chunks": len(chunks),
            "embedding_dimension": len(embeddings[0]) if embeddings else 0
        }
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_embeddings(filename="embedded_knowledge.json"):
    """
    Load chunks and embeddings from JSON file
    
    Args:
        filename (str): Input filename
        
    Returns:
        tuple: (chunks, embeddings)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data["chunks"], data["embeddings"]
    except FileNotFoundError:
        return [], []

def find_relevant_chunk(question, chunks, embeddings, model, top_k=1, threshold=0.1):
    """
    Find the most relevant chunk for a question
    
    Args:
        question (str): User's question
        chunks (list): List of text chunks
        embeddings (list): List of embeddings
        model: SentenceTransformer model
        top_k (int): Number of top chunks to return
        threshold (float): Minimum similarity threshold
        
    Returns:
        str or None: Most relevant chunk or None if below threshold
    """
    if not chunks or not embeddings:
        return None
    
    # Embed the question
    instruction = "Represent this query for retrieval: "
    question_embedding = model.encode([instruction + question], convert_to_tensor=False)
    
    # Calculate cosine similarity
    embeddings_array = np.array(embeddings)
    similarities = cosine_similarity(question_embedding, embeddings_array)[0]
    
    # Get top k most similar chunks
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    if similarities[top_indices[0]] < threshold:
        return None
    
    return chunks[top_indices[0]]

def preprocess_text_for_embedding(text):
    """
    Preprocess text before embedding
    
    Args:
        text (str): Input text
        
    Returns:
        str: Preprocessed text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters that might interfere with embedding
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    
    return text

def chunk_text_by_sentences(text, max_chunk_size=500, overlap=50):
    """
    Split text into chunks by sentences with overlap
    
    Args:
        text (str): Input text
        max_chunk_size (int): Maximum chunk size in characters
        overlap (int): Overlap between chunks in characters
        
    Returns:
        list: List of text chunks
    """
    sentences = re.split(r'[.!?]+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # If adding this sentence would exceed max size, start a new chunk
        if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Start new chunk with overlap
            current_chunk = current_chunk[-overlap:] + " " + sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks
