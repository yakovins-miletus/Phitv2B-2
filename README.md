# 🛡️ Phitopolis Heimdall CMS

**Phitopolis Heimdall** is the in-house Content Management System (CMS) and REST API backend powering the Phitopolis digital platform. It serves public read-only content to **Phitopolis Fresko** and provides a secure, private visual Admin Dashboard for content management.

---

## 🏗 System Architecture

* **Backend Engine**: FastAPI (Python 3.12+)
* **Database**: Async SQLAlchemy 2.0 (`aiosqlite` WAL for development / PostgreSQL for production)
* **Admin UI**: React 19 + Vite + TypeScript glassmorphic dashboard (`admin-ui/`)
* **Security & Invisibility Model**:
  * Bound to `127.0.0.1:8000` behind Nginx reverse proxy.
  * Public read-only endpoints (`/api/v1/services`, `/api/v1/team`, `/api/v1/blog-posts`).
  * 5-Layer Trust Boundary defense on `/api/v1/contact-messages` (dual honeypots + HTML tag sanitization).
  * Private Admin CRUD operations (`/api/v1/heimdall/admin/*`) served exclusively over **Tailscale Mesh VPN**.

---

## 📂 Project Structure

```
Heimdall CMS/
├── app/
│   ├── main.py                  # FastAPI application & startup lifecycle
│   ├── api.py                   # Central API router
│   ├── core/                    # App settings, RFC 7807 error handlers & base schemas
│   ├── db/                      # SQLAlchemy session, declarative base & auto-seeding
│   └── features/
│       ├── blog/                # Blog post models, schemas, repository & service
│       ├── innovation/          # Innovation post models, schemas & repository
│       ├── services/            # Service catalog & sub-team structures
│       ├── team/                # Team member profiles & focus areas
│       ├── contact/             # Trust-boundary contact form submission handling
│       └── admin/               # Private Tailscale-gated CMS admin API
│
├── admin-ui/                    # Visual Admin Dashboard Frontend (React 19 + Vite)
│   ├── src/
│   │   ├── components/          # Blog manager, markdown editor, contact inbox
│   │   └── api/adminClient.ts   # Typed API client
│   └── package.json
│
├── tests/                       # Async pytest suite
├── pyproject.toml               # Python dependencies & build config
└── README.md
```

---

## ⚡ Quick Start

### 1. Run Backend Server
```bash
cd "Heimdall CMS"

# Install dependencies using uv
uv sync

# Start FastAPI server on port 8000
uv run uvicorn app.main:app --reload --port 8000
```
* **Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 2. Run Admin Dashboard UI
```bash
cd "Heimdall CMS/admin-ui"

# Install Node dependencies
yarn install # or npm install

# Start Vite dev server on port 5174
yarn dev
```
* **Admin Dashboard UI**: [http://127.0.0.1:5174/](http://127.0.0.1:5174/)

---

## 🧪 Testing

```bash
# Run pytest test suite
uv run pytest
```
