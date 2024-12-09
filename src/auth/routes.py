from fastapi import APIRouter,Depends,status
from datetime import timedelta
from src.db.main import get_sessions
from .schemas import UserCreateModel,UserModel,UserLoginModel
from .service import UserService
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from .utils import create_access_token,decode_token,verify_passwd

auth_router=APIRouter()
user_service=UserService()
REFRESH_TOKEN_EXPIRY=2

@auth_router.post("/signup",response_model=UserModel,status_code=status.HTTP_201_CREATED)    
async def create_user_account(user_data:UserCreateModel,session=Depends(get_sessions)):
    email=user_data.email
    user_exists=await user_service.user_exists(email,session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already exists")
    else:
        new_user=await user_service.create_user(user_data,session)
        return new_user


@auth_router.post("/login",response_model=UserModel,status_code=status.HTTP_200_OK)
async def login_users(login_data:UserLoginModel,session=Depends(get_sessions)):
    email=login_data.email
    password=login_data.password

    user=await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid=verify_passwd(password,user.password_hash)
        if password_valid:
            access_token=create_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid)
                }
            )
            refresh_token=create_access_token(
                user_data={
                    "email":user.email,
                    "user_uid":str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)
                    }
                }
            )
        
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")