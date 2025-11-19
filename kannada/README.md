# Modalapada – Kannada Voice-to-Text Correction (YourTeamName)

This repository is a packaged submission scaffold for the Voice Challenge.

See `code/` for the runnable frontend and backend skeletons. Add your recordings to `recordings/` and run the backend and frontend locally as described below.

Run backend:

```powershell
cd code/backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Run frontend:

```bash
cd code/frontend
npm install
npm run dev
```

Folder structure:

- `recordings/` — place `easy_paragraph.mp4`, `medium_paragraph.mp4`, `hard_paragraph.mp4` here
- `text_outputs/` — code will write `_original.txt` and `_corrected.txt` files here
- `confusion_fixes/` — csv logs written here
- `code/backend` — FastAPI backend
- `code/frontend` — Vite + React + TypeScript frontend

Speaker info: see `speaker_info.json` for metadata template.
