import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self._base_url = settings.OPENROUTER_BASE_URL
        self._api_key = settings.OPENROUTER_API_KEY
        self._headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
        }

    async def get_completion(
        self, messages: list[dict], model: str, temperature: float
    ) -> str:
        async with httpx.AsyncClient() as client:
            try:
                # print(f"DEBUG --  отправляем запрос к модели {model}, сообщений: {len(messages)}")
                response = await client.post(
                    f"{self._base_url}/chat/completions",
                    headers=self._headers,
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                    },
                )
                response.raise_for_status()
                data = response.json()
                # print(f"DEBUG --  ответ от openrouter: {data}")
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(
                    f"OpenRouter вернул ошибку: {e.response.status_code} - {e.response.text}"
                )
            except (httpx.RequestError, KeyError, IndexError) as e:
                raise ExternalServiceError(f"Ошибка при обращении к OpenRouter: {e}")
