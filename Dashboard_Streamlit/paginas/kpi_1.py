import streamlit as st
from data_loader import load_internet_penetration_data, cargar_datos_penetracion_mapa
from visualization import graficar_penetracion_internet, graficar_comparativa_acceso_proyectado, graficar_evolucion_penetracion_provincia, graficar_mapa_penetracion

def display():
    st.title("KPI 1 - Acceso a Internet")

    # Cargar los datos de penetración general y mapa
    df_penetracion = load_internet_penetration_data()
    df_penetracion_mapa = cargar_datos_penetracion_mapa()
    geojson_path = 'assets/argentina_nivel_1_normalizado.geojson'

    # Mostrar gráficos iniciales
    st.subheader("Penetración de Internet por 100 Hogares (2023 en adelante)")
    graficar_penetracion_internet(df_penetracion)

    st.subheader("Comparativa de Acceso a Internet: Actual vs. Proyectado (2% Aumento)")
    graficar_comparativa_acceso_proyectado(df_penetracion)

    # Subtítulo de la sección de evolución y filtro de selección
    st.subheader("Evolución de la Penetración por Provincia")

    # Sidebar para seleccionar la provincia
    provincia_seleccionada = st.selectbox(
        'Selecciona una provincia:', 
        sorted(df_penetracion[df_penetracion['anio'] >= 2023]['nombre_provincia'].unique())
    )

    # Gráfico de evolución de penetración de internet por provincia
    graficar_evolucion_penetracion_provincia(df_penetracion, provincia_seleccionada)

    # Mapa de penetración por provincia
    graficar_mapa_penetracion(df_penetracion_mapa, geojson_path)