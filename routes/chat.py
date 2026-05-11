from fastapi import APIRouter

from models.schemas import (
    ChatRequest,
    ChatResponse
)

from services.agent import SHLAgent

router = APIRouter()

agent = SHLAgent()


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat_endpoint(
    request: ChatRequest
):

    result = agent.chat(
        [
            message.dict()
            for message in request.messages
        ]
    )

    return result