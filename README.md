# Phitopolis Heimdall CMS

**Phitopolis Heimdall** is the in-house Content Management System (CMS) and REST API backend for the Phitopolis ecosystem.

## 🚀 Overview

* **Framework**: FastAPI (Python 3.12+)
* **Database**: Async SQLAlchemy 2.0 (`aiosqlite` local fallback / PostgreSQL production)
* **Security & Invisibility**:
  * Bound to localhost (`127.0.0.1:8000`) behind Nginx.
  * Public read-only endpoints served at `/api/v1/`.
  * Tailscale Private Mesh VPN access for admin CRUD operations (`admin.internal.phitopolis.com`).
  * 5-Layer Trust Boundary defense on `/api/v1/contact-messages`.

## 🛠 Local Development

```bash
# Install dependencies using uv
uv sync

# Run dev server
uv run uvicorn app.main:app --reload --port 8000
```
