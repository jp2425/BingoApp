from service.ConnectionManager import ConnectionManager
from repo.RepoAbsClass import RepoAbsClass
from fastapi import  WebSocket, WebSocketDisconnect

class WebsocketService:
    """
    Class responsibble to process the websockets requests.
    """

    def __init__(self, repo: RepoAbsClass, manager: ConnectionManager):
        self._repo = repo
        self._manager = manager

    async def handle_connection_last_endpoint(self,websocket: WebSocket):
        """
        Handler for the connection on "/ws/last" endpoint.
        :param websocket: websocket
        :return:
        """
        await self._manager.connect_last(websocket)
        try:
            last_entry = self._repo.get_last()
            await websocket.send_text(str(last_entry))
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            self._manager.disconnect_last(websocket)

    async def handle_connection_history_endpoint(self,websocket: WebSocket):
        """
        Handler for the connection on "/ws/history" endpoint.
        :param websocket: websocket
        :return:
        """
        await self._manager.connect_history(websocket)
        try:
            numbers = self._repo.get_all_numbers()
            history = [str(n[0]) for n in numbers]
            history_str = ','.join(history)
            await websocket.send_text(str(history_str))
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            self._manager.disconnect_last(websocket)