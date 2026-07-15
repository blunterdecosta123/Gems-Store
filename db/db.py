from sqlmodel import create_engine,SQLModel
from sqlmodel import Session


engine =create_engine('sqlite:///database.db', echo=True) # echo=True will print the SQL statements
session=Session(bind=engine)