from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.user_router import user_router
from routers.draw_router import draw_router
from routers.ws_figures_router import ws_figures_router

app = FastAPI()
app.title = "Api-PAINT"
app.version = "0.0.1"

origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(ErrorHandler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router)
app.include_router(draw_router)
app.include_router(ws_figures_router)

Base.metadata.create_all(bind=engine)