import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de la página
st.set_page_config(page_title="📊Hackathon BI Dashboard", layout="wide")

st.title(" 🤖 Management - Analytics Dashboard")
st.markdown("Este dashboard visualiza los KPIs clave extraídos del pipeline de datos (PostgreSQL -> DuckDB -> Parquet).")

# Ruta de los archivos analíticos
OUTPUT_PATH = 'analytics/output/distribucion_participantes.parquet'

def load_data():
    if os.path.exists(OUTPUT_PATH):
        return pd.read_parquet(OUTPUT_PATH)
    else:
        return None

data = load_data()

if data is not None:
    # --- SECCIÓN DE MÉTRICAS GLOBALES ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_teams = len(data)
        st.metric("Total de Equipos", total_teams)
        
    with col2:
        total_participants = data['total_participantes'].sum()
        st.metric("Total Participantes", total_participants)
        
    with col3:
        avg_members = round(data['total_participantes'].mean(), 2)
        st.metric("Promedio Miembros/Equipo", avg_members)

    st.divider()

    # --- VISUALIZACIONES ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Distribución de Participantes por Equipo")
        fig_bar = px.bar(
            data, 
            x='equipo', 
            y='total_participantes',
            labels={'total_participantes': 'Participantes', 'equipo': 'Nombre del Equipo'},
            color='total_participantes',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("Concentración de Miembros (Treemap)")
        fig_tree = px.treemap(
            data, 
            path=['equipo'], 
            values='total_participantes',
            color='total_participantes'
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    # --- TABLA DE DATOS CRUDA ---
    with st.expander("Ver datos detallados"):
        st.dataframe(data, use_container_width=True)

else:
    st.error(" No se encontró el archivo Parquet. Asegúrate de ejecutar primero el script de análisis.")
    st.info("Ruta buscada: `analytics/output/distribucion_participantes.parquet`")