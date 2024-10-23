from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Rule

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/rule_engine_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_rule_to_db(rule_string, db):
    rule = Rule(rule_string=rule_string)
    db.add(rule)
    db.commit()

def get_all_rules_from_db(db):
    return db.query(Rule).all()
