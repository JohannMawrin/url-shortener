from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from app.api.dependencies import SessionDep
from app.api.main import router
from app.core.config import settings
from app.core.exceptions import ShortURLNotFoundError
from app.services.short_urls import ShortURLService

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

app.include_router(router)


@app.exception_handler(ShortURLNotFoundError)
async def short_url_not_found_handler(
    request: Request,
    exc: ShortURLNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.get("/{short_code}", response_class=RedirectResponse)
async def redirect(short_code: str, session: SessionDep):
    short_url = await ShortURLService(session).increment_access_count(short_code)

    return RedirectResponse(
        url=short_url.url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
