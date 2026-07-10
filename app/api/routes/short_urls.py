from fastapi import APIRouter, status, HTTPException

from app.api.dependencies import SessionDep
from app.schemas.short_urls import ShortURLPublic, ShortURLPayload, ShortURLStats
from app.services.short_urls import ShortURLService

router = APIRouter(prefix="/shorten", tags=["short_urls"])


@router.post(
    "/",
    response_model=ShortURLPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_short_url(payload: ShortURLPayload, session: SessionDep):
    return await ShortURLService(session).create(payload)


@router.get("/{short_code}", response_model=ShortURLPublic)
async def get_original_url(short_code: str, session: SessionDep):
    return await ShortURLService(session).get(short_code)


@router.get("/{short_code}/stats", response_model=ShortURLStats)
async def get_url_stats(short_code: str, session: SessionDep):
    return await ShortURLService(session).get(short_code)
