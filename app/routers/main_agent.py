from typing import List
from fastapi import APIRouter
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from app.workflows.main_workflow import MainWorkflow
from app.events.main_assistant_event import main_assistant_event
from app.memories.buffer_memory import BufferMemory

# Create a router for agent-related endpoints
router = APIRouter(prefix="/api/main_agent", tags=["main_agent"])

# Define the input model for better Swagger documentation
class ConversationInput(BaseModel):
    session_id: str = Field(
       ...,
        description="The unique identifier for the chat session",
        example="3-a456-426614174000"
    )
    input: str = Field(
        ...,
        description="The input text for the conversation",
        example="What is the weather today?"
    )

    class Config:
        schema_extra = {
            "example": {
                "input": "What is the weather today?"
            }
        }

class ConversationResponse(BaseModel):
    response: str = Field(
        ...,
        description="The assistant's response to the conversation",
        example="The weather today is sunny with a high of 75°F."
    )

class TaskResponse(BaseModel):
    task_id: str = Field(
        ...,
        description="The ID of the background task",
        example="123e4567-e89b-12d3-a456-426614174000"
    )

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: str = None

class ChatHistoryResponse(BaseModel):
    messages: List[dict] = Field(
        ...,
        description="List of chat messages with their content and role",
        example=[
            {"role": "human", "content": "What is the weather today?"},
            {"role": "assistant", "content": "The weather today is sunny with a high of 75°F."}
        ]
    )

@router.get("/conversation/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str):
    memory = BufferMemory()
    messages = memory.get_chat_history()
    formatted_messages = [
        {"role": "human" if isinstance(msg, HumanMessage) else "assistant", "content": msg.content}
        for msg in messages
    ]
    return ChatHistoryResponse(messages=formatted_messages)


@router.post("/conversation", response_model=ConversationResponse)
async def conversation(
    input_data: ConversationInput
):
    assistant = MainWorkflow()
    return ConversationResponse(response=assistant.run(session_id=input_data.session_id, input=input_data.input))

@router.post("/conversation/async", response_model=TaskResponse)
async def conversation_async(
    input_data: ConversationInput
):
    task = main_assistant_event.delay(session_id=input_data.session_id, input=input_data.input)
    return TaskResponse(task_id=task.id)

@router.get("/conversation/status/{task_id}", response_model=TaskStatusResponse)
async def get_conversation_status(task_id: str):
    task = main_assistant_event.AsyncResult(task_id)
    return TaskStatusResponse(
        task_id=task_id,
        status=task.status,
        result=task.result if task.ready() else None
    )

