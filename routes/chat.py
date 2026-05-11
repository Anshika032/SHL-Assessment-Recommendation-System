from fastapi import APIRouter, HTTPException

from models.schemas import ChatRequest
from services.agent import SHLAgent

router = APIRouter()

# Lazy-loaded global agent
agent = None


@router.post("/chat")
async def chat(request: ChatRequest):
    global agent

    try:
        # Initialize only on first request
        if agent is None:
            print("Initializing SHL Agent...")
            agent = SHLAgent()

        response = agent.chat(request.query)

        return {
            "query": request.query,
            "response": response
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )