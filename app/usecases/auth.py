from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.models import User
from app.repositories.users import UsersRepository
from app.schemas.auth import RegisterRequest
from app.schemas.user import UserPublic


class AuthUseCases:
    def __init__(self, users_repo: UsersRepository):
        self._users_repo = users_repo

    async def register(self, request: RegisterRequest) -> User:
        existing = await self._users_repo.get_by_email(request.email)
        if existing:
            raise ConflictError("Email already exists")

        hashed_password = get_password_hash(request.password)
        user = User(email=request.email, password_hash=hashed_password)
        # print(f"DEBUG --  регистрируем пользователя {request.email}")
        return await self._users_repo.create(user)

    async def login(self, email: str, password: str) -> str:
        user = await self._users_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")

        token = create_access_token(data={"sub": str(user.id)})
        # print(f"DEBUG --  выдали токен пользователю id={user.id}")
        return token

    async def get_profile(self, user_id: int) -> UserPublic:
        user = await self._users_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return UserPublic.model_validate(user)
