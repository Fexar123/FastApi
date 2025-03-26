from fastapi import APIRouter, status, HTTPException
from database.db import SessionDep
from schemas.user_schema import UserSchema, UserResponse, UserSchemaPrem
from operations import AnUser_Opera


router = APIRouter()

@router.post("/user", tags=["User"], summary="Создание юзера")
async def register_user(data: UserSchema, session: SessionDep, result: AnUser_Opera) -> UserResponse:
    return await result.add_user(data, session)

@router.get("/user/{user_id}", tags=["User"], summary="Получить юзера по id")
async def get_user_by_id(user_id: int, session: SessionDep, result: AnUser_Opera):
    return await result.get_by_id(user_id, session)

@router.get("/user/{username}", tags=["User"], summary="Получить юзера по username")
async def get_user_by_username(username: str, session: SessionDep, result: AnUser_Opera):
    return await result.get_by_username(username, session)

@router.post("/register/premium-user", tags=["User"], status_code=status.HTTP_201_CREATED)
async def register_premium_user(user: UserSchemaPrem, session: SessionDep)->UserResponse:
    user = await AnUser_Opera.add_user(user, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail = " username or email already exists")
    return  user
    

