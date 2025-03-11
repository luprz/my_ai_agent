import os
from typing import List
from datetime import datetime
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

def get_chat_message_model(table_name: str):
    class ChatMessage(Base):
        __tablename__ = table_name

        id = Column(Integer, primary_key=True)
        session_id = Column(String(255), nullable=False)
        role = Column(String(50), nullable=False)
        content = Column(Text, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)

        __table_args__ = (
            Index('idx_session_created', 'session_id', 'created_at'),
            {'extend_existing': True}
        )
    return ChatMessage

class PostgresMemory:
    """PostgreSQL memory class for storing chat history using SQLAlchemy ORM.

    This class implements a memory mechanism for storing and retrieving
    chat history using PostgreSQL as the storage backend with SQLAlchemy ORM.
    It provides methods to add messages to the database and retrieve the
    chat history as a list of messages.
    """

    def __init__(self, session_id: str, interactions = 50, table_name: str = "chat_messages"):
        """Initialize the PostgreSQL memory.

        Args:
            session_id: The unique identifier for the chat session
            interactions: Maximum number of interactions to keep (default: 50)
            table_name: The name of the table to store messages (default: 'chat_messages')
        """
        postgres_url = os.getenv('POSTGRES_URL')
        if not postgres_url:
            raise ValueError("POSTGRES_URL environment variable is not set")
        self.engine = create_engine(postgres_url)

        # Get the ChatMessage model with the specified table name
        self.ChatMessage = get_chat_message_model(table_name)
        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.session_id = session_id
        self.interactions = interactions

    def add_message(self, human: str, ai: str):
        """Add a message pair to PostgreSQL.

        Args:
            human: The human message to be added to the database
            ai: The AI response to be added to the database
        """
        # Create message objects
        human_message = self.ChatMessage(
            session_id=self.session_id,
            role="human",
            content=human
        )
        ai_message = self.ChatMessage(
            session_id=self.session_id,
            role="ai",
            content=ai
        )

        # Add and commit both messages
        self.session.add(human_message)
        self.session.add(ai_message)
        self.session.commit()

    def get_chat_history(self) -> List:
        """Retrieve the chat history as a list of messages.

        Returns:
            List: A list of chat history messages limited by interactions.
        """
        # Fetch messages and order them by creation time
        records = self.session.query(self.ChatMessage)\
            .filter(self.ChatMessage.session_id == self.session_id)\
            .order_by(self.ChatMessage.created_at)\
            .limit(self.interactions * 2)\
            .all()

        # Convert the database records to LangChain message format
        messages = []
        for record in records:
            if record.role == "human":
                messages.append(HumanMessage(content=record.content))
            else:
                messages.append(AIMessage(content=record.content))

        return messages

    def get_all_chat_history(self) -> List:
        """Retrieve all messages from PostgreSQL.
        Returns:
            List: A list of all chat messages.
        """
        # Fetch all messages
        records = self.session.query(self.ChatMessage)\
            .filter(self.ChatMessage.session_id == self.session_id)\
            .order_by(self.ChatMessage.created_at)\
            .all()
        # Convert the database records to LangChain message format
        messages = []

        for record in records:
            if record.role == "human":
                messages.append(HumanMessage(content=record.content))
            else:
                messages.append(AIMessage(content=record.content))

        return messages

    def __del__(self):
        """Close the database session when the object is destroyed."""
        if hasattr(self, 'session'):
            self.session.close()
        if hasattr(self, 'engine'):
            self.engine.dispose()