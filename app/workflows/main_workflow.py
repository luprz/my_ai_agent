from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from app.agents.main_assistant.agent import MainAgent

class WorkflowState(TypedDict):
    session_id: str
    messages: Annotated[Sequence[HumanMessage | AIMessage], "The chat history"]

def main_assistant(
    state: WorkflowState,
) -> WorkflowState:
    messages = state["messages"]
    session_id = state["session_id"]
    agent = MainAgent()
    last_message = messages[-1]
    response = agent.execute(session_id=session_id, input=last_message.content)
    final_response = AIMessage(content=response)
    return {"messages": messages + [final_response]}

class MainWorkflow:
    def __init__(self):
        self.graph = StateGraph(WorkflowState)
        self.graph.add_node("ask_to_main_assistant", main_assistant)

        self.graph.set_entry_point("ask_to_main_assistant")
        self.graph.add_edge("ask_to_main_assistant", END)
        self.workflow = self.graph.compile()

    def run(self, session_id: str, input: str):
        messages = [HumanMessage(content=input)]
        result = self.workflow.invoke({"messages": messages, "session_id": session_id, "input": input})
        return result["messages"][-1].content