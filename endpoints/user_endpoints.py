from auth.auth import AuthHandler
from fastapi import APIRouter,HTTPException
from models.user_models import *
from repos.user_repository import select_all_users,find_user_by_username
from sqlmodel import Session,select
from db.db import session
from fastapi.responses import JSONResponse
from fastapi import Depends

user_router=APIRouter()
auth_handler=AuthHandler()

@user_router.post("/registration",tags=["User"],status_code=201,description="Register a new user")
def register(user:UserInput):
    users=select_all_users()
    if any(user.username==u.username for u in users):
        raise HTTPException(status_code=400,detail="Username already exists")
    hashed_pwd=auth_handler.get_password_hash(user.password)
    u=User(username=user.username,password=hashed_pwd,email=user.email,is_seller=user.is_seller)
    session.add(u)
    session.commit()
    return JSONResponse(status_code=201,content={"message":"User registered successfully"})

@user_router.post("/login",tags=["User"],status_code=200,description="Login a user")
def login(user:UserLogin):
    user_found=find_user_by_username(user.username)
    if user_found is None:
        return HTTPException(status_code=404,detail="Invalid username or password")
    verified=auth_handler.verify_password(user.password,user_found.password)
    if not verified:
        return HTTPException(status_code=401,detail="Invalid username or password")
    
    token=auth_handler.encode_token(user_found.username)
    return {"token":token}

@user_router.get("/users/me",tags=["User"],status_code=200,description="Get current user")
def get_current_user(user=Depends(auth_handler.get_current_user)):
    return user.username