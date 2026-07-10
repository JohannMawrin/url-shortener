from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ShortURL(Base):
    __tablename__ = "short_urls"

    url: Mapped[str] = mapped_column(String(2048))
    short_code: Mapped[str] = mapped_column(String(8), unique=True)
    access_count: Mapped[int] = mapped_column(default=0)
