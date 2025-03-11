from fastapi import WebSocket
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        try:
            await websocket.accept()
            self.active_connections[session_id] = websocket
            logger.info(f"Client #{session_id} connected successfully")
        except Exception as e:
            logger.error(f"Error connecting client #{session_id}: {str(e)}")
            raise

    def disconnect(self, websocket: WebSocket):
        try:
            # Find and remove the session associated with this websocket
            for session_id, conn in list(self.active_connections.items()):
                if conn == websocket:
                    del self.active_connections[session_id]
                    logger.info(f"Client #{session_id} disconnected")
                    break
        except Exception as e:
            logger.error(f"Error during disconnect: {str(e)}")

    async def send_personal_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(message)
                logger.debug(f"Personal message sent to client #{session_id}")
            except Exception as e:
                logger.error(f"Error sending personal message to client #{session_id}: {str(e)}")
                # Remove dead connection
                del self.active_connections[session_id]
                raise

    async def broadcast(self, message: str, session_id: str = None):
        try:
            if session_id:
                if session_id in self.active_connections:
                    await self.active_connections[session_id].send_text(message)
                    logger.debug(f"Message broadcasted to client #{session_id}")
                else:
                    logger.warning(f"Client #{session_id} not found in active connections")
            else:
                for session_id, connection in list(self.active_connections.items()):
                    try:
                        await connection.send_text(message)
                        logger.debug(f"Message broadcasted to client #{session_id}")
                    except Exception as e:
                        logger.error(f"Error broadcasting to client #{session_id}: {str(e)}")
                        del self.active_connections[session_id]
        except Exception as e:
            logger.error(f"Error during broadcast: {str(e)}")
            raise

manager = ConnectionManager()
