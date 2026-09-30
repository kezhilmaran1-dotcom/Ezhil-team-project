import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from ai_core.gemini_generator import GeminiDocumentGenerator

load_dotenv()

app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal document generation backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = Field(..., min_length=2)
    dates: str = Field(..., min_length=2)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>LegalEase</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            margin: 0;
            padding: 24px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 8px;
            font-size: 42px;
        }
        .subtitle {
            text-align: center;
            color: #94a3b8;
            margin-bottom: 24px;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1.5fr;
            gap: 24px;
        }
        .panel {
            background: #111827;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 20px;
        }
        label {
            display: block;
            font-weight: 600;
            margin: 14px 0 8px;
        }
        input, textarea, button {
            width: 100%;
            box-sizing: border-box;
            font: inherit;
        }
        input, textarea {
            background: #020817;
            color: #e2e8f0;
            border: 1px solid #475569;
            border-radius: 10px;
            padding: 12px;
        }
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 12px 16px;
            cursor: pointer;
            font-weight: 700;
            margin-top: 14px;
        }
        button.secondary {
            background: #1f2937;
            border: 1px solid #475569;
        }
        .preview {
            background: #020817;
            color: #f8fafc;
            border-radius: 12px;
            border: 1px solid #475569;
            padding: 20px;
            white-space: pre-wrap;
            min-height: 300px;
            line-height: 1.6;
        }
        .hidden {
            display: none;
        }
        .status {
            margin-top: 14px;
            padding: 12px;
            border-radius: 8px;
        }
        .error {
            background: rgba(127, 29, 29, 0.4);
            color: #fecaca;
            border: 1px solid #ef4444;
        }
        .success {
            background: rgba(20, 83, 45, 0.4);
            color: #bbf7d0;
            border: 1px solid #22c55e;
        }
        .actions {
            display: flex;
            gap: 10px;
            margin-top: 16px;
        }
        .actions > * { flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚖️ LegalEase</h1>
        <div class="subtitle">AI-Powered Legal Document Generator</div>

        <div class="grid">
            <div class="panel">
                <h2>Document Details</h2>
                <label for="document_type">Document Type</label>
                <input id="document_type" placeholder="Freelance Work Contract" />

                <label for="parties">Parties Involved</label>
                <textarea id="parties" placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)"></textarea>

                <label for="terms">Terms & Conditions</label>
                <textarea id="terms" placeholder="Payment within 30 days; Confidentiality must be maintained;"></textarea>

                <label for="dates">Effective Date</label>
                <input id="dates" placeholder="April 10, 2026" />

                <button id="generateBtn">✨ Generate Document</button>
                <div id="status" class="status hidden"></div>
            </div>

            <div class="panel">
                <h2>Document Preview</h2>
                <div id="preview" class="preview">Your generated legal document will appear here.</div>
                <div class="actions">
                    <button id="editBtn" class="secondary">✏️ Edit Document</button>
                    <button id="regenerateBtn" class="secondary">🔄 Regenerate</button>
                </div>
                <div class="actions">
                    <button id="downloadTxt" class="secondary">⬇️ TXT</button>
                    <button id="downloadDocx" class="secondary">⬇️ DOCX</button>
                    <button id="downloadPdf" class="secondary">⬇️ PDF</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentDocument = "";
        let isEditing = false;

        const preview = document.getElementById('preview');
        const editBtn = document.getElementById('editBtn');

        function setStatus(message, type = 'success') {
            const statusEl = document.getElementById('status');
            statusEl.textContent = message;
            statusEl.className = `status ${type}`;
            statusEl.classList.remove('hidden');
        }

        function clearStatus() {
            const statusEl = document.getElementById('status');
            statusEl.className = 'status hidden';
            statusEl.textContent = '';
        }

        function renderPreview() {
            if (!currentDocument) {
                preview.textContent = 'Your generated legal document will appear here.';
                return;
            }
            preview.textContent = currentDocument;
        }

        async function generateDocument() {
            const payload = {
                document_type: document.getElementById('document_type').value,
                parties: document.getElementById('parties').value,
                terms: document.getElementById('terms').value,
                dates: document.getElementById('dates').value,
            };

            if (!payload.document_type || !payload.parties || !payload.terms || !payload.dates) {
                setStatus('Please fill in all fields before generating a document.', 'error');
                return;
            }

            clearStatus();
            const button = document.getElementById('generateBtn');
            button.disabled = true;
            button.textContent = 'Generating...';

            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });

                const result = await response.json();
                if (!response.ok) {
                    throw new Error(result.detail || 'Generation failed.');
                }

                currentDocument = result.document;
                renderPreview();
                setStatus('Document generated successfully.', 'success');
            } catch (error) {
                setStatus(error.message, 'error');
            } finally {
                button.disabled = false;
                button.textContent = '✨ Generate Document';
            }
        }

        function toggleEditMode() {
            if (!currentDocument) {
                setStatus('Generate a document before editing it.', 'error');
                return;
            }

            const area = document.createElement('textarea');
            area.value = currentDocument;
            area.style.width = '100%';
            area.style.minHeight = '300px';
            area.style.boxSizing = 'border-box';
            area.style.padding = '12px';
            area.style.borderRadius = '10px';
            area.style.background = '#020817';
            area.style.color = '#e2e8f0';

            if (!isEditing) {
                preview.innerHTML = '';
                preview.appendChild(area);
                isEditing = true;
                editBtn.textContent = '💾 Save Edits';
            } else {
                currentDocument = area.value;
                renderPreview();
                isEditing = false;
                editBtn.textContent = '✏️ Edit Document';
                setStatus('Edits saved.', 'success');
            }
        }

        function prepareDownload(kind) {
            if (!currentDocument) {
                setStatus('Generate a document before downloading.', 'error');
                return;
            }

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/download/${kind}`;
            form.style.display = 'none';

            const documentInput = document.createElement('textarea');
            documentInput.name = 'document';
            documentInput.value = currentDocument;

            const titleInput = document.createElement('input');
            titleInput.name = 'title';
            titleInput.value = document.getElementById('document_type').value || 'Legal Document';

            form.appendChild(documentInput);
            form.appendChild(titleInput);
            document.body.appendChild(form);
            form.submit();
            form.remove();
        }

        document.getElementById('generateBtn').addEventListener('click', generateDocument);
        editBtn.addEventListener('click', toggleEditMode);
        document.getElementById('regenerateBtn').addEventListener('click', () => {
            currentDocument = '';
            isEditing = false;
            renderPreview();
            clearStatus();
            editBtn.textContent = '✏️ Edit Document';
        });
        document.getElementById('downloadTxt').addEventListener('click', () => prepareDownload('txt'));
        document.getElementById('downloadDocx').addEventListener('click', () => prepareDownload('docx'));
        document.getElementById('downloadPdf').addEventListener('click', () => prepareDownload('pdf'));
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_PAGE


@app.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        text = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )
        return {"success": True, "document": text}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/download/{kind}")
def download_document(kind: str, document: str = Form(...), title: str = Form("Legal Document")):
    if not document:
        raise HTTPException(status_code=400, detail="No document content provided.")

    from fastapi.responses import Response
    from utils.document_formatter import format_txt, format_docx, format_pdf

    title_name = title or "Legal Document"
    file_name = "legalease_document"

    if kind == 'txt':
        content = format_txt(document)
        return Response(
            content=content,
            media_type='text/plain',
            headers={'Content-Disposition': f'attachment; filename="{file_name}.txt"'},
        )
    if kind == 'docx':
        content = format_docx(document, title_name, document, os.path.join('assets', 'logo.png'))
        return Response(
            content=content,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={'Content-Disposition': f'attachment; filename="{file_name}.docx"'},
        )
    if kind == 'pdf':
        content = format_pdf(document, title_name, os.path.join('assets', 'logo.png'))
        return Response(
            content=content,
            media_type='application/pdf',
            headers={'Content-Disposition': f'attachment; filename="{file_name}.pdf"'},
        )

    raise HTTPException(status_code=400, detail="Unsupported download type.")


@app.get("/health")
def health():
    return {"status": "ok", "message": "LegalEase API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
