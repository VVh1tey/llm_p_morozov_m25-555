from app.core.config import settings
from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessagesRepository
from app.schemas.chat import ChatRequest
from app.services.openrouter_client import OpenRouterClient


class ChatUseCases:
    def __init__(
        self,
        chat_repo: ChatMessagesRepository,
        or_client: OpenRouterClient,
    ):
        self._chat_repo = chat_repo
        self._or_client = or_client

    async def ask(self, user_id: int, request: ChatRequest) -> str:
        messages = []

        # если есть системная инструкция — добавляем первым
        if request.system:
            messages.append({"role": "system", "content": request.system})

        history = await self._chat_repo.get_last_n(user_id, request.max_history)
        history.reverse()
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # добавляем текущий запрос пользователя
        messages.append({"role": "user", "content": request.prompt})

        # сохраняем запрос пользователя в историю
        await self._chat_repo.add(
            ChatMessage(user_id=user_id, role="user", content=request.prompt)
        )

        # print(f"DEBUG --  отправляем {len(messages)} сообщений в модель")
        answer = await self._or_client.get_completion(
            messages=messages,
            model=settings.OPENROUTER_MODEL,
            temperature=request.temperature,
        )

        await self._chat_repo.add(
            ChatMessage(user_id=user_id, role="assistant", content=answer)
        )

        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> list[ChatMessage]:
        msgs = await self._chat_repo.get_last_n(user_id, limit)
        msgs.reverse()
        return msgs

    async def clear_history(self, user_id: int) -> None:
        await self._chat_repo.delete_all_by_user_id(user_id)
