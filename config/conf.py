import os
from dotenv import load_dotenv

load_dotenv(override=True)  # carga el .env en las variables de entorno

API_KEY = os.getenv("API_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

EMBEDDING_ENGINE = 'text-embedding-3-small'

ROLE = {
    'role': 'system',
    'content': '''Eres el asistente virtual de la Escuela de Ciencias Exactas e Ingeniería de la Universidad Sergio Arboleda.
    
    Directrices para tus respuestas:
    1. Responde ÚNICAMENTE usando la información proporcionada por el sistema de la Escuela.
    2. Ignora preguntas fuera del contexto académico de la Escuela.
    3. Usa el siguiente formato para tus respuestas:
        - Para títulos principales: TÍTULO EN MAYÚSCULAS
        - Para subtítulos: Subtítulo con Primera Letra en Mayúscula
        - Para listas numeradas: 1. 2. 3.
        - Para listas sin orden: • (viñetas)
        - Para énfasis: usar **palabra**
        - Usar emojis relevantes al inicio de cada sección
    
    4. Estructura de respuesta:
        - Siempre usar saltos de línea entre secciones
        - Mantener respuestas concisas y organizadas
        - Resaltar palabras clave con **negrita**
        
    5. Para saludos iniciales:
        - Dar bienvenida cálida y entusiasta
        - No ofrecer información no solicitada
        
    6. Formato prohibido:
        - No usar #, ##, o ### para títulos
        - No usar markdown excepto para **negrita**
        - No usar formato HTML
    
    Ejemplo de formato:
    🎓 PROGRAMA ACADÉMICO
    
    • **Nombre del programa**: Ingeniería
    • **Duración**: 10 semestres
    
    📚 MATERIAS PRINCIPALES
    1. **Cálculo I**
    2. **Física I**'''
}

SUBJECT_INFO = {
    'role': 'system',
    'content': '''Información sobre las materias de la Escuela de Ciencias Exactas e Ingeniería de la Universidad Sergio Arboleda en caso que te pregunten por ellas:
Electrónica 			Matemáticas 			CCIA			Ingeniería Ambiental 	
Asignatura	Prerrequisito		Asignatura	Prerrequisito		Asignatura	Prerrequisito		Asignatura	Prerrequisito
Programación para IE	Pensamiento Computacional		Cálculo diferencial	Introducción al Cálculo		Fundamentos de Diseño de Software	Pensamiento Algorítmico		Cálculo Integral	Cálculo Diferencial
Análisis de Circuitos	Introducción a la IE y Laboratorio		Álgebra Lineal I	Fundamentos de Matemáticas		Ciberética y Sistemas Inteligentes	Introducción a IA-CC		Física Mecánica y Laboratorio	Cálculo Diferencial
Física Electromagnética y Laboratorio	Física Mecánica y Laboratorio		Matemáticas discretas	Fundamentos de Matemáticas		Estructura de Datos Lineales	Ciencia Computacional Básica		Modelación Matemática para Ingeniería	Cálculo Integral
Cálculo Integral	Cálculo Diferencial		Cálculo Integral y Series	Cálculo diferencial		Paradigmas de Programación	Pensamiento Algorítmico		Termodinámica y Laboratorio	Física Mecánica y Laboratorio
Diseño Electrónico Básico	Análisis de Circuitos		Teoría de Números	Álgebra Lineal I		Arquitectura de Computadores	Tecnología Inteligente y Sociedad Contemporánea		Bioquímica Ambiental	Química y Laboratorio
Electrónica de Semiconductores	Física Electromagnética y Laboratorio		Álgebra Lineal II	Álgebra Lineal I		Estructura de Datos No Lineales	Estructura de Datos Lineales		Química y Calidad Ambiental y Laboratorio	Química y Laboratorio
Fluidos y Termodinámica	Física Electromagnética y Laboratorio		Cálculo Vectorial	Cálculo Integral y Series		Análisis de Algoritmos	Paradigmas de Programación		Cartografía y Aplicaciones Geoespaciales	Ecología, Ecosistemas y Biodiversidad
Electrónica Digital	Programación para IE		Probabilidad	Matemáticas discretas		Redes de Computación	Arquitectura de Computadores		Fluidos e Hidráulica	Modelación Matemática para Ingeniería
Cálculo Vectorial y Multivariable	Cálculo Integral		Ecuaciones Diferenciales Ordinarias	Cálculo Integral y Series		Bases de Datos	Estructura de Datos No Lineales		Métodos Numéricos y Herramientas Computacionales	Modelación Matemática para Ingeniería
Variable Compleja	Cálculo Vectorial y Multivariable		Análisis Matemático	Cálculo Vectorial		Lenguajes de Programación y Transducción	Paradigmas de Programación		Balance de Materia y Energía	Química y Calidad Ambiental y Laboratorio
Electrónica Aplicada	Electrónica de Semiconductores		Estadística	Probabilidad		Sistemas Operativos	Arquitectura de Computadores		Ciencias de la Tierra y el Suelo	Cartografía y Aplicaciones Geoespaciales
Ondas y Campos EM	Física Electromagnética y Laboratorio		Álgebra Abstracta	Álgebra Lineal II		Ingeniería de Software	Fundamentos de Diseño de Software		Ordenamiento Territorial en Colombia	Ciencias de la Tierra y el Suelo
Arquitectura de Computadores	Electrónica Digital		Variable Compleja	Análisis Matemático		Patrones de Diseño de Software	Ingeniería de Software		Análisis Ambiental de Procesos Unitarios	Balance de Materia y Energía
Ecuaciones Diferenciales	Cálculo Integral		Topología	Álgebra Abstracta		Computación Paralela y Distribuida	Sistemas Operativos		Manejo y Remediación de Suelos	Ciencias de la Tierra y el Suelo
Diseño Electrónico Intermedio	Diseño Electrónico Básico		Computación científica II	Computación científica I		Inteligencia Artificial	Ciencia Computacional Avanzada		Gestión Integral de Residuos Sólidos, Tóxicos y Peligrosos	Balance de Materia y Energía
Teoría de Sistemas Lineales	Electrónica Aplicada		Computación científica III	Computación científica II		Big Data e Ingeniería de Datos	Ciencia Computacional Avanzada		Control y Simulación Atmosférica	Clima Change: the science and global impact
Sensores e Instrumentación	Ondas y Campos EM		Modelación de fenómenos naturales I	Computación científica II		Seguridad de la Información	Redes de Computación		Hydrodynamic Modeling	Fluidos e Hidráulica
Sistemas Embebidos	Arquitectura de Computadores		Modelación de fenómenos naturales II	Modelación de fenómenos naturales I		Arquitectura de Software	Ingeniería de Software		Evaluación, Planes de Manejo y Monitoreo Ambiental	Gestión Integral de Residuos Sólidos, Tóxicos y Peligrosos
Inteligencia Artificial	Electrónica Digital		Modelación de fenómenos naturales III	Modelación de fenómenos naturales II		Aprendizaje de Máquina	Inteligencia Artificial		Formulación y Evaluación de Proyectos Socioambientales	Ordenamiento Territorial en Colombia
Seminario de I+D+I	Teoría de Sistemas Lineales					Diseño Creativo	Aprendizaje de Máquina		Sistemas de Gestión y Política Ambiental	Evaluación, Planes de Manejo y Monitoreo Ambiental
Opción de grado	Seminario de I+D+I					Opción de Grado	Seminario I+D+I		Opción de Grado	Seminario I+D+I'''
}