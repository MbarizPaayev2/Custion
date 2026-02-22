# Security+ Learning API

AI-powered FastAPI backend for Security+ exam preparation with Azerbaijani translation and A2-level vocabulary support.

## Features

- **Azerbaijani Translation**: Automatic translation of Security+ technical content
- **Vocabulary Analysis**: Identifies unknown technical terms using a known words hashmap
- **A2-Level Definitions**: Simple English definitions for technical terms via Ollama AI
- **Mini Notes**: Azerbaijani explanations of core concepts

## Setup

### 1. Install Ollama (if not installed)

Download and install from: https://ollama.ai/download

Then pull the model:
```bash
ollama pull llama3.2
```

### 2. Install Python Dependencies (WITHOUT Rust)

**Windows:**
```bash
install_dependencies.bat
```

**Manual Installation:**
```bash
pip uninstall -y pydantic pydantic-core fastapi uvicorn
pip install --only-binary=:all: pydantic==2.6.4
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` file:
```
OLLAMA_MODEL=llama3.2
```

### 4. Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /analyze
Analyze Security+ technical text.

**Request**:
```json
{
  "text": "A firewall is a network security device that monitors and filters incoming and outgoing network traffic."
}
```

**Response**:
```json
{
  "original_text": "A firewall is a network security device...",
  "az_translation": "Firewall şəbəkə təhlükəsizliyi cihazıdır...",
  "vocabulary_list": [
    {
      "word": "firewall",
      "a2_definition": "A tool that protects computers from bad internet connections"
    }
  ],
  "security_plus_mini_note": "Firewall anlayışı...",
  "unknown_words_count": 3
}
```

### GET /health
Check API health and service status.

## Troubleshooting

### Cargo/Rust Error

If you get Rust/Cargo errors, use the pre-compiled installation:

```bash
pip install --only-binary=:all: pydantic pydantic-core
```

This installs pre-built wheels without requiring Rust compiler.

### Python Version

- Recommended: Python 3.11 or 3.12
- Supported: Python 3.13 (with pre-compiled binaries)

## Project Structure

```
.
├── main.py                    # FastAPI routes and app setup
├── services.py                # Business logic (translation, AI, vocabulary)
├── schemas.py                 # Pydantic models
├── config.py                  # Configuration and known words hashmap
├── requirements.txt           # Python dependencies
├── install_dependencies.bat   # Windows installation script
├── .env                       # Environment variables
├── static/                    # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md                  # Documentation
```
