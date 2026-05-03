from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecases, get_current_user_id
from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCases

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserPublic)
async def register(
    request: RegisterRequest, uc: AuthUseCases = Depends(get_auth_usecases)
):
    try:
        user = await uc.register(request)
        return UserPublic.model_validate(user)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uc: AuthUseCases = Depends(get_auth_usecases),
):
    try:
        access_token = await uc.login(form_data.username, form_data.password)
        return TokenResponse(access_token=access_token)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    uc: AuthUseCases = Depends(get_auth_usecases),
):
    try:
        return await uc.get_profile(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
