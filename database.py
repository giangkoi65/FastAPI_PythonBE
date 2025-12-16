from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "mysql://root:123456@localhost:3306/test_db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)