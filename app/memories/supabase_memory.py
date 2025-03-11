import os
from langchain_core.messages import AIMessage, HumanMessage
from supabase import create_client
from typing import List

class SupabaseMemory:
    """Supabase memory class for storing chat history.

    This class implements a memory mechanism for storing and retrieving
    chat history using Supabase as the storage backend. It provides methods
    to add messages to the database and retrieve the chat history as a list
    of messages.
    """

    def __init__(self, session_id: str, interactions = 50, table_name: str = "chat_messages"):
        """Initialize the Supabase memory.
        
        Args:
            supabase_url: The URL of your Supabase project
            supabase_key: The API key for your Supabase project
            session_id: The unique identifier for the chat session
            table_name: The name of the table to store messages (default: 'chat_messages')
        """
        self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        self.table_name = table_name
        self.session_id = session_id
        self.interactions = interactions
        """Remove old messages to maintain a fixed context size.
        
        Args:
            max_rows: Maximum number of messages to keep (default: 50)
        """
        # Get total count of messages for this session
        count_response = self.supabase.table(self.table_name)\
            .select("*", count="exact")\
            .eq("session_id", self.session_id)\
            .execute()
        
        total_messages = count_response.count

        if total_messages > self.interactions:
            # Calculate how many messages to delete
            messages_to_delete = total_messages - self.interactions
            
            # Get the IDs of oldest messages to delete
            delete_response = self.supabase.table(self.table_name)\
                .select("id")\
                .eq("session_id", self.session_id)\
                .order('created_at', desc=False)\
                .limit(messages_to_delete)\
                .execute()

            # Delete all excess messages at once
            if delete_response.data:
                message_ids = [msg["id"] for msg in delete_response.data]
                self.supabase.table(self.table_name)\
                    .delete()\
                    .in_("id", message_ids)\
                    .execute()

    def add_message(self, human: str, ai: str):
        """Add a message pair to Supabase.
        
        Args:
            human: The human message to be added to the database
            ai: The AI response to be added to the database
        """
        # Insert the message pair into Supabase
        self.supabase.table(self.table_name).insert([
            {"role": "human", "content": human, "session_id": self.session_id},
            {"role": "ai", "content": ai, "session_id": self.session_id}
        ]).execute()

    def get_chat_history(self) -> List:
        """Retrieve the chat history as a list of messages.
        
        Returns:
            List: A list of chat history messages limited by interactions.
        """
        # Fetch messages from Supabase and order them by creation time
        response = self.supabase.table(self.table_name)\
            .select("*")\
            .eq("session_id", self.session_id)\
            .order('created_at', desc=True)\
            .limit(self.interactions * 2)\
            .execute()
        
        # Convert the database records to LangChain message format
        messages = []
        # Reverse the response data to get ascending order
        for record in reversed(response.data):
            if record["role"] == "human":
                messages.append(HumanMessage(content=record["content"]))
            else:
                messages.append(AIMessage(content=record["content"]))
        
        return messages

    def get_all_chat_history(self) -> List:
        """Retrieve all messages from Supabase.

        Returns:
            List: A list of all chat messages.
        """
        # Fetch all messages from Supabase and order them by creation time
        response = self.supabase.table(self.table_name)\
           .select("*")\
           .eq("session_id", self.session_id)\
          .order('created_at', desc=True)\
          .execute()
        # Convert the database records to LangChain message format
        messages = []
        # Reverse the response data to get ascending order
        for record in reversed(response.data):
            if record["role"] == "human":
                messages.append(HumanMessage(content=record["content"]))
            else:
                messages.append(AIMessage(content=record["content"]))
        return messages