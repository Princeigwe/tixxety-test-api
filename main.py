from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends

from database_config import engine, Base
from sqlalchemy.orm import Session
from database_config import get_db


from modules.auth.auth_routers import router as auth_router
from modules.events import event_routers
from modules.tickets import ticket_routers, ticket_services


from apscheduler.schedulers.background import BackgroundScheduler
import atexit

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
app.include_router(event_routers.router)
app.include_router(ticket_routers.router)


# cron job operation to run background task to expire unpaid tickets at 1-minute intervals
scheduler = BackgroundScheduler()
scheduler.add_job(ticket_services.expire_unpaid_tickets, 'interval', minutes=1) 
scheduler.start()


@atexit.register
def shutdown_background_services():
  print("Shutting down background services")
  scheduler.shutdown() 