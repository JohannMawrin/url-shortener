from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.short_urls import ShortURL


class ShortURLRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, url: str, short_code: str) -> ShortURL:
        short_url = ShortURL(url=url, short_code=short_code)
        self._session.add(short_url)
        await self._session.flush()
        return short_url

    async def get(self, short_code: str) -> ShortURL | None:
        query = select(ShortURL).where(ShortURL.short_code == short_code)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
