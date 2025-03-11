from typing import List
from langchain_core.messages import AIMessage, HumanMessage

class BufferMemory:
    """Buffer memory class for storing chat history.

    This class implements a buffer memory mechanism for storing and retrieving
    chat history. It provides methods to add messages to the buffer and retrieve
    the chat history as a list of messages.
    """

    def __init__(self):
        """Initialize the buffer memory."""
        self.chat_history = []

    def add_message(self, human: str, ai: str):
        """Add a message to the buffer.
        Args:
            human: The human message to be added to the buffer.
            ai: The AI response to be added to the buffer.
        """
        self.chat_history.extend([
          HumanMessage(content=human),
          AIMessage(content=ai
        )
    ])

    def get_chat_history(self):
        """Retrieve the chat history as a list of messages.
        Returns:
            List: A list of chat history messages.
        """
        return self.chat_history

    def get_all_chat_history(self) -> List:
        """Retrieve all messages from the buffer.
        Returns:
            List: A list of all chat messages.
        """
        return self.chat_history