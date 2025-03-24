GITHUB_CLIENT_ID = "Ov23liAUD6SkxRnBDFF4"
GITHUB_CLIENT_SECRET = ("e2e83003ef89b1afc6d5c3e49b6d0c1d5a43aab5")

GITHUB_REDIRECT_URI = (
"http://localhost:8000/github/auth/token"
)
GITHUB_AUTHORIZATION_URL = (
"https://github.com/login/oauth/authorize"
)


import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2
from sqlalchemy.orm import Session
from modules import User
from database.db import SessionDep
from operations import AnUser_Opera



def resolve_github_token(session: SessionDep, AnUser: AnUser_Opera, access_token: str = Depends(OAuth2())) -> User:
    user_response = httpx.get("https://api.github.com/user", headers={"Authorization": access_token }).json()
    username = user_response.get("login", " ")
    user = AnUser.get_by_username(username, session)
    if not user:
        email = user_response.get("email", " ")
        user = AnUser.get_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=403,detail="Token not valid"
        )
    return user