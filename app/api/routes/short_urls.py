from fastapi import APIRouter, status

from app.api.dependencies import SessionDep
from app.schemas.short_urls import ShortURLPublic, ShortURLPayload
from app.services.short_urls import ShortURLService

router = APIRouter(prefix="/shorten", tags=["short_urls"])


@router.post(
    "/",
    response_model=ShortURLPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(payload: ShortURLPayload, session: SessionDep):
    return await ShortURLService(session).create(payload)
