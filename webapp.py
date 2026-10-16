"""Web application for the system and OpenAI connectivity diagnostics."""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

from tool import get_system_diagnostic

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Open Diagnostic",
    description="A small web dashboard for local system and OpenAI API checks.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def system_health() -> dict[str, object]:
    """Return basic runtime diagnostics without making an external API call."""
    return get_system_diagnostic()


@app.post("/api/openai-check")
def openai_check() -> dict[str, str]:
    """Check OpenAI connectivity using the server-side environment key."""
    if not os.environ.get("OPENAI_API_KEY"):
        return {
            "status": "not_configured",
            "message": "OpenAI API key is not configured on this server. System diagnostics still work.",
        }

    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly: OpenAI API connection successful.",
                }
            ],
            max_tokens=30,
        )
        message = response.choices[0].message.content or "The API responded without text."
        return {"status": "online", "message": message}
    except Exception as exc:
        # Report actionable status without returning request internals or credentials.
        status_code = getattr(exc, "status_code", None)
        if status_code == 401:
            message = "OpenAI rejected the configured API key (401). Check that it is valid and active."
        elif status_code == 429:
            message = "OpenAI quota or rate limit reached (429). Check billing, credits, and usage limits."
        else:
            message = "Could not connect to OpenAI. Check server network access and API configuration."
        return {"status": "error", "message": message}
