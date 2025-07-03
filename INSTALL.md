# Installation Guide for KKH Nursing Chatbot

## Quick Start (Windows)

1. **Double-click `start_app.bat`** - This will automatically handle most setup steps
2. **Follow the prompts** - The script will install dependencies and start the app
3. **Open your browser** - Go to `http://localhost:8501` if it doesn't open automatically

## Manual Installation

### Step 1: Install Python
- Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
- During installation, make sure to check "Add Python to PATH"

### Step 2: Install Dependencies
Open Command Prompt/PowerShell/Terminal and run:
```bash
pip install -r requirements.txt
```

### Step 3: Setup LM Studio (Optional but Recommended)
1. Download LM Studio from [lmstudio.ai](https://lmstudio.ai/)
2. Install and open LM Studio
3. Download the "OpenHermes-2.5-Mistral-7B" model from the model catalog
4. Start the local server (usually runs on `http://localhost:1234`)

### Step 4: Test Your Installation
Run the test script:
```bash
python test_setup.py
```

### Step 5: Start the Application
```bash
streamlit run app_clean.py
```

## Project Structure Overview

```
KKH Nursing Chatbot 3/
├── app_clean.py           # Main application (recommended)
├── app.py                 # Original monolithic version
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── start_app.bat          # Windows startup script
├── start_app.sh           # Linux/Mac startup script
├── test_setup.py          # Installation test script
├── data/
│   └── KKH Information file.pdf
├── logo/
│   └── photo_2025-06-16_15-57-21.jpg
└── utils/
    ├── __init__.py
    ├── pdf_processor.py
    ├── fluid_calculator.py
    ├── quiz_generator.py
    └── llm_interface.py
```

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'streamlit'"**
   - Solution: Run `pip install -r requirements.txt`

2. **"Error connecting to LM Studio"**
   - Solution: Start LM Studio and load the model, or use basic mode

3. **"PDF file not found"**
   - Solution: Ensure `KKH Information file.pdf` is in the `data/` folder

4. **Memory issues with large PDFs**
   - Solution: Reduce chunk size in `config.py`

### Performance Tips

- First run may take 5-10 minutes to download the embedding model
- LM Studio requires significant RAM (8GB+ recommended)
- Large PDFs will take time to process initially
- Embeddings are cached for faster subsequent runs

## Configuration

Edit `config.py` to customize:
- LM Studio connection settings
- Embedding model parameters
- PDF processing options
- UI themes and colors

## Features Overview

### 🤖 AI Chatbot
- Processes PDF documents automatically
- Uses advanced embeddings for question matching
- Integrates with LM Studio for natural responses
- Maintains chat history during session

### 🧮 Fluid Calculator
- Maintenance fluid calculations (Holliday-Segar)
- Resuscitation fluid calculations (20mL/kg)
- Deficit calculations for dehydration
- Pediatric-focused formulas

### 📚 Knowledge Quiz
- Auto-generates questions from PDF content
- Multiple choice, True/False, and open-ended questions
- Tracks scores and provides feedback
- Randomized question order

## Usage Tips

1. **PDF Processing**: Place nursing documents in the `data/` folder
2. **Chat Interface**: Ask specific questions about protocols and procedures
3. **Fluid Calculator**: Use for pediatric patients with weight-based calculations
4. **Quiz Feature**: Test knowledge retention and understanding

## Support

- Run `python test_setup.py` to diagnose issues
- Check the README.md for detailed documentation
- Ensure all files are in the correct directory structure

## Next Steps

1. Test the application with the provided sample PDF
2. Add your own nursing documents to the `data/` folder
3. Customize the configuration for your specific needs
4. Train staff on using the different features

---

**Remember**: This is a learning and reference tool. Always follow institutional protocols and consult with medical professionals for patient care decisions.
