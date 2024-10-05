from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import sqlite3
import threading
import uvicorn

from starlette.staticfiles import StaticFiles

from CommandManager import CommandManager
from ConnectionManager import ConnectionManager



app = FastAPI()


conn = sqlite3.connect('numeros.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS numeros (id INTEGER PRIMARY KEY AUTOINCREMENT, numero INTEGER UNIQUE)')
conn.commit()


manager = ConnectionManager()
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
async def root():
    return {"message": "Servidor de Bingo em execução"}

# Página que mostra o último número recebido
@app.get("/last")
async def get_last():
    try:
        file = open("static/index_ultimo.html", "r")

        return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        return HTMLResponse(content="<h1> Erro no servidor </h1>", status_code=500)

# Página que mostra o histórico de números recebidos
@app.get("/history")
async def get_history():
    try:
        file = open("static/index_historico.html", "r")

        return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        return HTMLResponse(content="<h1> Erro no servidor </h1>", status_code=500)
    
# Endpoint WebSocket para o último número
@app.websocket("/ws/last")
async def websocket_endpoint_last(websocket: WebSocket):
    await manager.connect_last(websocket)
    try:
        cursor.execute("SELECT numero FROM numeros ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if result:
            await websocket.send_text(str(result[0]))
        else:
            await websocket.send_text("Nenhum número recebido ainda.")
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_last(websocket)

@app.websocket("/ws/history")
async def websocket_endpoint_history(websocket: WebSocket):
    await manager.connect_history(websocket)
    try:
        cursor.execute("SELECT numero FROM numeros")
        numeros = cursor.fetchall()
        history = [str(n[0]) for n in numeros]
        history_str = ','.join(history)
        await websocket.send_text(history_str)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_history(websocket)

# Função principal
def main():
    cm_manager = CommandManager(cursor,conn,manager)
    input_thread = threading.Thread(target=cm_manager.read_command)
    input_thread.daemon = True
    input_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
