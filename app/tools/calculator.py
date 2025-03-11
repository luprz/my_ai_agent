from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import math

class CalculatorInput(BaseModel):
    """Input for the Calculator tool."""
    operacion: str = Field(..., description="The mathematical operation in Python expression format")

class CalculatorTool(BaseTool):
    """Tool for executing simple mathematical operations."""
    name: str = "calculator"
    description: str = """Executes a simple mathematical operation.
    The operation should be in Python expression format.
    Examples: "2+2", "math.sqrt(16)", "math.pi * 5**2"""
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, operacion: str) -> str:
        try:
            resultado = eval(operacion, {"__builtins__": {}}, {"math": math})
            return f"Resultado: {resultado}"
        except Exception as e:
            return f"Error al calcular: {str(e)}"
    
    async def _arun(self, operacion: str) -> str:
        return self._run(operacion)