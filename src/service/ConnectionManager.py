from fastapi import  WebSocket
from starlette.websockets import WebSocketState


class ConnectionManager:
    """
    Classe responsável por gerir as conexões de clientes.
    Mantém uma lista das conexões por tipo de conexão.
    """
    
    def __init__(self):
        self.active_connections_last = []
        self.active_connections_history = []

    async def connect_last(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections_last.append(websocket)

    def disconnect_last(self, websocket: WebSocket):
        if websocket in self.active_connections_last:
            self.active_connections_last.remove(websocket)

    async def connect_history(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections_history.append(websocket)

    def disconnect_history(self, websocket: WebSocket):
        if websocket in self.active_connections_history:
            self.active_connections_history.remove(websocket)

    async def send_last(self, message: str):
        for connection in self.active_connections_last[:]: # we should iterate through a copy of the list. Otherwise, if we change the list during iteration, it will lead to erroneous behavior
            try:
                await connection.send_text(message)
            except:
                self.active_connections_last.remove(connection)

    async def send_history(self, message: str):
        print(len(self.active_connections_history), " conexões")
        for connection in self.active_connections_history[:]:  # we should iterate through a copy of the list. Otherwise, if we change the list during iteration, it will lead to erroneous behavior
            print(len(self.active_connections_history), " conexões dentro")

            print("Tentando enviar historico")
            if connection.client_state == WebSocketState.CONNECTED:
                try:
                    await connection.send_text(message)
                    print("historico enviado")
                except:
                    self.active_connections_history.remove(connection)
                    print("removendo")
            else:
                self.active_connections_history.remove(connection)
                print("removendo")


