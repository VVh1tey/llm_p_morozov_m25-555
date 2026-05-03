import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str
    system: str | None = None
    max_history: int = 10
    temperature: float = Field(0.1, ge=0, le=1)


class ChatResponse(BaseModel):
    answer: str


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
