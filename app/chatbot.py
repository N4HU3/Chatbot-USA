from config.conf import ROLE, SUBJECT_INFO
from app.embeddings_manager import EmbeddingsManager
from app.openai_api import OpenAIApi


class Chatbot:
    def __init__(self, api_key, data_path, embeddings_path):
        """
        Initializes a new instance of the Chatbot class.

        Parameters:
            api_key (str): The API key for accessing the OpenAI API.
            data_path (str): The path to the data file.
            embeddings_path (str): The path to the embeddings file.

        Returns:
            None
        """
        self.openai = OpenAIApi(api_key)
        self.embeddings = EmbeddingsManager(embeddings_path, data_path)
        self.conversation = []
        self.conversation = [ROLE]

    def ask_question(self, question):
        """
        Ask a question to the chatbot and get a response.

        Parameters:
            question (str): The question to ask the chatbot.

        Returns:
            str: The chatbot response. If the last assistant response was the question about transferring to an agent,
            it checks if the response to the question is 'yes' or 'si', in which case it returns a response indicating that
            the agent transfer process has been initiated. If the response is 'no', it returns a response indicating that
            assistance will continue here. If the response is neither 'yes' nor 'no', it returns a response indicating that
            the answer was not understood and prompts the user to respond with 'yes' or 'no' to be transferred to an agent. If
            no relevant information is found in the database, it returns a response indicating that no relevant information was found.
            If the chatbot response contains the word 'agent', it returns a response indicating that the agent transfer process has been initiated.
        """
        self.conversation.append({'role': 'user', 'content': question})
        system_infos = self.embeddings.search(question, n_results=5)
        if not system_infos.empty:
            # Añadir un prompt introductorio y combinar preguntas y respuestas
            system_info = "🔍 Información que podría ser relevante para la consulta del usuario consulta:\n\n" + "\n\n".join(
                f"Pregunta: {pregunta}\nRespuesta: {respuesta}"
                for pregunta, respuesta in zip(system_infos['PREGUNTA'], system_infos['RESPUESTA'])
            )
        else:
            system_info = 'No se encontró información relevante.'

        # Agregar el resultado a la conversación
        self.conversation.append({'role': 'system', 'content': system_info})

        # self.trim_conversation()
        answer = self.openai.generate_response(self.conversation)
        self.conversation.append({'role': 'assistant', 'content': answer})

        return answer
