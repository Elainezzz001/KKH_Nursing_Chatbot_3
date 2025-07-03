import requests
import json

def query_lm_studio(prompt, system_message="You are a helpful nursing chatbot. Only answer based on the context provided.", temperature=0.7, max_tokens=500):
    """
    Query LM Studio API
    
    Args:
        prompt (str): User's question with context
        system_message (str): System message for the model
        temperature (float): Temperature for response generation
        max_tokens (int): Maximum tokens in response
        
    Returns:
        str: Response from the model
    """
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
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error connecting to LM Studio: {str(e)}"

def format_nursing_prompt(question, context):
    """
    Format a nursing-specific prompt for the LLM
    
    Args:
        question (str): User's question
        context (str): Relevant context from knowledge base
        
    Returns:
        str: Formatted prompt
    """
    return f"""Context:\n{context}\n\nQuestion: {question}

Please provide a comprehensive nursing-focused answer based on the context provided. Include:
1. Direct answer to the question
2. Key nursing considerations
3. Safety implications if applicable
4. Any relevant protocols or procedures

Keep your response professional and focused on nursing practice."""

def check_lm_studio_connection():
    """
    Check if LM Studio is running and accessible
    
    Returns:
        bool: True if connection is successful
    """
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_available_models():
    """
    Get list of available models from LM Studio
    
    Returns:
        list: List of available models
    """
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []

def generate_nursing_response(question, context, response_type="standard"):
    """
    Generate nursing-specific response using LLM
    
    Args:
        question (str): User's question
        context (str): Relevant context
        response_type (str): Type of response (standard, detailed, quick)
        
    Returns:
        str: Generated response
    """
    system_messages = {
        "standard": "You are a helpful nursing chatbot. Only answer based on the context provided. Focus on practical nursing considerations.",
        "detailed": "You are an expert nursing educator. Provide detailed, evidence-based answers using only the context provided. Include step-by-step procedures when applicable.",
        "quick": "You are a nursing assistant. Provide concise, actionable answers based on the context provided. Focus on immediate actions and key points."
    }
    
    system_message = system_messages.get(response_type, system_messages["standard"])
    
    if response_type == "detailed":
        prompt = format_nursing_prompt(question, context)
        max_tokens = 800
    elif response_type == "quick":
        prompt = f"Context: {context}\n\nQuestion: {question}\n\nProvide a brief, actionable answer:"
        max_tokens = 200
    else:
        prompt = f"Context:\n{context}\n\nQuestion: {question}"
        max_tokens = 500
    
    return query_lm_studio(prompt, system_message, max_tokens=max_tokens)

def validate_response_quality(response):
    """
    Validate the quality of LLM response
    
    Args:
        response (str): Generated response
        
    Returns:
        dict: Validation results
    """
    issues = []
    
    # Check for common issues
    if len(response) < 20:
        issues.append("Response too short")
    
    if "Error connecting" in response:
        issues.append("Connection error")
    
    if not any(keyword in response.lower() for keyword in ['nursing', 'patient', 'care', 'procedure', 'protocol']):
        issues.append("Response may not be nursing-focused")
    
    return {
        "is_valid": len(issues) == 0,
        "issues": issues,
        "length": len(response),
        "nursing_terms": sum(1 for keyword in ['nursing', 'patient', 'care', 'procedure', 'protocol', 'assessment', 'monitoring'] if keyword in response.lower())
    }
