from database.db import SessionDep
from modules.Book import BookModel
from modules.User import UserModel
from schemas.user_schema import UserSchema
from schemas.book_schema import BookSchema
from sqlalchemy import select
from typing import Annotated, Optional
from fastapi import Depends

class BookOpera:

    async def  add_book(data: BookSchema, session: SessionDep):
        new_book = BookModel(
            title = data.title,
            author = data.author,
        )   
        session.add(new_book)
        await session.commit()
        return new_book


    async def get_by_id(book_id: int, session: SessionDep):
        result = await session.execute(select(BookModel).filter(BookModel.id == book_id))
        return result.scalar()
    
    async def get_all(session: SessionDep):
        query = select(BookModel)
        result = await session.execute(query)
        return result.scalars().all()

def get_book_opera():
    return BookOpera

AnBook_Opera = Annotated[BookOpera, Depends(get_book_opera)]



class UserOpera:

    async def add_user(data: UserSchema, session: SessionDep):
        new_user = UserModel(
            username = data.username,
            email = data.email,
            password = data.password,
        )   
        session.add(new_user)
        await session.commit()
        return new_user

    async def get_by_id(user_id: int, session: SessionDep):
        result = await session.execute(select(UserModel).filter(UserModel.id == user_id))
        return result.scalar()


    async def get_by_username(username: str ,session: SessionDep) -> Optional[UserModel]:
        result = await session.execute(select(UserModel).filter(UserModel.username == username))
        return result.scalar()
    
    async def get_by_email(email: str, session: SessionDep):
        result = await session.execute(select(UserModel).filter(UserModel.email == email))
        return result.scalar()

def get_user_opera():
    return UserOpera

def pwd_context(password: str, user_password: str) -> bool:
    if password == user_password:
        return True
    
AnUser_Opera = Annotated[UserOpera, Depends(get_user_opera)]