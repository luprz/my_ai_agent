"""Gemini 2.0 Flash model implementation.

This module provides a class for integrating with Google's Gemini 2.0 Flash model
through the LangChain framework.
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


class Gemini:
    """Class for interacting with OpenAI's models.

    This class provides methods to initialize and configure OpenAI models
    for use within the application.
    """
    @staticmethod
    def get_llm(model: str, temperature: float):
        load_dotenv()
        return ChatGoogleGenerativeAI(temperature=temperature, model=model)