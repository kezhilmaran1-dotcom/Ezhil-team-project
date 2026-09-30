# LegalEase — AI-Powered Legal Document Generator

This project follows the architecture and functionality described in the supplied LegalEase PDF:

- Streamlit frontend
- FastAPI backend
- Gemini API integration
- Inputs: document type, parties, terms, effective date
- Editable document preview
- TXT, DOCX and PDF export
- DOCX terms table
- PDF header/footer
- Optional logo support

## 1. Project structure

```text
LegalEase_Project/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── routes.py
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py
├── utils/
│   ├── __init__.py
│   └── document_formatter.py
└── assets/
    └── logo.png   (optional)
```

## 2. Install Python

Use Python 3.10 or newer.

## 3. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

## 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## 5. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key:

```text
GEMINI_API_KEY=YOUR_KEY_HERE
GEMINI_MODEL=gemini-1.5-pro
BACKEND_URL=http://127.0.0.1:8000
```

Do not publish your API key or commit `.env` to GitHub.

## 6. Optional logo

Place your logo at:

```text
assets/logo.png
```

The DOCX and PDF exporters will use it automatically.

## 7. Run the FastAPI backend

Open Terminal 1:

```powershell
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## 8. Run the Streamlit frontend

Open Terminal 2:

```powershell
streamlit run app.py
```

Streamlit will show the local website address, normally:

```text
http://localhost:8501
```

## 9. How to use

Example:

Document Type:
```text
Freelance Work Contract
```

Parties:
```text
Jane Doe (Service Provider), TechNova Inc. (Client)
```

Terms:
```text
Payment within 30 days of invoice;
Provider will deliver work by the agreed deadline;
Confidentiality must be maintained;
Either party may terminate with 15 days notice
```

Effective Date:
```text
April 10, 2026
```

Click **Generate Document**.

Then you can:

1. Preview the generated document.
2. Click **Edit Document**.
3. Modify the generated text.
4. Download TXT, DOCX or PDF.

## Important

The Gemini SDK/model naming used here follows the supplied project specification. If your current Google AI account/API uses a newer Gemini SDK or model name, update `requirements.txt`, `.env`, and `ai_core/gemini_generator.py` accordingly.
