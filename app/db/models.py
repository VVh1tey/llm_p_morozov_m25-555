import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # email уникальный, индекс для быстрого поиска
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str]
    role: Mapped[str] = mapped_column(String, default="user")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )

    chat_messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # внешний ключ на пользователя
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str]  # "user" или "assistant"
    content: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="chat_messages")
