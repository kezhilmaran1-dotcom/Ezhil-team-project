import os

from ai_core.gemini_generator import GeminiDocumentGenerator


def test_missing_api_key_does_not_crash_init(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    generator = GeminiDocumentGenerator()
    assert generator.api_key is None
    assert generator.model is None


def test_generate_document_without_api_key_raises_clear_error(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    generator = GeminiDocumentGenerator()

    try:
        generator.generate_document("Contract", "Jane", "Pay on time", "2026-01-01")
        assert False, "Expected ValueError when API key is missing"
    except ValueError as exc:
        assert "GEMINI_API_KEY" in str(exc)
