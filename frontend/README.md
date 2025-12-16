```markdown
Frontend top-level README

Structure:
- `frontend/cms/` - Web CMS React app (single-page app). Build output can be copied into Django static.
- Mobile frontend: moved to a Unity project (separate repository). This repository contains the Django API and the web CMS only.

Quick commands (from `frontend/cms`):
- `npm install`
- `npm start` (dev)
- `npm run build`
- `npm run copy-to-django` (build + copy into `AGHAMazingQuestMobile/static/cms/`)

Copy helper:
- `./_scripts/copy-build-to-django.js` will be created to copy `frontend/cms/build/` into `AGHAMazingQuestMobile/static/cms/`.

```
Frontend top-level README

Structure:
- `frontend/cms/` - Web CMS React app (single-page app). Build output can be copied into Django static.

Quick commands (from `frontend/cms`):
- `npm install`
- `npm start` (dev)
- `npm run build`
- `npm run copy-to-django` (build + copy into `AGHAMazingQuestMobile/static/cms/`)

Copy helper:
- `./_scripts/copy-build-to-django.js` will be created to copy `frontend/cms/build/` into `AGHAMazingQuestMobile/static/cms/`.

