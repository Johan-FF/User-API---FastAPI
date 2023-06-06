from fastapi import Path, Depends, APIRouter, Response, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from middlewares.jwt_bearer import JWTBearer
from services.draw_service import DrawService
from schemas.draw_schema import DrawSchema
from config.database import Session

draw_router = APIRouter()

@draw_router.get('/draws/owner/{id}',
        tags=['draws'],
        response_model=List[DrawSchema],
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_draws_by_owner(response: Response, id: int = Path(ge=1, le=2000)) -> List[DrawSchema]:
    db = Session()
    result = DrawService(db).get_draws_by_owner(id)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:4200"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    if result==[]:
        return JSONResponse(status_code=200, content=[])
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(result))

@draw_router.get('/draws/{id}',
        tags=['draws'],
        response_model=DrawSchema,
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_draw(id: int = Path(ge=1, le=2000)) -> DrawSchema:
    db = Session()
    result = DrawService(db).get_draw(id)
    if not result:
        return JSONResponse(status_code=404, content={"message":"draw not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@draw_router.get('/draws/exist/{name}',
        tags=['draws'],
        response_model=dict,
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def get_id_by_name(name: str = Path(min_length=1)) -> dict:
    db = Session()
    result = DrawService(db).get_id_by_name(name)
    return JSONResponse(status_code=200, content={"message":"sucess", "id": result})

@draw_router.post('/draws',
        tags=['draws'],
        response_model=dict,
        status_code=201,
        dependencies=[Depends(JWTBearer())])
def create_draw(draw: DrawSchema) -> dict:
    db = Session()
    created = DrawService(db).create_draw(draw)
    if not created:
        return JSONResponse(status_code=200, content={"message":"DrawError"})
    return JSONResponse(status_code=201, content={"message":"sucess", "id": DrawService(db).get_id_by_name(draw.name)})

@draw_router.put('/draws/{id}',
        tags=['draws'],
        response_model=dict,
        status_code=200,
        dependencies=[Depends(JWTBearer())])
def update_draw(draw: DrawSchema, id: int = Path(ge=1, le=2000)) -> dict:
    db = Session()
    is_update = DrawService(db).update_draw(id, draw)
    if not is_update:
        return JSONResponse(status_code=404, content={"message":"draw not found"})
    return JSONResponse(status_code=200, content={"message":"sucess"})

@draw_router.delete('/draws/{id}',
        tags=['draws'],
        response_model=dict,
        dependencies=[Depends(JWTBearer())])
def delete_user(id: int = Path(ge=1, le=2000)) -> dict:
    db = Session()
    is_deleted = DrawService(db).delete_draw(id)
    if not is_deleted:
        return JSONResponse(status_code=404, content={"message":"draw not found"})
    return JSONResponse(status_code=200, content={"message":"sucess"})
