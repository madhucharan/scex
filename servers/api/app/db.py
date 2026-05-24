from app.core.config import settings
from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.models.user import User

engine = create_async_engine(
    settings.database_url,
    connect_args={"ssl": "require"},
    echo=True,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with AsyncSession(engine) as session:
        yield session
