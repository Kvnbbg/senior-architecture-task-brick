# Senior Architecture Task Brick

Isolated functional brick demonstrating senior-level rigor:
- Strict TypeScript / Pydantic models with sealed boundaries
- Clean separation of concerns
- 100% unit test coverage on domain logic before any commit
- Explicit architectural decisions documented in PR

## Stack
- Backend: Python 3.12+, FastAPI, Pydantic v2
- Frontend: TypeScript, React, Tailwind CSS
- Tests: Pytest (backend), Jest (frontend ready)

## Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic pytest
pytest -v
```

## Frontend setup
```bash
cd frontend
npm install
npm test
```
