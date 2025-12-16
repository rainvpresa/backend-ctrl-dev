AGHAMazingQuest CMS Frontend

This directory contains the web CMS React application.

Commands:
- Install dependencies: `npm install`
- Run dev server: `npm start` (port 3000 by default)
- Build: `npm run build`
- Build and copy to Django static (project root): `npm run copy-to-django`

The `copy-to-django` script runs a helper that places the built files into `AGHAMazingQuestMobile/static/cms/` so Django can serve them in production.
