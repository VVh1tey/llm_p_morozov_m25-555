from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ChatMessage


class ChatMessagesRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, message: ChatMessage) -> ChatMessage:
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        # print(f"DEBUG --  сохранено сообщение role={message.role} user_id={message.user_id}")
        return message

    async def get_last_n(self, user_id: int, n: int) -> list[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(n)
        )
        result = await self._session.execute(stmt)
        msgs = list(result.scalars().all())
        # print(f"DEBUG --  получено {len(msgs)} сообщений для user_id={user_id}")
        return msgs

    async def delete_all_by_user_id(self, user_id: int):
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()
