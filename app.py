import streamlit as st
import os
from google import genai
from google.genai import types

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Estimador de Construcción CR",
    page_icon="🏗️",
    layout="wide"
)

# Título y descripción
st.title("🏗️ Calculadora Inteligente de Construcción - Costa Rica")
st.markdown(
    "Calcula los materiales, costos de construcción estimados y obtén recomendaciones "
    "técnicas adaptadas al contexto y normativas costarricenses usando IA generativa."
)

# Configuración de la API Key de Gemini
try:
    gemini_key = st.secrets["API_KEY"]
except (KeyError, st.errors.StreamlitSecretNotFoundError):
    gemini_key = None

gemini_key = gemini_key or os.getenv("GEMINI_API_KEY")

# Sidebar para configurar la clave si no está en las variables de entorno
with st.sidebar:
    st.header("Configuración")
    if not gemini_key:
        gemini_key = st.text_input("Ingresa tu Gemini API Key:", type="password")
    else:
        st.success("🔑 API Key detectada en los secretos o el entorno.")
    
    st.markdown("---")
    st.markdown("### Sobre el Asistente")
    st.info(
        "Este asistente actúa como un Ingeniero Civil especializado en el mercado de Costa Rica "
        "y calcula estimaciones basadas en normativas como el Código Sísmico de CR."
    )

# Verificar cliente
if not gemini_key:
    st.warning("⚠️ Por favor, introduce tu Gemini API Key en la barra lateral para comenzar.")
else:
    # Inicializar el cliente oficial de Google GenAI
    client = genai.Client(api_key=gemini_key)

    # System Instruction para el modelo
    system_instruction = (
        "Eres un ingeniero civil y experto en estimación de costos de construcción en Costa Rica. "
        "Tu tarea es analizar los requerimientos de vivienda provistos por el usuario y calcular "
        "los materiales requeridos y los costos estimados asociados en colones costarricenses (CRC) y dólares (USD). "
        "Devuelve siempre la información estructurada en formato Markdown limpio con las siguientes secciones:\n"
        "1. Resumen del Proyecto\n"
        "2. Lista Detallada de Materiales (con cantidades estimadas)\n"
        "3. Costo Promedio Estimado (aclarando explícitamente que es una estimación aproximada basada en valores de mercado en Costa Rica)\n"
        "4. Recomendaciones técnicas locales (considerando clima, sismicidad y normativas de Costa Rica como el Código Sísmico)."
    )

    # Inicializar historial del chat en Streamlit si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos de la sesión
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("Ej: Quiero una casa de 2 pisos, 3 habitaciones, 120m², acabados modernos..."):
        # Mostrar el mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generar respuesta de la IA
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("👷‍♂️ Analizando requerimientos y calculando costos...")
            
            try:
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3
                    )
                )
                
                respuesta_texto = response.text
                response_placeholder.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                
            except Exception as e:
                st.error(f"Ocurrió un error al conectar con Gemini: {str(e)}")
