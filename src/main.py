from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routes import router
from src.storage import initialize_storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_storage()
    yield


app = FastAPI(
    title="Smart Expense Tracker API",
    description="A REST API for tracking and managing personal expenses efficiently.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)