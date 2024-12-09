from pydantic import BaseModel,Field
import uuid
from datetime import datetime

class UserCreateModel(BaseModel):
    first_name:str=Field(max_length=40)
    last_name:str=Field(max_length=40)
    username:str=Field(max_length=40)
    email:str=Field(max_length=40)
    password:str=Field(max_length=20,min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool
    password_hash:str=Field(exclude=True)
    created_at:datetime
    updated_at:datetime

class UserLoginModel(BaseModel):
    email:str=Field(max_length=40)
    password:str=Field(max_length=20,min_length=6)