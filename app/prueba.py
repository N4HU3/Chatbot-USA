from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Página 1: Portada con error intencional en el nombre de la universidad.
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 100, "Guía para Correctores")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 130, "Dirección de Publicaciones")
    c.setFont("Helvetica", 12)
    # Error intencional: "Univesidad" en lugar de "Universidad"
    c.drawCentredString(width / 2, height - 160, "Univesidad Sergio Arboleda")
    c.showPage()

    # Página 2: Sección de instrucciones con error intencional en la ortografía.
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Sección I: Instrucciones")
    c.setFont("Helvetica", 12)
    text = c.beginText(50, height - 80)
    content = (
        "Por favor, revise cuidadosamente el siguiente documento. \n"
        "Este documento contiene lineas que deben ser corregidas.\n"  # Error: "lineas" en lugar de "líneas"
        "Ejemplo de error: La ortografía y la gramática deben ser revisadas.\n"
        "Nota: Observe que 'lineas' debería llevar tilde: 'líneas'."
    )
    text.textLines(content)
    c.drawText(text)
    c.showPage()

    # Página 3: Sección de revisión de contenido con errores intencionales.
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Sección II: Revisión de Contenido")
    c.setFont("Helvetica", 12)
    text = c.beginText(50, height - 80)
    content = (
        "El contenido del documento debe cumplir con los estandares de redacción.\n"  # Error: "estandares" en lugar de "estándares"
        "Verifique que todas las referencias esten correctas y que el formato APA se haya aplicado correctamente.\n"  # Error: "esten" en lugar de "estén"
        "Ejemplo de error: 'estandares' debería ser 'estándares' y 'esten' debería ser 'estén'."
    )
    text.textLines(content)
    c.drawText(text)
    c.showPage()

    # Finaliza y guarda el PDF.
    c.save()

if __name__ == "__main__":
    # Se genera el archivo PDF de prueba.
    create_pdf("documento_prueba.pdf")
    print("El documento 'documento_prueba.pdf' se ha generado correctamente.")
