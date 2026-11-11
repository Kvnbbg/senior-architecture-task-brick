"""Application entry point – minimal FastAPI setup for the isolated brick."""
from fastapi import FastAPI

from app.router import router

app = FastAPI(
    title="Senior Task Brick",
    description="Strictly typed, isolated Task management service demonstrating senior architecture.",
    version="1.0.0",
)

app.include_router(router)
