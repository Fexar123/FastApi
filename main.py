
from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException, Response, File, UploadFile
from fastapi.responses import FileResponse
from ws.chat import router
import uvicorn
from authx import AuthX, AuthXConfig
from fastapi.middleware.cors import CORSMiddleware
from myqrcode.code import image
from database.db import engine
from modules.Book import Base
from modules.User import Base
from schemas.book_schema import UserLoginSchema
from routes.book_routes import router as book_router
from routes.user_router import router as user_router
from routes.security import router as sec_router

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


config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)







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

@app.post("/login", tags = ["Token"])
def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code = 401, detail = "Incorrect username or password")




if __name__ == "__main__":
    uvicorn.run("main:app",reload = True, port = 8001)

    