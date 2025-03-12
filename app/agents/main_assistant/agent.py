from app.utils.agent import Agent
from app.tools.calculator import CalculatorTool
from app.llms.gemini.model import Gemini
from app.agents.main_assistant.personality import PERSONALITY
from app.memories.buffer_memory import BufferMemory

class MainAgent:
    """Agent class for apartment administration.

    This class implements an AI assistant that helps with the administration
    of horizontal apartment complexes using LangChain and Gemini 2.0 Flash.
    """
    def execute(self, session_id, input):
        agent = Agent(
            llm=Gemini.get_llm(model="models/gemini-2.0-flash", temperature=0.5),
            system_message=PERSONALITY,
            tools=[CalculatorTool()],
            memory=BufferMemory(session_id=session_id, interactions=30)
        )
        return agent.execute(input)