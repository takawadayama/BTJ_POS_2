import os
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = 'C:/Users/waday/Step4/POS_new/backend/.env'
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
SSL_CA = os.getenv("SSL_CA")

# Create SQLAlchemy engine with SSL connection arguments
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": SSL_CA,
            "cert_reqs": "CERT_REQUIRED"
        }
    }
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Inventory table
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)

def create_and_populate_table():
    # Create a new session
    session = SessionLocal()
    try:
        # Drop the table if it already exists
        Inventory.__table__.drop(engine, checkfirst=True)
        print("Finished dropping table (if existed).")

        # Create the table
        Base.metadata.create_all(engine)
        print("Finished creating table.")

        # Insert some data into the table
        session.add_all([
            Inventory(name='banana', quantity=150),
            Inventory(name='orange', quantity=154),
            Inventory(name='apple', quantity=100)
        ])
        session.commit()
        print("Inserted data into table.")

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()
        print("Done.")

if __name__ == "__main__":
    create_and_populate_table()
