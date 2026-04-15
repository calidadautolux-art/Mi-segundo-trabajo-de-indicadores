import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Auditoría Toyota Salta", layout="wide")

OBJETIVO = 0.90  # 90% definido por el usuario
SHEET_ID = "16kPaOjXPXSzZFzIgVnbBfRjDh6j7SCVO"
# Asegúrate de poner los GIDs reales aquí:
GIDS = {
    "Servicio": "REEMPLAZAR_POR_ID_PESTAÑA_SERVICIO",
    "Presencial": "1444184392"
}

def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

# --- CARGA DE DATOS ---
df_serv = load_data(GIDS["Servicio"])

st.title("🚗 Control de Desvíos - Asesores de Servicio")

if not df_serv.empty:
    # 1. Dashboard por Asesor
    st.header("📈 Desempeño Individual por Asesor")
    
    # Asumimos que las columnas se llaman 'Asesor', 'Punto de Control' y 'Resultado' (1 o 0)
    lista_asesores = df_serv['Asesor'].unique()
    
    for asesor in lista_asesores:
        with st.expander(f"Análisis detallado: {asesor}"):
            df_ase = df_serv[df_serv['Asesor'] == asesor]
            cumplimiento = df_ase['Resultado'].mean()
            desvio_val = cumplimiento - OBJETIVO
            
            c1, c2 = st.columns([1, 2])
            
            with c1:
                st.metric("Cumplimiento", f"{cumplimiento*100:.2f}%", 
                          f"{desvio_val*100:.2f}% vs Objetivo", 
                          delta_color="normal" if cumplimiento >= OBJETIVO else "inverse")
                
                # Desvíos más frecuentes del asesor
                st.write("**Fallas más frecuentes:**")
                fallas = df_ase[df_ase['Resultado'] == 0]['Punto de Control'].value_counts()
                if not fallas.empty:
                    st.dataframe(fallas)
                else:
                    st.success("Sin desvíos registrados")

            with c2:
                # Gráfico de cumplimiento por punto de control
                fig = px.bar(df_ase, x='Punto de Control', y='Resultado', 
                             title=f"Checklist - {asesor}",
                             color='Resultado', color_continuous_scale=['red', 'green'])
                fig.add_hline(y=OBJETIVO, line_dash="dash", line_color="white", annotation_text="Objetivo 90%")
                st.plotly_chart(fig, use_container_width=True)

    # 2. Galería de Evidencias (Fotos de Desvíos)
    st.divider()
    st.header("📸 Galería de Evidencias de Desvíos")
    st.info("Las imágenes se cargan desde la carpeta 'fotos_desvios' en el repositorio.")
    
    ruta_fotos = "fotos_desvios"
    
    if os.path.exists(ruta_fotos):
        archivos = [f for f in os.listdir(ruta_fotos) if f.endswith(('.png', '.jpg', '.jpeg'))]
        if archivos:
            cols = st.columns(3) # Galería de 3 columnas
            for i, img_name in enumerate(archivos):
                with cols[i % 3]:
                    st.image(os.path.join(ruta_fotos, img_name), caption=f"Evidencia: {img_name}")
        else:
            st.warning("No hay fotos en la carpeta 'fotos_desvios'.")
    else:
        st.error("No se encontró la carpeta 'fotos_desvios'. Créala en tu repositorio de GitHub.")

else:
    st.error("Error al cargar la hoja de Servicio. Verifica el GID y los permisos del Google Sheet.")
