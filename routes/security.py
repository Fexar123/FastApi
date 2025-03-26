from database.db import SessionDep
from modules.User import UserModel
from email_validator import (
    validate_email,
    EmailNotValidError,
)
from fastapi import Depends
from sqlalchemy import select

from operations import pwd_context, AnUser_Opera 

async def authenticate_user(username_or_email: str,password: str, session: SessionDep) -> UserModel | None:
        try:
            validate_email(username_or_email)
            query_filter =  UserModel.email
        except EmailNotValidError:
              query_filter = UserModel.username
        result = await session.execute(select(UserModel).filter(query_filter == username_or_email))
        user = result.scalars().first()
        if not user or not pwd_context(password, user.password):
              return
        return user

SECRET_KEY = "my_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

def create_access_token(data: dict) -> str:
      to_encode = data.copy()
      expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
      return encoded_jwt

async def decode_access_token(token: str, session: SessionDep) -> UserModel | None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
        except JWTError:
              return
        if not username:
              return
        user = await AnUser_Opera.get_by_username(username,session)
        return user

from fastapi import (
APIRouter,
Depends,
HTTPException,
status,
)
from fastapi.security import (
OAuth2PasswordRequestForm,
OAuth2PasswordBearer
)
from schemas.Token import Token

router = APIRouter()

@router.post("/token", response_model=Token)
async def get_user_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
          raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, details="Incorrect username or password")
    access_token  = create_access_token(data = {"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/users/me")
async def read_user_me(session: SessionDep, token: str = Depends(oauth2_scheme)):
      user = await decode_access_token(token, session)
      if not user:
            raise HTTPException(status_code = 403, detail="User not authorized")
      return {"description": f"{user.username}"}
