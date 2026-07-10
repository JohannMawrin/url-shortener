import secrets
import string

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ShortURLNotFoundError
from app.models.short_urls import ShortURL
from app.repositories.short_urls import ShortURLRepository
from app.schemas.short_urls import ShortURLPayload


class ShortURLService:
    _MAX_SHORT_CODE_GENERATION_ATTEMPTS: int = 10

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _generate_short_code(length: int = 8) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    async def create(self, payload: ShortURLPayload) -> ShortURL:
        for _ in range(self._MAX_SHORT_CODE_GENERATION_ATTEMPTS):
            short_code = self._generate_short_code()

            async with self._session.begin_nested():
                try:
                    short_url = await ShortURLRepository(self._session).create(
                        str(payload.url),
                        short_code,
                    )
                    await self._session.commit()
                    return short_url
                except IntegrityError:
                    continue

        raise RuntimeError("Failed to generate a unique short code")

    async def get(self, short_code: str) -> ShortURL:
        short_url = await ShortURLRepository(self._session).get(short_code)

        if short_url is None:
            raise ShortURLNotFoundError(short_code)

        return short_url

    async def update(self, short_code: str, payload: ShortURLPayload) -> ShortURL:
        short_url = await ShortURLRepository(self._session).update(
            short_code,
            str(payload.url),
        )

        if short_url is None:
            raise ShortURLNotFoundError(short_code)

        await self._session.commit()
        return short_url

    async def delete(self, short_code: str) -> None:
        is_deleted = await ShortURLRepository(self._session).delete(short_code)

        if not is_deleted:
            raise ShortURLNotFoundError(short_code)

        await self._session.commit()

    async def increment_access_count(self, short_code: str) -> ShortURL:
        repository = ShortURLRepository(self._session)
        short_url = await repository.get(short_code)

        if short_url is None:
            raise ShortURLNotFoundError(short_code)

        await repository.increment_access_count(short_code)

        await self._session.commit()
        return short_url
