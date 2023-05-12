from fastapi import Path, Query, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bcrypt import checkpw
from typing import List
from middlewares.jwt_bearer import JWTBearer
from utils.jwt_manager import create_token
from utils.cryp_manager import generate_encrypt
from services.user_service import UserService
from schemas.user_schema import UserSchema
from schemas.user_login_schema import UserLoginSchema
from config.database import Session, engine
from sqlalchemy import MetaData, Table
import datetime

user_router = APIRouter()

@user_router.get('/users', 
        tags=['users'],
        response_model=List[UserSchema],
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_users() -> List[UserSchema]:
    db = Session()
    result = UserService(db).get_users()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@user_router.get('/users/{id}',
        tags=['users'],
        response_model=UserSchema,
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_user(id: int = Path(ge=1, le=2000)) -> UserSchema:
    db = Session()
    result = UserService(db).get_user(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"user not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@user_router.get('/users/',
        tags=['users'],
        response_model=List[UserSchema],
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_users_by_nickname(nickname: str = Query(max_length=20)) -> List[UserSchema]:
    db = Session()
    result = UserService(db).get_user_by_nickname(nickname)
    return JSONResponse(status_code=200, content=jsonable_encoder[result])

@user_router.post('/users',
        tags=['users'],
        response_model=dict,
        status_code=201)
def create_user(user: UserSchema) -> dict:
    db = Session()
    created = UserService(db).create_user(user)
    if not created:
        return JSONResponse(status_code=200, content={"message":"user exists"})
    return JSONResponse(status_code=201, content={"message":"sucess"})

@user_router.put('/users/{id}',
        tags=['users'],
        response_model=dict,
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def update_user(user: UserSchema, id: int = Path(ge=1, le=2000)) -> dict:
    db = Session()
    is_update = UserService(db).update_user(id, user)
    if not is_update:
        return JSONResponse(status_code=404, content={"message":"user not found"})
    return JSONResponse(status_code=200, content={"message":"sucess"})

@user_router.delete('/users/{id}',
        tags=['users'],
        response_model=dict,
        dependencies=[Depends(JWTBearer())])
def delete_user(id: int = Path(ge=1, le=2000)) -> dict:
    metadata = MetaData(bind=engine)
    mytable = Table('movies', metadata, autoload=True)
    mytable.drop(engine)
    db = Session()
    is_deleted = UserService(db).delete_user(id)
    if not is_deleted:
        return JSONResponse(status_code=404, content={"message":"user not found"})
    return JSONResponse(status_code=200, content={"message":"sucess"})

@user_router.post('/users/login',
        tags=['users'],
        status_code=200)
def login(user: UserLoginSchema):
    db = Session()
    result = UserService(db).get_user_by_email(user.email)
    if not result:
        return JSONResponse(status_code=404, content={"message":"email not found"})    

    confirm_password: str = generate_encrypt(user.password)
    if checkpw(result.password, confirm_password):
        return JSONResponse(status_code=404, content={"message":"invalid password"})

    token = create_token(user.dict())
    return JSONResponse(status_code=200, content={"message":token, "id":result.id})