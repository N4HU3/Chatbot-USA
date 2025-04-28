import time
import openai
import openai
from openai.error import RateLimitError
from config.conf import API_KEY


class OpenAIApi:
    def __init__(self, api_key=API_KEY):
        """
        Initializes a new instance of the OpenAIApi class.

        Parameters:
            api_key (str): The API key for accessing the OpenAI API.

        Returns:
            None
        """
        openai.api_key = api_key

    def generate_response(self, conversation):
        """
        Generates a response using the OpenAI ChatCompletion API.

        Args:
            conversation (list): A list of dictionaries representing the conversation history.
                Each dictionary should have the following keys: 'role' (str) and 'content' (str).

        Returns:
            str: The generated response from the ChatCompletion API.

        Raises:
            KeyError: If the response from the API does not contain the expected keys.

        Example:
            conversation = [
                {'role': 'user', 'content': 'Hello'},
                {'role': 'assistant', 'content': 'Hi there!'}
            ]
            response = generate_response(conversation)
            print(response)  # Output: 'Hi there!'
        """
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation,
            temperature=0.1
        )
        return response['choices'][0]['message']['content']

    def generate_response_with_retry(self, conversation, retries=3, delay=2):
        for attempt in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=conversation,
                    temperature=0.1
                )
                return response['choices'][0]['message']['content']
            except RateLimitError as e:
                print(
                    f"[Intento {attempt+1}] Límite de tokens alcanzado. Reintentando en {delay} segundos...")
                time.sleep(delay)
        raise Exception(
            "❌ No se pudo completar la solicitud después de varios intentos.")
