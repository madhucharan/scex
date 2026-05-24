from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models.schemas import SignUpRequest, LoginRequest, AuthResponse
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup(data: SignUpRequest, session: AsyncSession = Depends(get_session)):
    user, error = await auth_service.signup(data.email, data.password, session)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return {"message": "User created successfully", "user_id": user.id}

@router.post("/login", response_model=AuthResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    token, error = await auth_service.login(data.email, data.password, session)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return AuthResponse(access_token=token)