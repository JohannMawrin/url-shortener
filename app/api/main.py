from fastapi import APIRouter, status
from starlette.responses import RedirectResponse

from app.api.dependencies import SessionDep
from app.api.routes import short_urls
from app.services.short_urls import ShortURLService

router = APIRouter()


@router.get("/{short_code}", response_class=RedirectResponse)
async def redirect(short_code: str, session: SessionDep):
    short_url = await ShortURLService(session).increment_access_count(short_code)

    return RedirectResponse(
        url=short_url.url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


router.include_router(short_urls.router)
