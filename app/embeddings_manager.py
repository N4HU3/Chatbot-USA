import os
import pandas as pd
from config.conf import EMBEDDING_ENGINE
from openai.embeddings_utils import get_embedding, cosine_similarity


class EmbeddingsManager:
    def __init__(self, path_embedding, path_data):
        """
        Initializes the EmbeddingsManager with the provided paths for embedding data and raw data.

        Parameters:
            path_embedding (str): The path to the embedding data file.
            path_data (str): The path to the raw data file.

        Returns:
            None
        """
        if os.path.exists(path_embedding):
            self.df = pd.read_csv(path_embedding)
        else:
            print("Generando Embedding")
            embedding = pd.read_csv(path_data)
            embedding['Embedding'] = embedding['PREGUNTA'].apply(
                lambda x: get_embedding(x, engine=EMBEDDING_ENGINE))
            embedding.to_csv('data/embeddings.csv')
            self.df = embedding
            print("Embedding generado correctamente")

    def search(self, query, n_results=2, similarity_threshold=0.5):
        """
        Searches for the most similar responses to a given query in the embedded data.

        Args:
            query (str): The query to search for.
            n_results (int, optional): The number of results to return. Defaults to 3.
            similarity_threshold (float, optional): The similarity threshold. Defaults to 0.8.

        Returns:
            pandas.DataFrame: A DataFrame containing the most similar responses, their similarity scores, and their embeddings.
                Columns:
                    - PREGUNTA (str): The original question.
                    - RESPUESTA (str): The response.
                    - Similitud (float): The similarity score.
                    - Embedding (list): The embedding of the response.
        """
        query_embed = get_embedding(query, engine=EMBEDDING_ENGINE)
        # Convert the 'Embedding' column from string to list
        self.df['Embedding'] = self.df['Embedding'].apply(
            lambda x: eval(x) if isinstance(x, str) else x)
        self.df["Similitud"] = self.df['Embedding'].apply(
            lambda x: cosine_similarity(x, query_embed))

        self.df = self.df.sort_values("Similitud", ascending=False)
        filtered_data = self.df[self.df["Similitud"] > similarity_threshold]
        return filtered_data.iloc[:n_results][["PREGUNTA", "RESPUESTA", "Similitud", "Embedding"]]
