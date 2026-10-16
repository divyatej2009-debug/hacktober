# Open Diagnostic

A small, responsive web dashboard for checking the server's system status and (optionally) its OpenAI API connection. The OpenAI key is read only from the server environment and is never sent to the browser.

## Run locally

Requires Python 3.10 or newer.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn webapp:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The system check works without an OpenAI key. To enable the optional API check, set a valid key in the same PowerShell session:

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:OPENAI_MODEL = "gpt-4o"
```

The live OpenAI check makes a billable API request. API credentials and account billing must be configured by the owner.

## Endpoints

- `/` — dashboard
- `/api/health` — system diagnostics JSON
- `/api/openai-check` — optional server-side OpenAI connectivity check (POST)
- `/docs` — interactive API documentation

## Deploy publicly on Render

1. Push this project to a GitHub repository you own. Do not commit an API key or the `.venv` directory.
2. In Render, create a **Blueprint** and select that repository. Render reads `render.yaml` and provisions the web service.
3. In the new Render service's **Environment** settings, add `OPENAI_API_KEY` only if you want the optional live API check. Keep it secret; never put it in source control or frontend settings.
4. After the deployment is healthy, Render provides a public HTTPS address such as `https://open-diagnostic.onrender.com`.

The public URL is created by Render after you authenticate and deploy; it cannot be provisioned from this local workspace alone. The free service may sleep when idle and take a little time to wake.
