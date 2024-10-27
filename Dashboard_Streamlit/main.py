import streamlit as st
from paginas import resumen_general, kpi_1, kpi_2, kpi_3, conclusiones

# Diccionario de navegación
pages = {
    "Resumen General": resumen_general,
    "KPI 1 - Acceso a Internet": kpi_1,
    "KPI 2 - Cobertura de Fibra Óptica": kpi_2,
    "KPI 3 - Aumento en Planes Pospago": kpi_3,
    "Conclusiones": conclusiones
}

# Barra lateral de navegación
st.sidebar.title("Navegación")
selection = st.sidebar.selectbox("Selecciona una sección:", list(pages.keys()))

# Ejecutar la página seleccionada
page = pages[selection]
page.display()
