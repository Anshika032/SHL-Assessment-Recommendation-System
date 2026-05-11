from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.chat import router as chat_router

app = FastAPI(
    title="SHL Assessment Recommender"
)


@app.get("/")
def root():

    return {
        "message": (
            "SHL Assessment "
            "Recommender API Running"
        )
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health_router
)

app.include_router(
    chat_router
)