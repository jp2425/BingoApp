import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request,Body, HTTPException
from fastapi.responses import HTMLResponse
import threading
import uvicorn
from starlette import status
from starlette.responses import PlainTextResponse

from starlette.staticfiles import StaticFiles

from service.CommandManager import CommandManager
from service.ConnectionManager import ConnectionManager
from config import config
from fastapi.templating import Jinja2Templates

from repo.SQLiteRepo import SQLiteRepo
from service.WebsocketService import WebsocketService
from service.NumberService import NumberService

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
number_service = NumberService(repo,manager)
cm_manager = CommandManager(repo,number_service)
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
@app.get("/number", response_class=HTMLResponse)
async def get_history(request: Request):
    client_host = request.client.host
    if client_host not in config["page"]["number"]["allowed_IP"] and len(config["page"]["number"]["allowed_IP"]) != 0:
        raise HTTPException(status_code=403)

    return templates.TemplateResponse(
        request=request, name="number_insert_ui.html", context={"title": config["page"]["number"]["title"],"reset_button": config["page"]["number"]["button_reset"],"change_ui_button": config["page"]["number"]["button_change_ui"]}
    )

@app.get("/number_manual", response_class=HTMLResponse)
async def get_history(request: Request):
    client_host = request.client.host

    if client_host not in config["page"]["backup_restore"]["allowed_IP"] and len(config["page"]["number"]["allowed_IP"]) != 0:
        raise HTTPException(status_code=403)

    return templates.TemplateResponse(
        request=request, name="database_backup_restore.html", context={"title": config["page"]["history"]["title"],"container_title": config["page"]["history"]["container_title"]}
    )

@app.post("/api/number", response_class=HTMLResponse)
async def get_number(request: Request, numbers: str = Body(...)):
    # Parse the 'numbers' string, splitting by commas and converting to integers

    try:
        for num in numbers.split("=")[1].split(","):
            await number_service.insert_number_db(num)
    except Exception as e:
        return PlainTextResponse(content="Bad request: "+str(e), status_code=status.HTTP_400_BAD_REQUEST)
    return PlainTextResponse(content="Success", status_code=status.HTTP_200_OK)

@app.get("/api/number", response_class=HTMLResponse)
async def get_numbers():

    try:
            value = await number_service.get_all_numbers()
            print(value)
            return PlainTextResponse(content=json.dumps(value), status_code=status.HTTP_200_OK)

    except Exception as e:
        return PlainTextResponse(content="Bad request: "+str(e), status_code=status.HTTP_400_BAD_REQUEST)


@app.delete("/api/number/{id}", response_class=HTMLResponse)
async def delete_number(request: Request, id: int):
    try:
        await number_service.delete_number_db(id)
    except Exception as e:
        return PlainTextResponse(content="Bad request: " + str(e), status_code=status.HTTP_400_BAD_REQUEST)

    return PlainTextResponse(content="Success", status_code=status.HTTP_200_OK)

@app.delete("/api/number_all", response_class=HTMLResponse)
async def delete_number(request: Request):
    try:
        await number_service.clear_db()
    except Exception as e:
        return PlainTextResponse(content="Bad request: " + str(e), status_code=status.HTTP_400_BAD_REQUEST)

    return PlainTextResponse(content="Success", status_code=status.HTTP_200_OK)

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

    input_thread = threading.Thread(target=cm_manager.read_command)
    input_thread.daemon = True
    input_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
