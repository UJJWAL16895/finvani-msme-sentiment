# FinVani: MSME Sentiment Analysis

## 🚀 Deployment on Railway (Monorepo Setup)

This repository contains both the Backend (Python) and Frontend (Next.js). To deploy on Railway, you must create **two separate services**.

### Service 1: Backend
1.  **New Project** -> **Deploy from GitHub** -> Select this repo.
2.  Go to **Settings** -> **General** -> **Root Directory**.
3.  Set it to: `/backend`
4.  Railway will verify (Green checkmark).
5.  Go to **Variables**:
    - No specific variables needed for basic functionality.
6.  The service will rebuild using the `backend/Dockerfile`.

### Service 2: Frontend
1.  In the same project, click **+ New** -> **GitHub Repo** -> Select this repo *again*.
2.  Go to **Settings** -> **General** -> **Root Directory**.
3.  Set it to: `/frontend`
4.  Go to **Variables**:
    - Add `NEXT_PUBLIC_API_URL`.
    - Value: `https://<YOUR-BACKEND-RAILWAY-URL>` (Copy this from the Backend service dashboard).
5.  The service will rebuild using the `frontend/Dockerfile`.

### Troubleshooting
- If you see `Script start.sh not found`, it means Railway is trying to build the root folder. **Set the Root Directory to /backend or /frontend**.
- If the build fails finding `requirements.txt`, ensure Root Directory is `/backend`.
