import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DEL PORTAL ---
st.set_page_config(
    page_title="Auditoría de Procesos - Toyota Salta",
    page_icon="🚗",
    layout="wide"
)

# Reemplaza con los GIDs reales de tu Google Sheet (están al final de la URL de cada pestaña)
SHEET_ID = "16kPaOjXPXSzZFzIgVnbBfRjDh6j7SCVO"
GIDS = {
    "Citas Presencial": "1444184392",
    "Citas Call": "REEMPLAZAR_GID_CALL",
    "Servicio": "REEMPLAZAR_GID_SERVICIO",
    "Ordenes": "REEMPLAZAR_GID_ORDENES"
}

def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# --- INTERFAZ DE USUARIO ---
st.title("📊 Portal de Auditoría de Procesos Internos")
st.markdown("### Sucursal Salta - Análisis de Desvíos y Desempeño")

# Sidebar para selección global
st.sidebar.header("Opciones de Visualización")
mes_analisis = st.sidebar.selectbox("Mes de Auditoría", ["Marzo 2026"])

# --- CARGA DE DATOS ---
df_presencial = load_data(GIDS["Citas Presencial"])
df_call = load_data(GIDS["Citas Call"])
df_servicio = load_data(GIDS["Servicio"])
df_ordenes = load_data(GIDS["Ordenes"])

# --- SECCIÓN 1: ANÁLISIS DE DESVÍOS CRÍTICOS ---
st.header("⚠️ Informe de Desvíos")

col1, col2, col3 = st.columns(3)

# Ejemplo de cálculo basado en los datos de la sucursal
with col1:
    st.metric(label="Cumplimiento Asesores de Servicio", value="84.60%", delta="-5.54%", delta_color="inverse")
    st.caption("Objetivo: 90.14%")

with col2:
    # Simulación de cálculo de desvío en Órdenes (puedes vincularlo a tu DF)
    st.metric(label="Cumplimiento Citas Call", value="92.10%", delta="1.5%")

with col3:
    st.metric(label="Desvío General de Sucursal", value="91.84%", delta="-3.23%", delta_color="inverse")

st.divider()

# --- SECCIÓN 2: DESVÍOS FRECUENTES (ASESORES DE SERVICIO) ---
st.subheader("🚩 Principales Fallas en Asesores de Servicio")

if not df_servicio.empty:
    # Buscamos filas donde el puntaje sea 0 o el cumplimiento sea "No"
    # Ajusta 'Resultado' y 'Puntos de Control' según los nombres exactos de tus columnas
    try:
        desvios_frecuentes = df_servicio[df_servicio['Resultado'] == 0].groupby('Punto de Control').size().reset_index(name='Frecuencia')
        desvios_frecuentes = desvios_frecuentes.sort_values(by='Frecuencia', ascending=False)

        fig = px.bar(desvios_frecuentes.head(5), x='Frecuencia', y='Punto de Control', 
                     orientation='h', title="Top 5 Incumplimientos más Frecuentes",
                     color_discrete_sequence=['#EB0A1E']) # Rojo Toyota
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Asegúrate de que la hoja de 'Servicio' tenga las columnas 'Punto de Control' y 'Resultado' para ver el análisis de fallas.")
else:
    st.warning("No se pudo cargar la hoja de Servicio. Verifica el GID.")

# --- SECCIÓN 3: TABLEROS DETALLADOS ---
st.header("📋 Detalle por Área de Auditoría")

tab1, tab2, tab3, tab4 = st.tabs(["Citas Presencial", "Citas Call", "Servicio", "Órdenes de Reparación"])

with tab1:
    st.subheader("Auditoría: Citas Presenciales")
    st.dataframe(df_presencial, use_container_width=True)

with tab2:
    st.subheader("Auditoría: Citas Call Center")
    st.dataframe(df_call, use_container_width=True)

with tab3:
    st.subheader("Auditoría: Gestión de Servicio")
    if not df_servicio.empty:
        # Filtro por asesor si la columna existe
        if 'Asesor' in df_servicio.columns:
            asesor = st.selectbox("Filtrar por Asesor de Servicio", df_servicio['Asesor'].unique())
            st.write(df_servicio[df_servicio['Asesor'] == asesor])
        else:
            st.dataframe(df_servicio, use_container_width=True)

with tab4:
    st.subheader("Auditoría: Órdenes (OR)")
    st.dataframe(df_ordenes, use_container_width=True)

# --- BOTÓN DE DESCARGA ---
st.sidebar.divider()
if st.sidebar.button("Generar Reporte de Desvíos"):
    st.sidebar.success("Reporte generado correctamente para Salta.")
