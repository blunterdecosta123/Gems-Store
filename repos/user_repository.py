from db.db import engine
from sqlmodel import Session,select
from models.user_models import *

def select_all_users():
    with Session(engine) as session:
        statements=select(User)
        res=session.exec(statements).all()
        return res
    
def find_user_by_username(username:str):
    with Session(engine) as session:
        statements=select(User).where(User.username==username)
        res=session.exec(statements).first()
        return res
        