# ज्ञानगंगा AI — Static HTML edition

## Run locally
Open `index.html` in a modern browser.

## Publish online with GitHub Pages
1. Create a GitHub repository (for example `gyangangaa-ai`).
2. Upload `index.html` to the repository root and commit it.
3. Open **Settings → Pages**.
4. Choose **Deploy from a branch**, branch `main`, folder `/(root)`, then save.
5. Wait for GitHub Pages to publish the site. The URL will be shown on the Pages settings screen.

## Important limitations
- This is a static front end; no Python server or SQLite database is running.
- Added resources are stored in the visitor's browser (`localStorage`), not shared between visitors/devices. Export CSV for a backup.
- The optional Gemini assistant asks each visitor to enter their own API key. Do not hard-code a key into this HTML or publish a secret key in a public repository. Google API usage/quota and possible charges depend on the visitor's account.
- The Gemini model name is editable in the page because model availability can change.
