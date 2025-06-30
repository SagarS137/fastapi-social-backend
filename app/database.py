from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
# try:
#     conn = psycopg2.connect(host="localhost", dbname="fastapi", user="postgres",
#                             password="12345678", cursor_factory=RealDictCursor)  # Connect to PostgreSQL database
#     cursor = conn.cursor()                # Create a cursor to execute SQL queries
#     print("Database connection successful")

# except Exception as e:
#     print("Database connection failed")
#     print(e)
#     time.sleep(3)
