# KKH Nursing Chatbot

A comprehensive Streamlit-based medical chatbot designed for nursing professionals at KKH (KK Women's and Children's Hospital). This application provides intelligent nursing assistance through PDF-based knowledge retrieval, pediatric fluid calculations, and interactive nursing quizzes.

## Features

### 🤖 AI-Powered Chatbot
- **PDF Knowledge Base**: Automatically extracts and processes information from nursing protocols and guidelines
- **Intelligent Retrieval**: Uses multilingual embeddings to find relevant information for user queries
- **LLM Integration**: Connects to LM Studio for natural language responses using OpenHermes-2.5-Mistral-7B

### 🧮 Pediatric Fluid Calculator
- **Maintenance Fluids**: Holliday-Segar method calculations
- **Resuscitation**: 20mL/kg bolus calculations
- **Deficit Calculations**: 5% and 10% dehydration formulas
- **Real-time Results**: Displays results in mL/day and mL/hour

### 📚 Interactive Nursing Quiz
- **Dynamic Question Generation**: Creates questions from PDF content
- **Multiple Question Types**: MCQs, True/False, and open-ended questions
- **Score Tracking**: Comprehensive scoring and feedback system
- **Retake Option**: Allows users to retake quizzes for learning reinforcement

### 💬 Enhanced Chat Interface
- **Professional UI**: Clean, medical-themed interface with custom styling
- **Chat History**: Persistent conversation history during sessions
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
KKH Nursing Chatbot 3/
├── app.py                      # Main Streamlit application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── data/
│   └── KKH Information file.pdf # Nursing knowledge base
├── logo/
│   └── photo_2025-06-16_15-57-21.jpg # Application logo
├── utils/
│   ├── __init__.py            # Utils package initializer
│   ├── pdf_processor.py       # PDF extraction and embedding functions
│   ├── fluid_calculator.py    # Pediatric fluid calculation functions
│   ├── quiz_generator.py      # Quiz generation and management
│   └── llm_interface.py       # LM Studio API interface
└── embedded_knowledge.json    # Generated embeddings cache (created automatically)
```

## Installation & Setup

### Prerequisites
1. **Python 3.8+**
2. **LM Studio** - Download and install from [LM Studio](https://lmstudio.ai/)
3. **OpenHermes-2.5-Mistral-7B model** - Download through LM Studio

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Setup LM Studio
1. Open LM Studio
2. Download the OpenHermes-2.5-Mistral-7B model
3. Start the local server at `http://localhost:1234`
4. Ensure the model is loaded and ready to accept requests

### Step 3: Prepare Data
1. Place your nursing PDF files in the `data/` directory
2. The application will automatically process the PDF on first run
3. Embeddings will be cached in `embedded_knowledge.json`

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Usage Guide

### Chat Interface
1. Ask questions about nursing protocols, procedures, or guidelines
2. The system will search the knowledge base and provide relevant answers
3. Chat history is maintained during the session

### Fluid Calculator
1. Open the sidebar and find the "Fluid Calculator" section
2. Enter patient weight and age
3. Select the appropriate scenario (Maintenance, Resuscitation, or Deficit)
4. Click "Calculate" to get fluid requirements

### Nursing Quiz
1. Click "Start Quiz" in the sidebar
2. Answer questions based on the nursing knowledge base
3. Progress through all questions using the "Next Question" button
4. View your score and feedback at the end
5. Use "Retake Quiz" to try again with different questions

## Technical Details

### PDF Processing
- Uses `pdfplumber` for text and table extraction
- Implements intelligent text chunking with sentence boundary detection
- Creates embeddings using `intfloat/multilingual-e5-large-instruct`

### Embedding and Retrieval
- Stores embeddings in JSON format for quick loading
- Uses cosine similarity for relevance matching
- Configurable similarity threshold for quality control

### LLM Integration
- RESTful API integration with LM Studio
- Configurable system messages for different response types
- Error handling and connection validation

### Fluid Calculations
- Implements pediatric fluid calculation standards
- Holliday-Segar method for maintenance fluids
- Standard resuscitation and deficit formulas
- Age and weight-based calculations

## Configuration

Modify `config.py` to adjust:
- LM Studio connection settings
- Embedding model parameters
- Quiz generation settings
- UI themes and styling
- File paths and locations

## Troubleshooting

### Common Issues

1. **LM Studio Connection Error**
   - Ensure LM Studio is running at `http://localhost:1234`
   - Check that the model is loaded and active
   - Verify no firewall blocking the connection

2. **PDF Processing Fails**
   - Ensure PDF file exists in the `data/` directory
   - Check file permissions and readability
   - Verify PDF is not corrupted or password-protected

3. **Embedding Model Download**
   - First run may take time to download the embedding model
   - Ensure stable internet connection
   - Check available disk space (model is ~1GB)

4. **Memory Issues**
   - Large PDFs may require more RAM
   - Consider reducing chunk size in config
   - Close other applications if needed

## Dependencies

- **streamlit**: Web application framework
- **pdfplumber**: PDF text extraction
- **sentence-transformers**: Multilingual embeddings
- **scikit-learn**: Similarity calculations
- **numpy**: Numerical operations
- **pandas**: Data handling
- **requests**: API communication
- **torch**: Deep learning framework
- **transformers**: NLP models
- **Pillow**: Image processing

## Future Enhancements

- [ ] Multi-language support
- [ ] Advanced quiz analytics
- [ ] Integration with hospital systems
- [ ] Mobile application
- [ ] Voice interaction
- [ ] Document upload feature
- [ ] Export chat history
- [ ] Advanced fluid calculation scenarios

## License

This project is developed for educational and professional use at KKH. Please ensure compliance with institutional policies and data protection requirements.

## Support

For technical support or questions about the application, please contact the development team or refer to the documentation.

---

**Note**: This application is designed for educational and reference purposes. Always follow institutional protocols and consult with medical professionals for patient care decisions.
