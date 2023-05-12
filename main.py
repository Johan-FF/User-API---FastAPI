from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.user_router import user_router

app = FastAPI()
app.title = "Api-PAINT"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)