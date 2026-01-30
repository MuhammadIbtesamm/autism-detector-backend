import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 📁 Get absolute path to this folder (app/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📄 Database file will be created inside the app folder
DB_PATH = os.path.join(BASE_DIR, "autism.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
