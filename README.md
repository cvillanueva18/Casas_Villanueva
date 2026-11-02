# Calculadora de Materiales y Costos de Construcción (Costa Rica)

Esta es una aplicación interactiva desarrollada en Streamlit que utiliza la API de Gemini (con el SDK oficial `google-genai`) para estimar los materiales de construcción, costos aproximados y dar recomendaciones técnicas para viviendas en Costa Rica.

## Estructura del Proyecto
- `app.py`: Archivo principal de la aplicación de Streamlit.
- `requirements.txt`: Lista de dependencias del proyecto.
- `AGENTS.md`: Detalles de la configuración y rol de nuestro agente experto.

## Cómo ejecutar localmente
1. Clona o descarga estos archivos en tu máquina local.
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tu API Key de Gemini en tus variables de entorno:
   - En Windows:
     ```cmd
     set GEMINI_API_KEY=tu_api_key_aqui
     ```
   - En macOS/Linux:
     ```bash
     export GEMINI_API_KEY=tu_api_key_aqui
     ```
4. Corre la aplicación de Streamlit:
   ```bash
   streamlit run app.py
   ```
