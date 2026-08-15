# CivivOS Final Frontend

A polished React/Vite frontend for the CivivOS backend.

## Run

```powershell
npm install
npm run dev
```

Backend expected at `http://127.0.0.1:8000`.

## Routes

- `/` — editorial landing page
- `/dashboard` — citizen dashboard
- `/new` — create a case
- `/case/:caseId` — case dossier and lifecycle
- `/case/:caseId/appeal` — first appeal artifact

## Notes

Cases created through the frontend are remembered in localStorage so the dashboard can re-hydrate them from the FastAPI case endpoint.
