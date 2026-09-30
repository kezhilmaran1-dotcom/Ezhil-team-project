import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
        self.model = None

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)

    def _ensure_client(self):
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Create a .env file and add your Gemini API key before generating a document."
            )

        if self.model is None:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)

    def generate_document(self, document_type, parties, terms, dates):
        self._ensure_client()

        prompt = f"""
You are LegalEase, an AI assistant for drafting structured legal documents.

Create a professional draft of the following legal document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{dates}

TERMS AND CONDITIONS:
{terms}

Requirements:
1. Give the document a clear title.
2. Identify the parties and effective date.
3. Create logical sections and numbered clauses.
4. Convert the supplied terms into appropriate legal clauses.
5. Include signature blocks where appropriate.
6. Do not invent names, dates, addresses, money amounts, or obligations that were not supplied.
7. If information is missing, use a clear placeholder such as [ADDRESS] rather than guessing.
8. Return plain text suitable for editing and export.
9. Do not include markdown code fences.
10. This is a draft for review and should not claim to be legal advice.

Generate only the document.
"""
        response = self.model.generate_content(prompt)
        return response.text.strip()
