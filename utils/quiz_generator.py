import random
import re

def generate_quiz_questions(chunks, num_questions=15):
    """
    Generate quiz questions from PDF chunks
    
    Args:
        chunks (list): List of text chunks from PDF
        num_questions (int): Number of questions to generate
        
    Returns:
        list: List of quiz questions
    """
    if not chunks:
        return []
    
    # Filter chunks that are suitable for questions
    suitable_chunks = [chunk for chunk in chunks if len(chunk) > 50 and "Table from page" not in chunk]
    
    if len(suitable_chunks) < num_questions:
        num_questions = len(suitable_chunks)
    
    selected_chunks = random.sample(suitable_chunks, min(num_questions, len(suitable_chunks)))
    
    questions = []
    question_types = ["mcq", "true_false", "open_ended"]
    
    for i, chunk in enumerate(selected_chunks):
        question_type = random.choice(question_types)
        
        if question_type == "mcq":
            question = generate_mcq_question(chunk, i)
        elif question_type == "true_false":
            question = generate_true_false_question(chunk, i)
        else:
            question = generate_open_ended_question(chunk, i)
        
        questions.append(question)
    
    return questions

def generate_mcq_question(chunk, question_num):
    """Generate multiple choice question from chunk"""
    # Extract key concepts from the chunk
    key_phrases = extract_key_phrases(chunk)
    
    question = {
        "type": "mcq",
        "question": f"Based on the following nursing information, which statement is most accurate?\n\n{chunk[:200]}{'...' if len(chunk) > 200 else ''}",
        "options": generate_mcq_options(chunk, key_phrases),
        "correct_answer": 0,  # First option is always correct
        "context": chunk,
        "explanation": f"This question tests understanding of nursing protocols and procedures."
    }
    
    return question

def generate_true_false_question(chunk, question_num):
    """Generate true/false question from chunk"""
    # Create a statement based on the chunk
    statement = create_factual_statement(chunk)
    
    question = {
        "type": "true_false",
        "question": f"True or False: {statement}",
        "correct_answer": True,
        "context": chunk,
        "explanation": f"This statement is based on the nursing guidelines provided."
    }
    
    return question

def generate_open_ended_question(chunk, question_num):
    """Generate open-ended question from chunk"""
    question_starters = [
        "What are the key nursing considerations for",
        "Explain the importance of",
        "Describe the proper procedure for",
        "What should a nurse prioritize when",
        "How would you approach"
    ]
    
    starter = random.choice(question_starters)
    topic = extract_main_topic(chunk)
    
    question = {
        "type": "open_ended",
        "question": f"{starter} {topic}? Base your answer on the following information:\n\n{chunk[:300]}{'...' if len(chunk) > 300 else ''}",
        "context": chunk,
        "sample_answer": generate_sample_answer(chunk),
        "explanation": f"This open-ended question tests comprehensive understanding of nursing practices."
    }
    
    return question

def extract_key_phrases(text):
    """Extract key phrases from text for question generation"""
    # Simple keyword extraction
    # Remove common words and extract important nursing terms
    common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'shall', 'can', 'cannot', 'this', 'that', 'these', 'those', 'a', 'an'}
    
    words = re.findall(r'\b\w+\b', text.lower())
    key_phrases = [word for word in words if word not in common_words and len(word) > 3]
    
    return key_phrases[:10]  # Return top 10 key phrases

def generate_mcq_options(chunk, key_phrases):
    """Generate multiple choice options"""
    # First option is always correct (based on the chunk)
    correct_option = f"This follows proper nursing protocols as described in the guidelines"
    
    # Generate distractors
    distractor_templates = [
        "This procedure is not recommended in pediatric care",
        "This approach contradicts standard nursing practices",
        "This method is outdated and no longer used",
        "This technique requires additional physician approval"
    ]
    
    distractors = random.sample(distractor_templates, 3)
    
    options = [correct_option] + distractors
    random.shuffle(options)
    
    # Update correct answer index
    correct_index = options.index(correct_option)
    
    return options

