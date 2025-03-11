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
        return self.better_response(result)

    def better_response(self, result):
        # Create a prompt to improve the response
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Your task is to improve the following response by making it more coherent, natural, and user-friendly while preserving all essential information. Remove any technical artifacts and maintain a consistent, professional tone. IMPORTANT: You must respond in the same language as the input message."),
            ("human", result)
        ])

        # Use the same LLM instance to process the response
        chain = prompt | self.llm

        # Get the improved response
        improved_response = chain.invoke({})
        print("AI: ", improved_response.content)
        return improved_response.content
        