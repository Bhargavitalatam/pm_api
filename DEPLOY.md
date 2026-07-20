Deployment Guide (Koyeb & Vercel)
================================

This project can be deployed to Koyeb (container-based with managed PostgreSQL database) or Vercel (serverless function-based).

Deploying to Koyeb
------------------
Koyeb runs standard Docker containers and offers a free database tier.

### Option 1: 1-Click Deployment Button
Click the button below to deploy the app:

[![Deploy to Koyeb](https://www.koyeb.com/static/images/deploy/button.svg)](https://app.koyeb.com/deploy?type=git&repository=github.com/Bhargavitalatam/pm_api&branch=main&name=pm-api&ports=8000;http;/)

### Option 2: Manual Setup on Koyeb
1. Sign up/log in to [Koyeb](https://app.koyeb.com/).
2. Create a new service and select **GitHub** as the deployment method.
3. Choose your repository `pm_api`.
4. Koyeb will automatically detect the `Dockerfile` and build it.
5. Under **Environment variables**, set `DATABASE_URL` to your database connection string (you can provision a free PostgreSQL database directly on Koyeb).
6. Set the exposed port to `8000`.

Deploying to Vercel
-------------------
Vercel hosts the application as a Python serverless function.

1. Install the Vercel CLI locally or connect your GitHub repository to Vercel in the dashboard.
2. If using Vercel CLI, run:
   ```bash
   vercel
   ```
3. Set the environment variable `DATABASE_URL`. Since serverless functions restart often, configure a persistent remote PostgreSQL database (like [Neon](https://neon.tech/)) or use a temporary SQLite URL (`sqlite:///tmp/test.db`).
4. Once configured, deploy to production with:
   ```bash
   vercel --prod
   ```
