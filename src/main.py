from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import threading
import uvicorn

from starlette.staticfiles import StaticFiles

from service.CommandManager import CommandManager
from service.ConnectionManager import ConnectionManager
from config import config
from fastapi.templating import Jinja2Templates

from repo.SQLiteRepo import SQLiteRepo
from service.WebsocketService import WebsocketService

# ############################
#   FastAPI initialization   #
# ############################

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ###########################
#    Repo and manager init  #
# ###########################

manager = ConnectionManager()
repo = SQLiteRepo()
service = WebsocketService(repo,manager)
# ###########################
#         Routing           #
# ###########################
@app.get("/")
async def root():
    return {"message": "Servidor de Bingo em execução"}


@app.get("/last", response_class=HTMLResponse)
async def get_last(request: Request):
    return templates.TemplateResponse(
        request=request, name="index_last.html", context={"title": config["page"]["last"]["title"],"container_title": config["page"]["last"]["container_title"]}
    )

@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request):
    return templates.TemplateResponse(
        request=request, name="index_history.html", context={"title": config["page"]["history"]["title"],"container_title": config["page"]["history"]["container_title"]}
    )
    
# ####################################
#         WebSocket endpoints        #
# ####################################

@app.websocket("/ws/last")
async def websocket_endpoint_last(websocket: WebSocket):
    await service.handle_connection_last_endpoint(websocket)

@app.websocket("/ws/history")
async def websocket_endpoint_history(websocket: WebSocket):
    await service.handle_connection_history_endpoint(websocket)

# Função principal
def main():

    cm_manager = CommandManager(repo,manager)
    input_thread = threading.Thread(target=cm_manager.read_command)
    input_thread.daemon = True
    input_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
