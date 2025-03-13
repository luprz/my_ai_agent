from app.utils.chat_agent import ChatAgent
from app.tools.calculator import CalculatorTool
from app.llms.gemini.model import Gemini
from app.agents.main_agent.personality import SYSTEM_MESSAGE
from app.memories.buffer_memory import BufferMemory
from pydantic import BaseModel
from typing import Type

class MainAgentInput(BaseModel):
    input: str
    session_id: str

class MainAgent:
    """Main assistant agent

    This class implements an AI assistant using LangChain and Gemini 2.0 Flash.
    """
    name: str = "main_assistant"
    description: str = """AI assistant using LangChain and Gemini 2.0 Flash"""
    args_schema: Type[BaseModel] = MainAgentInput
    
    def execute(self, session_id: str, input: str):
        try:
            agent = ChatAgent(
                llm=Gemini.get_llm(model="models/gemini-2.0-flash", temperature=0.5),
                system_message=SYSTEM_MESSAGE,
                tools=[CalculatorTool()],
                memory=BufferMemory(session_id=session_id, interactions=30)
            )
            return agent.execute(input)
        except Exception as e:
            print(e)
            return "I apologize, but I encountered an error while processing your request. Please try again."
        