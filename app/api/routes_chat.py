from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecases, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatMessageOut, ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCases

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def ask(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCases = Depends(get_chat_usecases),
):
    try:
        answer = await uc.ask(user_id, request)
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )


@router.get("/history", response_model=list[ChatMessageOut])
async def get_history(
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCases = Depends(get_chat_usecases),
):
    return await uc.get_history(user_id)


@router.delete("/history")
async def delete_history(
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCases = Depends(get_chat_usecases),
):
    await uc.clear_history(user_id)
    return {"message": "История очищена"}
