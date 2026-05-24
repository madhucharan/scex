from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password_hash: Optional[str] = Field(default=None)
    auth_provider: Optional[str] = Field(default="local")
    created_at: datetime = Field(default_factory=datetime.now)

