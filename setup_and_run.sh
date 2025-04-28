#!/bin/bash

# Verificar si python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "pip no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si ya existe un entorno virtual
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
else
    echo "El entorno virtual ya existe."
fi

# Activar el entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar si la activación fue exitosa
if [ "$VIRTUAL_ENV" == "" ]; then
    echo "Error: No se pudo activar el entorno virtual."
    exit 1
fi

# Instalar dependencias
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
else
    echo "No se encontró el archivo requirements.txt. Continuando sin instalar dependencias."
fi

# Ejecutar el script principal
if [ -f "main.py" ]; then
    echo "Ejecutando main.py..."
    python3 main.py
else
    echo "No se encontró el archivo main.py. Verifica su existencia antes de ejecutar este script."
fi

# Salir del entorno virtual
deactivate
echo "El script ha finalizado. El entorno virtual ha sido desactivado."
