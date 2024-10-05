from fastapi import  WebSocket


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
        for connection in self.active_connections_last:
            await connection.send_text(message)

    async def send_history(self, message: str):
        for connection in self.active_connections_history:
            await connection.send_text(message)
