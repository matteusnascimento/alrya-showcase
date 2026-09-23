# ALRYA — Sanitized Code Samples

These files are small, reviewable examples of the engineering patterns used around ALRYA.

They are **not extracted production modules**. Names, endpoints, storage and data are synthetic so the public repository can demonstrate code quality without disclosing proprietary implementation.

## What to review

### Backend

- `domain.py`: tenant boundary, permissions, protocol-based repository dependency and deterministic domain behavior.
- `app.py`: a thin FastAPI HTTP adapter around the domain service.
- `test_tenant_access.py`: tests for cross-company isolation, missing permissions and valid access.

### Frontend

- `revenue-client.ts`: typed fetch boundary with explicit company context, cancellation and structured error handling.

## Running the backend sample

```bash
cd examples/backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app:app --reload
```

The HTTP sample uses demo headers only to make the example self-contained. Production authentication is intentionally not reproduced here.
