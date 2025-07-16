
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='SiniestroBot', layout='wide')

st.title("🤖 SiniestroBot - Analista Virtual de Siniestros")

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel de siniestros", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.success("✅ Archivo cargado correctamente. ¡Hazme una pregunta!")
    st.markdown("📌 **Ejemplos de preguntas que puedes hacer:**")
    st.markdown("""
    - ¿Cuál unidad de negocio tuvo más siniestros?
    - ¿Cuántos siniestros tuvo el operador Juan Pérez?
    - Gráfica de siniestros por tipo de evento
    - ¿Qué placas tienen más siniestros?
    - ¿Cuántos siniestros hubo en junio 2024?
    """)

    question = st.text_input("🧠 Pregunta:")

    if question:
        question_lower = question.lower()

        if "unidad" in question_lower:
            if "gráfica" in question_lower or "grafica" in question_lower:
                st.subheader("📊 Gráfica de siniestros por unidad de negocio")
                st.bar_chart(df["Unidad de negocio"].value_counts())
            else:
                top = df["Unidad de negocio"].value_counts().idxmax()
                st.info(f"La unidad de negocio con más siniestros es: **{top}**")

        elif "operador" in question_lower:
            operadores = df["Operador"].value_counts()
            if "gráfica" in question_lower or "grafica" in question_lower:
                st.subheader("📊 Siniestros por operador")
                st.bar_chart(operadores)
            else:
                top = operadores.idxmax()
                st.info(f"El operador con más siniestros es: **{top}**")

        elif "tipo" in question_lower or "evento" in question_lower:
            tipos = df["Tipo de evento"].value_counts()
            if "gráfica" in question_lower or "grafica" in question_lower:
                st.subheader("📊 Siniestros por tipo de evento")
                st.bar_chart(tipos)
            else:
                top = tipos.idxmax()
                st.info(f"El tipo de evento más común es: **{top}**")

        elif "placa" in question_lower or "unidad" in question_lower:
            placas = df["Unidad"].value_counts()
            if "gráfica" in question_lower or "grafica" in question_lower:
                st.subheader("📊 Siniestros por unidad/placa")
                st.bar_chart(placas)
            else:
                top = placas.idxmax()
                st.info(f"La unidad con más siniestros es: **{top}**")

        elif "mes" in question_lower or "fecha" in question_lower:
            if "Fecha" in df.columns:
                df["Mes"] = pd.to_datetime(df["Fecha"]).dt.to_period("M")
                st.subheader("📊 Siniestros por mes")
                st.bar_chart(df["Mes"].value_counts().sort_index())
            else:
                st.warning("No encontré columna 'Fecha' en tu archivo.")

        else:
            st.warning("No entendí la pregunta. Prueba con otro formato.")

else:
    st.info("⬆️ Sube un archivo para comenzar.")
