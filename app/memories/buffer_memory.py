from typing import List, Dict
from threading import Lock
from langchain_core.messages import AIMessage, HumanMessage

class BufferMemory:
    """Buffer memory class for storing session-based chat history.

    This class implements a buffer memory mechanism for storing and retrieving
    chat history with session support. It provides thread-safe methods to add
    messages to the buffer and retrieve the chat history as a list of messages.
    """
    _instance = None
    _sessions: Dict[str, List] = {}
    _lock = Lock()

    def __new__(cls, session_id: str = "default", interactions: int = 50):
        if cls._instance is None:
            cls._instance = super(BufferMemory, cls).__new__(cls)
            cls._instance.interactions = interactions
        return cls._instance

    def __init__(self, session_id: str = "default", interactions: int = 50):
        """Initialize the buffer memory with session support.
        
        Args:
            session_id: The unique identifier for the chat session.
            interactions: Maximum number of interactions to keep (default: 50)
        """
        self.session_id = session_id
        self.interactions = interactions

    def add_message(self, human: str, ai: str):
        """Add a message to the session buffer.
        Args:
            human: The human message to be added to the buffer.
            ai: The AI response to be added to the buffer.
        """
        with self._lock:
            if self.session_id not in self._sessions:
                self._sessions[self.session_id] = []
            
            self._sessions[self.session_id].extend([
                HumanMessage(content=human),
                AIMessage(content=ai)
            ])
            
            # Remove old messages if exceeding the interactions limit
            if len(self._sessions[self.session_id]) > self.interactions * 2:
                self._sessions[self.session_id] = self._sessions[self.session_id][-self.interactions * 2:]

    def get_chat_history(self) -> List:
        """Retrieve the chat history for the current session.
        Returns:
            List: A list of chat history messages for the current session.
        """
        with self._lock:
            return self._sessions.get(self.session_id, [])

    def get_all_chat_history(self) -> List:
        """Retrieve all messages from the current session buffer.
        Returns:
            List: A list of all chat messages for the current session.
        """
        return self.get_chat_history()

    def clear_session(self):
        """Clear the chat history for the current session."""
        with self._lock:
            if self.session_id in self._sessions:
                del self._sessions[self.session_id]

    def set_session(self, session_id: str):
        """Set the current session ID.
        Args:
            session_id: The new session ID to switch to.
        """
        self.session_id = session_id