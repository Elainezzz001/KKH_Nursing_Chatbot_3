# KKH Nursing Chatbot - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup LM Studio
1. Download LM Studio from https://lmstudio.ai/
2. Install and open LM Studio
3. Search for and download "OpenHermes-2.5-Mistral-7B"
4. Load the model and start the local server
5. Ensure it's running on `http://localhost:1234`

### 3. Verify Setup
```bash
python test_setup.py
```

### 4. Launch the Application
```bash
streamlit run app.py
```
*Or double-click `start_app.bat` on Windows*

## 📁 Project Structure Overview

```
FYP Nursing Chatbot 3/
├── 🚀 app.py                     # Main Streamlit application
├── 🔧 utils.py                   # Core functionality (PDF, embeddings, LLM)
├── ⚙️ config.py                  # Configuration settings
├── 📦 requirements.txt           # Python dependencies
├── 🧪 test_setup.py              # System verification script
├── 🖱️ start_app.bat              # Windows startup script
├── 📚 README.md                  # Detailed documentation
├── 📄 embedded_knowledge.json    # Generated embeddings cache
├── 📂 data/
│   └── KKH Information file.pdf  # Your nursing knowledge base
└── 🖼️ logo/
    └── photo_2025-06-16_15-57-21.jpg # Your logo
```

## 🎯 Key Features

### 💬 AI Chatbot
- **Smart Knowledge Retrieval**: Automatically finds relevant information from your PDF
- **Context-Aware Responses**: Uses advanced embeddings for semantic search
- **Local LLM Integration**: Secure, private processing with OpenHermes-2.5-Mistral-7B
- **Chat Memory**: Maintains conversation history during your session

### 💧 Pediatric Fluid Calculator
- **Maintenance Fluids**: Holliday-Segar method (100/50/20 rule)
- **Resuscitation**: 20mL/kg bolus calculations
- **Dehydration Management**: 5% and 10% deficit formulas
- **Age & Weight Adjustments**: Pediatric-specific calculations

### 📚 Knowledge Quiz System
- **Auto-Generated Questions**: Creates MCQ, True/False, and open-ended questions
- **PDF-Based Content**: Questions derived directly from your nursing materials
- **Progress Tracking**: Real-time scoring and performance feedback
- **Retake Capability**: Generate new questions for continuous learning

## 🛠️ Customization Options

### Change the Knowledge Base
1. Replace `data/KKH Information file.pdf` with your content
2. Delete `embedded_knowledge.json` to force regeneration
3. Restart the application

### Modify LLM Settings
Edit `config.py`:
```python
LLM_API_URL = "your_llm_endpoint"
LLM_MODEL_NAME = "your_model_name"
LLM_TEMPERATURE = 0.3  # Creativity level (0.0-1.0)
```

### Update Styling
Edit the CSS section in `app.py` to match your organization's branding.

## 🔧 Troubleshooting

### ❌ Common Issues

**"Error connecting to LLM"**
- ✅ Verify LM Studio is running
- ✅ Check that OpenHermes-2.5-Mistral-7B is loaded
- ✅ Confirm server is at `http://localhost:1234`

**"PDF file not found"**
- ✅ Ensure PDF is at `data/KKH Information file.pdf`
- ✅ Check file name matches exactly (including spaces)

**"Knowledge base not loading"**
- ✅ Run `python test_setup.py` to diagnose
- ✅ Delete `embedded_knowledge.json` and restart
- ✅ Verify PDF contains readable text

**Slow performance**
- ✅ First run is slower (model loading + embedding generation)
- ✅ Subsequent runs use cached embeddings
- ✅ Ensure adequate RAM (4GB+ recommended)

### 🔍 Debug Commands

```bash
# Test system setup
python test_setup.py

# Check dependencies
pip list

# Verify PDF content
python -c "from utils import load_and_process_pdf; print(len(load_and_process_pdf('data/KKH Information file.pdf')))"

# Test LLM connection
curl http://localhost:1234/health
```

## 🏥 Usage Tips for Nurses

### Best Practices
1. **Ask Specific Questions**: "What is the protocol for pediatric fever management?" works better than "fever"
2. **Use Medical Terms**: The AI understands nursing terminology from your PDF
3. **Check Calculations**: Always verify fluid calculations with your protocols
4. **Regular Quiz Practice**: Use the quiz feature for continuing education

### Example Questions
- "What are the signs of dehydration in pediatric patients?"
- "How do I calculate maintenance fluids for a 15kg child?"
- "What is the protocol for medication administration?"
- "When should I escalate to the attending physician?"

## 📊 Performance Metrics

- **Response Time**: ~2-5 seconds per query (after initial load)
- **Accuracy**: Based on your PDF content quality
- **Memory Usage**: ~2-4GB during operation
- **Storage**: ~500MB for embeddings (varies by PDF size)

## 🔒 Security & Privacy

- **Local Processing**: All data stays on your machine
- **No External API Calls**: Uses local LLM (LM Studio)
- **HIPAA Considerations**: Suitable for environments requiring data privacy
- **Audit Trail**: Chat logs available in session state

## 📞 Support

If you encounter issues:
1. Run `python test_setup.py` for diagnostics
2. Check the console for error messages
3. Verify all prerequisites are installed
4. Ensure your PDF contains extractable text

---

*Built for nursing professionals by nursing professionals. Happy learning! 🏥*
