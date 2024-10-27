import streamlit as st
from data_loader import cargar_datos_cobertura_fibra
from visualization import graficar_porcentaje_localidades_fibra, graficar_cobertura_fibra_optica_proyectada, graficar_mapa_cobertura_fibra, mostrar_tarjetas_cobertura

def display():
    st.title("KPI 2: Cobertura de Fibra Óptica")

    # Cargar los datos de cobertura de fibra óptica
    df_cobertura = cargar_datos_cobertura_fibra()
    geojson_path = 'Streamlit/ProvinciasArgentina_actualizado.geojson'

    # Primer gráfico: porcentaje de localidades con fibra óptica por provincia
    st.subheader("Porcentaje de Localidades con Fibra Óptica por Provincia")
    graficar_porcentaje_localidades_fibra(df_cobertura)

    st.divider()

    # Segundo gráfico: cobertura actual vs. proyectada en provincias con menor cobertura
    st.subheader("Cobertura de Fibra Óptica Actual vs. Proyectada en Provincias con Menor Cobertura")
    graficar_cobertura_fibra_optica_proyectada(df_cobertura)

    st.divider()

    # Mapa de cobertura de fibra óptica por provincia
    graficar_mapa_cobertura_fibra(df_cobertura, geojson_path)

    st.divider()

    # Tarjetas de progreso hacia el objetivo de 10%
    mostrar_tarjetas_cobertura(df_cobertura)
