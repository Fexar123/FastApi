import httpx
from fastapi import APIRouter, HTTPException, status
from routes.security import Token
from GitHubAuth.third_party_login import (
GITHUB_AUTHORIZATION_URL,
GITHUB_CLIENT_ID,
GITHUB_CLIENT_SECRET,
GITHUB_REDIRECT_URI,
)

router = APIRouter()

@router.get("/auth/url")
async def github_login():
    return {
        "auth_url": GITHUB_AUTHORIZATION_URL + f"?client_id={GITHUB_CLIENT_ID}"
    }

@router.get("/github/auth/token", response_model=Token)
async def github_callback(code: str):
    token_respone = httpx.post("https://github.com/login/oauth/access_token",
    data={"client_id": GITHUB_CLIENT_ID,
    "client_secret": GITHUB_CLIENT_SECRET,
    "code": code,
    "redirect_uri": GITHUB_REDIRECT_URI,},
    headers={"Accept": "application/json"},).json()
    access_token = token_respone.get("access_token")
    if not access_token:
        raise HTTPException(
    status_code=401,
    detail="User not registered",
    )
    token_type = token_respone.get("token_type", "bearer")
    return {"access_token": access_token, "token_type": token_type}


