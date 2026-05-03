from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def create(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        # print(f"DEBUG --  создан пользователь id={user.id} email={user.email}")
        return user
