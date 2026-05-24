import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.db import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down API")


app = FastAPI(title="scex API", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Welcome to the scex API!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)