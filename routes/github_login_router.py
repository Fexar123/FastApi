import httpx
from fastapi import APIRouter, HTTPException, status
from routes.security import Token
from third_party_login import (
GITHUB_AUTHORIZATION_URL,
GITHUB_CLIENT_ID,
GITHUB_CLIENT_SECRET,
GITHUB_REDIRECT_URI,
)