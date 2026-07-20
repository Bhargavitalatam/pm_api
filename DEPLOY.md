Deployment via GitHub Actions
=============================

What this does
- Builds the project's Docker image using the repository `Dockerfile`.
- Pushes the image to GitHub Container Registry (GHCR).
- Optionally triggers a Render deploy if you set `RENDER_SERVICE_ID` and `RENDER_API_KEY` repository secrets.

Enable and trigger
1. In your GitHub repository, go to `Settings` → `Actions` and ensure actions are enabled.
2. (Optional for Render) Add repository secrets: `RENDER_SERVICE_ID` and `RENDER_API_KEY`.
3. Push to the `main` branch or run the workflow manually under the `Actions` tab.

Notes
- GitHub does not host long-running containers itself. This workflow pushes the image to GHCR so you can run it on any host (Render, Railway, your VPS, etc.).
- If you want me to add support for another provider (Docker Hub, AWS ECS, Azure, etc.), tell me which one and I'll add it.
