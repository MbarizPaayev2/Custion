# Security+ Learning API

AI-powered FastAPI backend for Security+ exam preparation with Azerbaijani translation and A2-level vocabulary support.

## Features

- **Azerbaijani Translation**: Automatic translation of Security+ technical content
- **Vocabulary Analysis**: Identifies unknown technical terms using a known words hashmap
- **A2-Level Definitions**: Simple Azerbaijani definitions for technical terms via Gemini AI
- **Mini Notes**: Azerbaijani explanations of core concepts

## Setup

### 1. Configure Gemini API Key

Create or edit `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
ALLOWED_ORIGINS=http://localhost:8000
```

- `GEMINI_API_KEY` is required for AI term definitions and mini notes.
- `ALLOWED_ORIGINS` is optional. Use comma-separated values for multiple frontend origins.

### 2. Install Python Dependencies

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

### 3. Run the Application

```bash
python main.py
```

The API and frontend will be available at `http://localhost:8000`

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
      "a2_definition": "Şəbəkəni zərərli girişdən qoruyan təhlükəsizlik sistemi"
    }
  ],
  "security_plus_mini_note": "Firewall anlayışı...",
  "unknown_words_count": 3
}
```

### GET /health
Check API health and service status.

## Troubleshooting

### Python Version

- Recommended: Python 3.11 or 3.12
- Supported: Python 3.13 (with pre-compiled binaries)

## Project Structure

```text
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
