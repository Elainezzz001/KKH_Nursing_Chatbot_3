# KKH Nursing Chatbot

A comprehensive Streamlit-based medical chatbot designed for nursing professionals, featuring AI-powered knowledge retrieval, pediatric fluid calculations, and interactive quizzes.

## Features

### 🤖 AI Chatbot
- **PDF Knowledge Base**: Automatically processes and embeds content from `KKH Information file.pdf`
- **Semantic Search**: Uses `intfloat/multilingual-e5-large-instruct` for intelligent content retrieval
- **LLM Integration**: Connects to OpenHermes-2.5-Mistral-7B via LM Studio for natural language responses
- **Chat History**: Persistent conversation memory within sessions

### 💧 Pediatric Fluid Calculator
- **Maintenance Fluids**: Holliday-Segar method calculation
- **Resuscitation**: 20mL/kg bolus calculations
- **Dehydration Management**: 5% and 10% deficit calculations
- **Real-time Results**: Displays both mL/day and mL/hour rates

### 📚 Interactive Knowledge Quiz
- **Auto-generated Questions**: Creates MCQ, True/False, and open-ended questions from PDF content
- **Score Tracking**: Real-time scoring with session persistence
- **Retake Option**: Ability to regenerate and retake quizzes
- **Performance Feedback**: Encouragement based on score percentages

### 🎨 User Interface
- **Modern Design**: Clean, medical-themed styling with custom CSS
- **Responsive Layout**: Optimized for both desktop and mobile viewing
- **Logo Integration**: Displays your logo when available
- **Intuitive Navigation**: Clear separation of chat and tools

## Project Structure

```
FYP Nursing Chatbot 3/
├── app.py                      # Main Streamlit application
├── utils.py                    # Helper functions for PDF processing, embeddings, etc.
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── embedded_knowledge.json     # Generated embeddings cache (created automatically)
├── data/
│   └── KKH Information file.pdf # Your nursing knowledge PDF
└── logo/
    └── photo_2025-06-16_15-57-21.jpg # Your logo image
```

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **LM Studio** running with OpenHermes-2.5-Mistral-7B model
   - Download LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/)
   - Load the OpenHermes-2.5-Mistral-7B model
   - Start the local server on `http://localhost:1234`

### Installation

1. **Clone or download** this project to your local machine

2. **Navigate** to the project directory:
   ```bash
   cd "c:\FYP Nursing Chatbot 3"
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify your PDF file** is in the correct location:
   - Ensure `data/KKH Information file.pdf` exists
   - The app will process this file on first run

### Running the Application

1. **Start LM Studio** and ensure the model server is running on `http://localhost:1234`

2. **Launch the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Open your browser** to the URL displayed (usually `http://localhost:8501`)

4. **First-time setup**: The app will automatically process your PDF and create embeddings (this may take a few minutes)

## Usage Guide

### Chatbot
1. Type your nursing-related questions in the chat input
2. The AI will search the knowledge base and provide contextual answers
3. Chat history is maintained throughout your session

### Fluid Calculator
1. Open the sidebar and locate the "Pediatric Fluid Calculator"
2. Enter patient weight and age
3. Select the appropriate scenario (Maintenance/Resuscitation/Dehydration)
4. Click "Calculate Fluids" for instant results

### Knowledge Quiz
1. Click "Start New Quiz" in the sidebar
2. Answer questions one by one using the forms
3. View your score and retake as needed
4. Questions are automatically generated from your PDF content

## Customization

### Modifying the Knowledge Base
- Replace `data/KKH Information file.pdf` with your own content
- Delete `embedded_knowledge.json` to force regeneration
- Restart the app to process the new content

### Changing the LLM
- Modify the `api_url` in `utils.py` `query_llm()` function
- Update the model name in the payload
- Ensure your LLM server supports OpenAI-compatible API

### Styling
- Edit the CSS in `app.py` under the `st.markdown()` section
- Modify colors, fonts, and layout as needed
- Add your organization's branding

## Troubleshooting

### Common Issues

**"Error connecting to LLM"**
- Ensure LM Studio is running and accessible at `http://localhost:1234`
- Check that the OpenHermes-2.5-Mistral-7B model is loaded
- Verify firewall settings aren't blocking the connection

**"PDF file not found"**
- Confirm the PDF exists at `data/KKH Information file.pdf`
- Check file permissions and path spelling

**"Knowledge base not loading"**
- Delete `embedded_knowledge.json` and restart the app
- Ensure sufficient disk space for embedding generation
- Check that the PDF contains readable text

**Quiz not generating**
- Ensure the PDF was processed successfully
- Check that text extraction found meaningful content
- Try regenerating by reloading the knowledge base

### Performance Optimization

- **Large PDFs**: Consider splitting very large files into smaller sections
- **Memory usage**: The embedding model requires ~2-4GB RAM
- **Response time**: First run will be slower due to model loading

## Dependencies

- **streamlit**: Web framework for the application
- **pdfplumber**: PDF text and table extraction
- **sentence-transformers**: Embedding model for semantic search
- **scikit-learn**: Cosine similarity calculations
- **requests**: HTTP client for LLM API calls
- **Pillow**: Image processing for logo display
- **numpy/pandas**: Data manipulation and calculations

## Security Notes

- This application runs locally and doesn't send data to external services
- The LLM server (LM Studio) also runs locally
- Ensure patient data is handled according to your organization's policies
- For production use, implement proper authentication and access controls

## Support

For technical issues or questions:
1. Check this README for common solutions
2. Verify all prerequisites are correctly installed
3. Test with a simple PDF to isolate issues
4. Check console logs for detailed error messages

## License

This project is for educational and professional development purposes. Please ensure compliance with your organization's software usage policies.
