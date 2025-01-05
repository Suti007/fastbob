from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# URL_DATABASE = "mysql+pymysql://root:Mopl2007@localhost:3308/todo_suti"
URL_DATABASE = "postgresql://postgres:Mopl2007@localhost:5432/todo_suti"
engine= create_engine(URL_DATABASE)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base= declarative_base()