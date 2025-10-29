import os
from fastapi import HTTPException, status

from dotenv import load_dotenv
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone


load_dotenv(override=True)


ACCESS_SECRET_KEY = os.environ.get("JWT_SECRET")
ISSUER = os.environ.get("JWT_ISSUER")
ALGORITHM = "HS256"


async def create_access_token(payload: dict):
  expiry_time = datetime.now(timezone.utc) + timedelta(days=1)
  payload['exp'] = expiry_time
  payload['iss'] = ISSUER
  token = jwt.encode(payload, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
  return token


async def decode_access_token(token: str):
  try:
    decoded_payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM], issuer=ISSUER)
    if  decoded_payload['iss'] != ISSUER:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return decoded_payload
  except InvalidTokenError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")