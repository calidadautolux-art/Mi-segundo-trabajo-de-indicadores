import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Auditoría Interna - Autolux Salta", layout="wide")

# Configuración de GIDs (IDs de cada pestaña del Excel)
SHEET_ID = "16kPaOjXPXSzZFzIgVnbBfRjDh6j7SCVO"
GIDS = {
    "Resumen": "1103329952",
    "Citas Presencial": "1444184392",
    "Citas Call": "123456789", # Reemplazar con el GID real de esa pestaña
    "Servicio": "987654321",    # Reemplazar con el GID real de esa pestaña
    "Ordenes": "456789123"      # Reemplazar con el GID real de esa pestaña
}

def load_sheet(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# --- PROCESAMIENTO DE DATOS ---
df_servicio = load_sheet(GIDS["Servicio"])

st.title("🚗 Control de Procesos Internos - Salta")

# 1. Resumen de Desvíos (Comparativa vs Target)
st.subheader("⚠️ Análisis de Desvíos - Marzo 2026")
col1, col2, col3 = st.columns(3)

# Cálculo de desvío (Ejemplo basado en tu imagen: Octubre vs Marzo)
desvio_gral = 91.84 - 95.07 
col1.metric("Resultado Auditoría Gral", "91.84%", f"{desvio_gral:.2f}%", delta_color="inverse")
col2.metric("Desvío en Asesores Servicio", "84.60%", "-5.54%", delta_color="inverse")
col3.metric("Punto Crítico", "Gestión de OR", "Bajo Target")

st.divider()

# 2. Desvíos Frecuentes en Asesores de Servicio
st.subheader("🚩 Fallas Críticas en Asesores de Servicio")
# Aquí filtramos los ítems donde el cumplimiento es 'No' o 0
if 'Cumplimiento' in df_servicio.columns:
    fallas = df_servicio[df_servicio['Cumplimiento'] == 'No'].groupby('Item_Auditoria').size().reset_index(name='Frecuencia')
    fallas = fallas.sort_values(by='Frecuencia', ascending=False)
    
    fig_fallas = px.bar(fallas, x='Frecuencia', y='Item_Auditoria', orientation='h', 
                        title="Top Desvíos Detectados", color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig_fallas, use_container_width=True)
else:
    st.warning("Para ver desvíos frecuentes, asegúrate de que la hoja 'Servicio' tenga columnas de 'Item_Auditoria' y 'Cumplimiento'.")

# 3. Visualización por Hoja (Tableros Específicos)
tab1, tab2, tab3, tab4 = st.tabs(["📞 Citas Call", "🤝 Citas Presencial", "🔧 Servicio", "📝 Órdenes"])

with tab1:
    st.dataframe(load_sheet(GIDS["Citas Call"]))
with tab2:
    st.dataframe(load_sheet(GIDS["Citas Presencial"]))
with tab3:
    st.write("Detalle de Auditoría de Servicio")
    st.dataframe(df_servicio)
with tab4:
    st.dataframe(load_sheet(GIDS["Ordenes"]))
