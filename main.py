from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends

from database_config import engine, Base
from sqlalchemy.orm import Session
from database_config import get_db


from modules.auth.auth_routers import router as auth_router


app = FastAPI(
  title="Tixxety",
  description="Tixxety API",
  version="1.0.0",
  contact={
    "name": "Prince Igwenaghga",
    "url": "https://linkedin.com/in/prince-igwenagha",
    "email": "princeigwe.c@gmail.com",
  },
)


origins = [
  "http://localhost:3000",
  "http://localhost:3001",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


Base.metadata.create_all(engine)


app.include_router(auth_router)



