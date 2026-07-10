from sqlalchemy import select, update
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

    async def update(self, short_code: str, url: str) -> ShortURL | None:
        query = (
            update(ShortURL)
            .where(ShortURL.short_code == short_code)
            .values(url=url)
            .returning(ShortURL)
        )
        result = await self._session.execute(query)
        await self._session.flush()
        return result.scalar_one_or_none()

    async def delete(self, short_code: str) -> bool:
        query = (
            update(ShortURL)
            .where(ShortURL.short_code == short_code)
            .returning(ShortURL.short_code)
        )
        result = await self._session.execute(query)
        await self._session.flush()
        return result.scalar_one_or_none() is not None

    async def increment_access_count(self, short_code: str) -> ShortURL | None:
        query = (
            update(ShortURL)
            .where(ShortURL.short_code == short_code)
            .values(access_count=ShortURL.access_count + 1)
            .returning(ShortURL)
        )
        result = await self._session.execute(query)
        await self._session.flush()
        return result.scalar_one_or_none()
