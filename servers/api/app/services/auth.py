from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

async def signup(email: str, password: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    existing_user = result.first()
    
    if existing_user:
        return None, "Email already registered"
    
    user = User(
        email=email,
        password_hash=hash_password(password),
        auth_provider="local"
    )
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return user, None


async def login(email: str, password: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.email == email))
    user = result.first()
    
    if not user:
        return None, "Invalid credentials"
    
    if user.auth_provider != "local":
        return None, "Please use Google login"
    
    if not verify_password(password, user.password_hash):
        return None, "Invalid credentials"
    
    token = create_access_token({"sub": str(user.id)})
    
    return token, None