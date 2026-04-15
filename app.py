import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Portal de Auditoría - Toyota Salta",
    page_icon="🚗",
    layout="wide"
)

# 2. Función para cargar los datos
# Nota: Para leer un Google Sheet sin autenticación compleja, se usa el formato export?format=csv
def load_data():
    sheet_id = "16kPaOjXPXSzZFzIgVnbBfRjDh6j7SCVO"
    # El GID específico de tu pestaña según el enlace
    gid = "1444184392"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return None

df = load_data()

if df is not None:
    # 3. Título y Filtros
    st.title("📊 Tablero de Control de Calidad - Marzo 2026")
    st.markdown("### Sucursal Salta | Auditoría de Procesos")
    
    with st.sidebar:
        st.header("Filtros de Análisis")
        # Asumiendo que existe una columna 'Asesor' o 'Indicador'
        if 'Asesor' in df.columns:
            asesores = st.multiselect("Seleccionar Asesor", options=df['Asesor'].unique())
        
    # 4. Métricas Principales (KPIs)
    # Aquí calculamos o mostramos los valores según tu estructura de datos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="SSI (Target 93.4%)", value="94.1%", delta="0.7%")
    with col2:
        st.metric(label="CSI (Target 93.8%)", value="92.5%", delta="-1.3%", delta_color="inverse")
    with col3:
        st.metric(label="NPS (Target 83%)", value="85%", delta="2%")
    with col4:
        st.metric(label="Tasa de Respuesta", value="31%", delta="1%")

    st.divider()

    # 5. Visualización de Resultados
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Desempeño por Indicador Crítico")
        # Ejemplo de gráfico de barras si tienes columnas de puntajes
        if 'Indicador' in df.columns and 'Puntaje' in df.columns:
            fig_bar = px.bar(df, x='Indicador', y='Puntaje', color='Indicador',
                             title="Cumplimiento de Estándares")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Carga datos de puntajes para ver el gráfico de barras.")

    with col_right:
        st.subheader("Evolución de Auditoría")
        # Visualización de tendencias
        st.line_chart(df.select_dtypes(include=['number']).iloc[:, :3]) 

    # 6. Tabla de Detalles
    st.subheader("Detalle de Registros de Auditoría")
    st.dataframe(df, use_container_width=True)

    # 7. Botón para exportar reporte
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Auditoría Completa (CSV)",
        data=csv,
        file_name='auditoria_marzo_salta.csv',
        mime='text/csv',
    )
