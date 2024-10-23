# app/__init__.py

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Initialize the database
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/rule_engine_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import the views (optional if not needed)
from app import ui
