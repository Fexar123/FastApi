from fastapi import APIRouter
from database.db import SessionDep
from schemas.book_schema import BookSchema, BookResponse
from operations import AnBook_Opera


router = APIRouter()

@router.post("/books",summary = "Добавить книгу в БД", tags = ["Book"])
async def add_book(data: BookSchema, session: SessionDep, result: AnBook_Opera) -> BookResponse:
    return await result.add_book(data, session)
   

@router.get("/books/{book_id}", response_model=BookSchema,tags = ["Book"], summary = "Получить одну книгу")
async def get_book_one(book_id: int ,result: AnBook_Opera, session: SessionDep):
    return await result.get_by_id(book_id, session)

@router.get("/books", tags = ["Book"], summary = "Получить все книги")
async def get_book(session: SessionDep, result: AnBook_Opera):
    return result.get_all(session)
