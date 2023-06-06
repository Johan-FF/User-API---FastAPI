from fastapi import Path, APIRouter, WebSocket
import json
from typing import Dict, List
from services.draw_service import DrawService
from utils.jwt_manager import draw_token
from config.database import Session

ws_figures_router = APIRouter()

active_connections: Dict[int, Dict[int,WebSocket]] = {}
"""
{
    # id del dibujo
    4: {
        3: ws, # id del usuario y el websocket asociado a el
        2: ws, # id del usuario y el websocket asociado a el
        1: ws # id del usuario y el websocket asociado a el
    },
    2: {
        4: ws,
        5: ws
    }
}

"""


@ws_figures_router.websocket(
        "/figures/ws/{drawing_id}/{user_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        drawing_id: int = Path(ge=1, le=2000),
        user_id: int = Path(ge=1, le=2000)):
    await websocket.accept()
    if drawing_id in active_connections:
        connections = active_connections[drawing_id]
    else:
        connections = {}
        active_connections[drawing_id] = connections
    if not user_id in connections:
        connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            json_data = json.loads(data)
            info_encode = draw_token(json_data)
            db = Session()
            draw = DrawService(db).get_draw(drawing_id)
            draw.details = info_encode
            db.close()
            json_data['users'] = list(connections.keys())
            complete_data = json.dumps(json_data)
            await send_figures_to_all(connections, user_id, str(complete_data))
    finally:
        del connections[user_id]
        if len(connections) == 0:
            del active_connections[drawing_id]

async def send_figures_to_all(connections, user_id, data):
    for id_user_connected, ws in connections.items():
        if not id_user_connected==user_id:
            await ws.send_text(data) 
