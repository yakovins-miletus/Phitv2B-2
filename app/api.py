from fastapi import APIRouter

from app.features.admin.router import router as admin_router
from app.features.blog.router import router as blog_router
from app.features.contact.router import router as contact_router
from app.features.innovation.router import router as innovation_router
from app.features.services.router import router as services_router
from app.features.team.router import router as team_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(services_router)
api_router.include_router(team_router)
api_router.include_router(contact_router)
api_router.include_router(blog_router)
api_router.include_router(innovation_router)

# Admin CMS Router
api_router.include_router(admin_router)
