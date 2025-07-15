
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SiniestroBot", layout="wide")

st.title("🤖 SiniestroBot - Análisis Inteligente de Siniestros")

uploaded_file = st.file_uploader("📁 Sube tu archivo Excel de siniestros", type=["xlsx", "xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Archivo cargado exitosamente.")

    if st.checkbox("👀 Mostrar datos"):
        st.dataframe(df)

    query = st.text_input("¿Qué deseas saber del archivo?", "")

    if query:
        if "unidades de negocio" in query.lower():
            unidades = df["Unidad de Negocio"].dropna().unique()
            st.write(f"Hay {len(unidades)} unidades de negocio:")
            for unidad in unidades:
                st.markdown(f"- **{unidad}**")

        elif "gráfica" in query.lower() or "grafica" in query.lower():
            col = st.selectbox("Selecciona la columna para graficar", df.columns)
            fig, ax = plt.subplots()
            df[col].value_counts().plot(kind="bar", ax=ax)
            ax.set_title(f"Distribución de {col}")
            st.pyplot(fig)

        else:
            st.warning("Por ahora solo puedo responder preguntas sobre unidades de negocio o generar gráficas.")
else:
    st.info("Por favor sube un archivo para comenzar.")
