from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from pydantic import BaseModel

class IMemory(BaseModel):
    def get_chat_history(self):
        return
    def add_message(self, human: str, ai: str):
        return

class Agent:
    def __init__(self, llm, system_message, tools, memory: IMemory) -> None:
        self.tools = tools
        self.system_message = system_message
        self.llm = llm
        self.memory = memory

    def execute(self, input):
        chat_history = self.memory.get_chat_history()
        # Prompt moderno usando formato de chat
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", input),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Crear el agente con formato moderno de herramientas
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)

        # Configurar el ejecutor del agente
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

        # Execute the agent and return the result
        result = agent_executor.invoke({"input": input, "chat_history": chat_history})["output"]
        # Update chat history with the new interaction
        return result