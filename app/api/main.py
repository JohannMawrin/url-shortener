from fastapi import APIRouter

from app.api.routes import short_urls

router = APIRouter()
router.include_router(short_urls.router)
