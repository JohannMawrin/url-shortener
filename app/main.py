from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.main import router
from app.core.config import settings
from app.core.exceptions import ShortURLNotFoundError

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)


@app.exception_handler(ShortURLNotFoundError)
async def short_url_not_found_handler(
    request: Request,
    exc: ShortURLNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


app.include_router(router)
