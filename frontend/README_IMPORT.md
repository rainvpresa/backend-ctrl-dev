```markdown
Frontend import instructions

- This repository expects a web CMS application (React or other SPA) to live under `frontend/cms/`.

Quick steps to import an existing CMS project:
1. Put your CMS source in `frontend/cms/` (or place build output into the Django static location).
2. From the repo root, install dependencies for the CMS frontend (if applicable):
   - `cd frontend/cms`
   - `npm install` or `yarn`
3. Run locally for development:
   - `npm start` (runs on :3000 by default)
   - Ensure `REACT_APP_API_BASE_URL` (or your app's equivalent) in `.env` points to the Django API (e.g. `http://localhost:8000/api`).
4. Build for production:
   - `npm run build`
   - The build output will be in `frontend/cms/build/`. You can copy these static files into `AGHAMazingQuestMobile/static/cms/` or configure a reverse proxy (nginx) to serve them.

Notes:
- The previous example mobile app (React/Expo) was removed from this repository. Mobile clients now use a Unity project maintained in a separate repository.
- If you want Django to serve built CMS files directly, I can add a small helper script or view to copy/serve `frontend/cms/build/` into Django static files.
- If you prefer Docker for the frontend, I can add a `Dockerfile` for `frontend/cms/` on request.

```
