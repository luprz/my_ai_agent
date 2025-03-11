"""OpenAI model implementation.

This module provides a class for integrating with OpenAI's models
through the LangChain framework.
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


class OpenAIModel:
    """Class for interacting with OpenAI's models.

    This class provides methods to initialize and configure OpenAI models
    for use within the application.
    """
    @staticmethod
    def get_llm(model: str, temperature: float):
        load_dotenv()
        return ChatOpenAI(model=model, temperature=temperature, api_key=os.getenv("OPENAI_API_KEY"))