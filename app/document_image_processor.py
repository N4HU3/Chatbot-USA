import os
import base64
import tempfile
from io import BytesIO
from app.openai_api import OpenAIApi  # Asegúrate de que esta clase esté implementada

class DocumentImageProcessor:
    """
    Clase que procesa cualquier tipo de archivo convirtiendo cada página en una imagen
    para luego procesarla y obtener una descripción de su contenido mediante la API de OpenAI.
    
    Soportes:
      - PDF: Se convierten sus páginas en imágenes.
      - DOCX: Se convierte a PDF y luego se extraen las imágenes de cada página.
      - Imágenes (JPG, PNG, BMP, etc.): Se procesan como una única "página".
    """

    def __init__(self, file_path):
        """
        Inicializa la clase con la ruta del archivo.
        
        Args:
            file_path (str): Ruta del archivo a procesar.
        """
        self.file_path = file_path
        self.openai_client = OpenAIApi()  # Instancia para llamadas a la API

    def convert_to_images(self):
        """
        Convierte el archivo a una lista de objetos PIL.Image. Dependiendo de la extensión,
        se utiliza el método adecuado.
        
        Returns:
            list: Lista de objetos PIL.Image correspondientes a cada página.
        
        Raises:
            ValueError: Si el formato del archivo no es soportado.
        """
        ext = os.path.splitext(self.file_path)[1].lower()
        images = []
        if ext == '.pdf':
            # Convertir cada página del PDF a una imagen
            images = convert_from_path(self.file_path)
        elif ext == '.docx':
            # Convertir el DOCX a PDF (archivo temporal) y luego extraer las imágenes
            temp_pdf_path = tempfile.mktemp(suffix=".pdf")
            docx_to_pdf_convert(self.file_path, temp_pdf_path)
            images = convert_from_path(temp_pdf_path)
            os.remove(temp_pdf_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            # Si es una imagen, se procesa directamente
            img = Image.open(self.file_path)
            images.append(img)
        else:
            raise ValueError("Formato de archivo no soportado.")
        return images

    def image_to_base64(self, image):
        """
        Convierte una imagen PIL en una cadena base64 en formato PNG.
        
        Args:
            image (PIL.Image): La imagen a convertir.
            
        Returns:
            str: Cadena base64 de la imagen.
        """
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_str

    def process_page_image(self, image, page_number):
        """
        Procesa la imagen de una página: la convierte a data URI, arma el prompt y 
        solicita una descripción a la API de OpenAI.
        
        Args:
            image (PIL.Image): Imagen correspondiente a la página.
            page_number (int): Número de la página.
            
        Returns:
            str: Descripción generada para la página.
        """
        base64_image = self.image_to_base64(image)
        image_data_uri = f"data:image/png;base64,{base64_image}"
        prompt = f"Describe en detalle el contenido de la imagen lo mas fiel posible correspondiente a la página {page_number}."
        conversation = [
            {"role": "system", "content": "Eres un asistente experto en análisis y descripción de imágenes."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_data_uri}}
            ]}
        ]
        response = self.openai_client.generate_response_with_retry(conversation=conversation)
        return f"Página {page_number}: {response}"

    def process_file(self):
        """
        Convierte el archivo a imágenes (una por página) y procesa cada una para obtener su descripción.
        
        Returns:
            str: Descripciones combinadas de todas las páginas.
        """
        print("Procesando el archivo...")
        images = self.convert_to_images()
        descriptions = []
        for i, image in enumerate(images, start=1):
            desc = self.process_page_image(image, i)
            descriptions.append(desc)
        return "\n\n".join(descriptions)


# Ejemplo de uso
# if __name__ == "__main__":
#     # Reemplaza 'ruta_del_archivo' por la ruta real de tu archivo (puede ser PDF, DOCX o una imagen)
#     file_path = "data/Guia APA 7 EDICION.pdf"  # Ejemplo: "documento.pdf" o "archivo.docx" o "imagen.png"

#     # Instanciar el procesador y procesar el archivo
#     processor = DocumentImageProcessor(file_path)
#     result = processor.process_file()

#     # Mostrar en consola
#     print("Descripción del documento procesado:")
#     print(result)

#     # Guardar en un archivo de texto
#     output_path = "resultado.txt"
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(result)

#     print(f"\n✅ Resultado guardado en '{output_path}'")

