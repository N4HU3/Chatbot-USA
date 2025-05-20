import os
import pandas as pd
from config.conf import EMBEDDING_ENGINE, API_KEY
from openai.embeddings_utils import get_embedding
import openai


def generate_embeddings(path_data: str, path_embedding: str):
    """
    Genera un archivo de embeddings a partir de preguntas en un archivo CSV.

    Parameters:
        path_data (str): Ruta al archivo CSV que contiene la columna 'PREGUNTA'.
        path_embedding (str): Ruta donde se guardará el archivo CSV con los embeddings.
    """
    openai.api_key = API_KEY

    # Verificar existencia del archivo de datos
    if not os.path.exists(path_data):
        raise FileNotFoundError(f"El archivo de datos no existe: {path_data}")

    print("Leyendo datos desde:", path_data)
    df = pd.read_csv(path_data)

    # Verificar columna 'PREGUNTA'
    if 'PREGUNTA' not in df.columns:
        raise ValueError("El archivo de datos debe contener una columna llamada 'PREGUNTA'")

    # Eliminar filas con valores faltantes en 'PREGUNTA'
    df = df[df['PREGUNTA'].notna()].copy()

    # Convertir a cadena y reemplazar saltos de línea
    df['PREGUNTA'] = df['PREGUNTA'].astype(str).str.replace('\n', ' ')

    print("Generando embeddings...")
    # Generar embeddings para cada pregunta limpia
    df['Embedding'] = df['PREGUNTA'].apply(
        lambda x: get_embedding(x, engine=EMBEDDING_ENGINE)
    )

    # Asegurar carpeta de salida
    os.makedirs(os.path.dirname(path_embedding), exist_ok=True)
    df.to_csv(path_embedding, index=False)
    print(f"Embeddings guardados en: {path_embedding}")


if __name__ == "__main__":
    PATH_DATA = "data/data.csv"
    PATH_EMBEDDING = "data/embeddings.csv"
    generate_embeddings(PATH_DATA, PATH_EMBEDDING)
