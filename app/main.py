from tokenize import String
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

# Static Files
from fastapi.staticfiles import StaticFiles
# CORS
from fastapi.middleware.cors import CORSMiddleware
# WebSocket
from fastapi import WebSocket, WebSocketDisconnect
# Pagination
from fastapi_pagination import add_pagination

from app.database import db
from app.routes import users
from app.routes.dashboard import dashboard
from app.routes.application import application
# from app.routes.join import invite, join

load_dotenv()

app = FastAPI()
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(application.router)
# app.include_router(invite.router)
# app.include_router(join.router)

# Cross-Origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pagination
add_pagination(app)

# WebSocket
from typing import List
from datetime import datetime
import json
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)

            message = {"time":current_time,"clientId":client_id,"message":data}
            print(message)
            await manager.broadcast(json.dumps(message))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        message = {"time":current_time,"clientId":client_id,"message":"Offline"}
        await manager.broadcast(json.dumps(message))

@app.on_event("startup")
def on_startup():
    db.create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8001, reload=False, debug=True, access_log=False)