def create_factual_statement(chunk):
    """Create a factual statement from chunk"""
    # Extract the first complete sentence as a statement
    sentences = re.split(r'[.!?]+', chunk)
    if sentences:
        statement = sentences[0].strip()
        # Clean up the statement
        statement = re.sub(r'^[^A-Za-z]*', '', statement)  # Remove leading non-letters
        return statement
    return "This information is accurate according to nursing guidelines"

def extract_main_topic(chunk):
    """Extract main topic from chunk"""
    # Simple topic extraction - look for nursing-related keywords
    nursing_keywords = {
        'medication': 'medication administration',
        'patient': 'patient care',
        'assessment': 'patient assessment',
        'monitoring': 'patient monitoring',
        'procedure': 'nursing procedures',
        'safety': 'patient safety',
        'documentation': 'nursing documentation',
        'communication': 'patient communication',
        'infection': 'infection control',
        'hygiene': 'patient hygiene',
        'vital': 'vital signs monitoring',
        'pain': 'pain management',
        'wound': 'wound care',
        'fluid': 'fluid management',
        'nutrition': 'nutritional care'
    }
    
    chunk_lower = chunk.lower()
    for keyword, topic in nursing_keywords.items():
        if keyword in chunk_lower:
            return topic
    
    return "nursing care protocols"

def generate_sample_answer(chunk):
    """Generate a sample answer for open-ended questions"""
    # Create a structured answer based on the chunk
    key_points = extract_key_points(chunk)
    
    if key_points:
        sample_answer = "Key considerations include: " + "; ".join(key_points[:3])
    else:
        sample_answer = "The answer should address the main nursing considerations mentioned in the provided context."
    
    return sample_answer

def extract_key_points(text):
    """Extract key points from text"""
    # Split by common delimiters and extract meaningful points
    points = []
    
    # Split by various delimiters
    sentences = re.split(r'[.!?;]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in ['must', 'should', 'important', 'ensure', 'monitor', 'assess', 'document', 'follow', 'maintain']):
            points.append(sentence)
    
    return points[:5]  # Return top 5 key points

def validate_question_quality(question):
    """Validate the quality of generated questions"""
    issues = []
    
    # Check question length
    if len(question['question']) < 20:
        issues.append("Question too short")
    
    # Check if context is meaningful
    if len(question['context']) < 50:
        issues.append("Context too short")
    
    # Check MCQ options
    if question['type'] == 'mcq':
        if len(question['options']) != 4:
            issues.append("MCQ must have 4 options")
        if question['correct_answer'] not in range(4):
            issues.append("Invalid correct answer index")
    
    # Check True/False questions
    if question['type'] == 'true_false':
        if not isinstance(question['correct_answer'], bool):
            issues.append("True/False answer must be boolean")
    
    return len(issues) == 0, issues

def shuffle_quiz_questions(questions):
    """Shuffle quiz questions randomly"""
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return shuffled

def calculate_quiz_score(questions, answers):
    """Calculate quiz score based on answers"""
    if not questions or not answers:
        return 0, 0
    
    correct = 0
    total = len(questions)
    
    for i, question in enumerate(questions):
        if i < len(answers):
            user_answer = answers[i]
            
            if question['type'] == 'mcq':
                if isinstance(user_answer, str) and user_answer in question['options']:
                    if question['options'].index(user_answer) == question['correct_answer']:
                        correct += 1
            elif question['type'] == 'true_false':
                if user_answer == str(question['correct_answer']):
                    correct += 1
            # Open-ended questions are not automatically scored
    
    return correct, total

def get_quiz_feedback(score, total):
    """Generate feedback based on quiz score"""
    percentage = (score / total) * 100 if total > 0 else 0
    
    if percentage >= 90:
        return "Excellent! You have a strong understanding of nursing protocols."
    elif percentage >= 80:
        return "Good job! You demonstrate solid knowledge of nursing practices."
    elif percentage >= 70:
        return "Well done! Continue studying to improve your understanding."
    elif percentage >= 60:
        return "Fair performance. Consider reviewing the material more thoroughly."
    else:
        return "Keep studying! Review the nursing guidelines and try again."
