
from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException, Response, File, UploadFile
from fastapi.responses import FileResponse
from ws.chat import router
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from myqrcode.code import image
from database.db import engine
from modules.Book import Base
from modules.User import Base, UserModel
from schemas.book_schema import UserLoginSchema
from routes.book_routes import router as book_router
from routes.user_router import router as user_router
from routes.security import router as sec_router
from routes.github_login_router import router as git_router
from GitHubAuth.third_party_login import resolve_github_token

image.save("qrcode.png")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (лучше указывать конкретные)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, WebSocket и т.д.)
    allow_headers=["*"],  # Разрешить любые заголовки
)

app.include_router(book_router)
app.include_router(user_router)
app.include_router(sec_router)
app.include_router(git_router)




@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok":True}

@app.post("/files")
async def upload_file(uploaded_file: UploadFile):  
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"1_{filename}", "wb") as f:
        f.write(file.read())

@app.get("/files/{filename}")
async def get_file(filename: str):
    return FileResponse(filename)

@app.get("/home")
async def home_page(user: UserModel = Depends(resolve_github_token)):
    return {"message": f"logged in {user.username}"}



if __name__ == "__main__":
    uvicorn.run("main:app",reload = True, port = 8001)

    