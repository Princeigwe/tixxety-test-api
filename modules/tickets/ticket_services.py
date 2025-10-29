from fastapi import Depends, HTTPException, status
from database_config import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import DatabaseError