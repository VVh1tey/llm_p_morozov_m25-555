from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import AsyncSessionLocal
from app.repositories.chat_messages import ChatMessagesRepository
from app.repositories.users import UsersRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCases
from app.usecases.chat import ChatUseCases

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(
    session: AsyncSession = Depends(get_db_session),
) -> UsersRepository:
    return UsersRepository(session)


def get_chat_messages_repo(
    session: AsyncSession = Depends(get_db_session),
) -> ChatMessagesRepository:
    return ChatMessagesRepository(session)


def get_openrouter_client() -> OpenRouterClient:
    return OpenRouterClient()


def get_auth_usecases(
    users_repo: UsersRepository = Depends(get_users_repo),
) -> AuthUseCases:
    return AuthUseCases(users_repo)


def get_chat_usecases(
    chat_repo: ChatMessagesRepository = Depends(get_chat_messages_repo),
    or_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCases:
    return ChatUseCases(chat_repo, or_client)


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    # print(f"DEBUG -- payload из токена: {payload}")
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(payload["sub"])
