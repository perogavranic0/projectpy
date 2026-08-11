from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
db_url = "postgresql://postgres:YOURPASSWORD!@localhost:5432/application"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)