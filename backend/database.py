from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = 'C:/Users/waday/Step4/POS_new/backend/.env'
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")
ssl_ca = os.getenv("SSL_CA")

if DATABASE_URL is None or ssl_ca is None:
    raise ValueError("DATABASE_URL and SSL_CA must be set")

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": ssl_ca
        }
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベースセッションの依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()