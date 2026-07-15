from fastapi import Security, security,HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
import datetime
from repos.user_repository import find_user_by_username



class AuthHandler:
    security=HTTPBearer()
    pwd_context=CryptContext(schemes=["bcrypt"])
    secret_key="supersecret"
    
    def get_password_hash(self,password):
        return self.pwd_context.hash(password)
    
    def verify_password(self,password,hashed_password):
        return self.pwd_context.verify(password,hashed_password)
    
    def encode_token(self,user_id):
        payload={
            "exp":datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=30),
            "iat":datetime.datetime.now(datetime.timezone.utc),
            "sub":user_id
        }
        return jwt.encode(payload,self.secret_key,algorithm="HS256")
    
    def decode_token(self,token):
        try:
            payload=jwt.decode(token,self.secret_key,algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return HTTPException(status_code=401,detail="Token expired")
        except jwt.InvalidTokenError:
            return HTTPException(status_code=401,detail="Invalid token")
        
    def auth_wrapper(self,auth:HTTPAuthorizationCredentials=Security(security)):
        return self.decode_token(auth.credentials)
        
    def get_current_user(self,auth:HTTPAuthorizationCredentials=Security(security)):
        username=self.decode_token(auth.credentials)
        if username is None:
            raise HTTPException(status_code=401,detail="Could not validate credentials")
        user=find_user_by_username(username)
        if user is None:
            raise HTTPException(status_code=401,detail="Could not validate credentials")
        return user
        
        