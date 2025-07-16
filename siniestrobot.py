
import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import os

# Configura tu clave de API de OpenAI aquí o usa secrets en deployment
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="SiniestroBot - Analista Virtual de Siniestros", layout="centered")

st.title("🤖 SiniestroBot - Analista Virtual de Siniestros")
st.markdown("Sube tu archivo Excel de siniestros y haz preguntas en lenguaje natural.")

uploaded_file = st.file_uploader("📤 Drag and drop file here", type=["xlsx"], help="Limit 200MB per file • XLSX")

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("✅ Archivo cargado correctamente. ¡Hazme una pregunta!")

        st.markdown("### 📌 Ejemplos de preguntas que puedes hacer:")
        st.markdown("""
        - ¿Cuál unidad de negocio tuvo más siniestros?
        - ¿Cuántos siniestros tuvo el operador Juan Pérez?
        - Gráfica de siniestros por tipo de evento
        - ¿Qué placas tienen más siniestros?
        - ¿Cuántos siniestros hubo en junio 2024?
        - Promedio de siniestros por mes
        - ¿Hay más siniestros en lunes o viernes?
        """)

        user_question = st.text_input("✍️ Pregunta:")

        if user_question:
            with st.spinner("Pensando..."):
                sample_data = df.head(15).to_dict(orient="records")
                prompt = f"""
Eres un analista experto. Tienes los siguientes datos de siniestros en formato tabla. 
Responde la siguiente pregunta de forma concreta. Si aplica, proporciona una gráfica.
Usa lenguaje claro como si explicaras a un director.

Pregunta: {user_question}

Ejemplo de los datos:
{sample_data}
"""
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4
                )

                answer = response.choices[0].message["content"]
                st.markdown("### 📊 Respuesta:")
                st.markdown(answer)

                if "gráfica" in user_question.lower() or "grafica" in user_question.lower():
                    st.markdown("### 📈 Visualización tentativa:")
                    col_to_plot = df.select_dtypes(include="object").columns[0]
                    fig = px.histogram(df, x=col_to_plot)
                    st.plotly_chart(fig)

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
