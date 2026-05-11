from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.health import router as health_router
from routes.chat import router as chat_router

app = FastAPI(
    title="SHL Assessment Recommender",
    version="1.0.0"
)


# Root endpoint for Railway health checks
@app.get("/")
def root():
    return {
        "message": "SHL Assessment Recommender API Running"
    }


# Dedicated health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(health_router)
app.include_router(chat_router)