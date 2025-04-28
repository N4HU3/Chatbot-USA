from app.chatbot import Chatbot


class ChatbotSession:
    def __init__(self):
        """
        Initializes a new instance of the ChatbotSession class.

        This method creates an empty dictionary called `active_chatbots` to store the active chatbots.

        Parameters:
            None

        Returns:
            None
        """
        self.active_chatbots = {}

    def create_session(self, guid, api_key, data_file, embeddings_file, initial_message):
        """
        Initializes a new chatbot session with the provided parameters.

        Parameters:
            guid (str): The unique identifier for the chatbot session.
            api_key (str): The API key for the chatbot.
            data_file (str): The path to the data file for the chatbot.
            embeddings_file (str): The path to the embeddings file for the chatbot.
            initial_message (str): The initial message to start the conversation.

        Returns:
            None
        """
        self.active_chatbots[guid] = Chatbot(
            api_key, data_file, embeddings_file)
        self.active_chatbots[guid].conversation.append(
            {'role': 'system', 'content': initial_message})

    def get_chatbot(self, guid):
        """
        Get the chatbot instance associated with the given GUID.

        Parameters:
            guid (str): The unique identifier for the chatbot session.

        Returns:
            Chatbot or None: The chatbot instance associated with the GUID, or None if no chatbot is found.
        """
        return self.active_chatbots.get(guid)

    def remove_session(self, guid):
        """
        Removes a chatbot session based on the provided unique identifier.

        Parameters:
            guid (str): The unique identifier for the chatbot session to be removed.

        Returns:
            None
        """
        if guid in self.active_chatbots:
            del self.active_chatbots[guid]
