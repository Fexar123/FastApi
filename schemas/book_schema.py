from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    username: str
    password: str

class BookSchema(BaseModel):
    title: str
    author: str

class BookResponse(BookSchema):
    id: int
