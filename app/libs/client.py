import os
from openai import OpenAI
from typing import List, Dict


class GeminiClient:
    """
    Client wrapper for communicating with the Gemini API using OpenAI SDK-compatible interface.
    """

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY is not set in the environment variables.")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

    def chat(self, messages: List[Dict[str, str]], model: str = "gemini-2.0-flash") -> str:
        """
        Sends chat messages to the Gemini API and returns the assistant's response.

        Args:
            messages (List[Dict[str, str]]): The list of message dictionaries with roles and content.
            model (str): The Gemini model to use (default: "gemini-2.0-flash").

        Returns:
            str: The assistant's response message.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")
