import streamlit as st
from data_loader import cargar_datos_accesos_movil
from visualization import graficar_evolucion_accesos_pospago, graficar_proyeccion_accesos_pospago, graficar_distribucion_accesos, mostrar_tarjetas_accesos_pospago

def display():
    st.title("KPI 3: Aumento en Planes Pospago")

    # Cargar los datos de accesos a telefonía móvil
    df_telefonia = cargar_datos_accesos_movil()

    # Gráfico 1: Evolución de accesos pospago desde 2023 en adelante
    st.subheader("Evolución Trimestral del Acceso a Líneas Pospago (2023 en adelante)")
    graficar_evolucion_accesos_pospago(df_telefonia)

    st.divider()

    # Gráfico 2: Proyección del aumento del 5% en accesos de planes pospago
    st.subheader("Proyección de Aumento del 5% en Accesos de Planes Pospago (2024 T3)")
    graficar_proyeccion_accesos_pospago()

    st.divider()

    # Gráfico 3: Distribución de accesos pospago y prepago (2024 T1 y T2)
    st.subheader("Distribución de Accesos Pospago y Prepago (2024 T1 y T2)")
    graficar_distribucion_accesos(df_telefonia)

    st.divider()

    # Tarjetas de progreso hacia el 5% de aumento en accesos pospago
    st.subheader("Progreso hacia el 5% de Aumento en los Accesos a Líneas Pospago")
    mostrar_tarjetas_accesos_pospago(df_telefonia)
