# 📊 Dashboard de Análisis de Conectividad en Argentina

Este repositorio contiene una aplicación interactiva de **Streamlit** que analiza la conectividad en Argentina, enfocándose en tres KPIs clave relacionados con la penetración de internet, la cobertura de fibra óptica y el uso de planes pospago. La app presenta visualizaciones interactivas y recomendaciones basadas en los hallazgos, proporcionando insights valiosos para la mejora de la conectividad en diferentes regiones.


## 🌐 Estructura de la App

La app se organiza en 5 secciones principales:

1. **📈 Resumen General**: Página inicial con una visión general de los KPIs.
2. **🌍 KPI 1 - Acceso a Internet**: Análisis de la penetración de internet en hogares, con visualizaciones sobre el acceso promedio por provincia.
3. **📶 KPI 2 - Cobertura de Fibra Óptica**: Evaluación de la cobertura de fibra óptica en las provincias, identificando áreas con menor cobertura y proyecciones de mejora.
4. **📱 KPI 3 - Aumento en Planes Pospago**: Análisis del crecimiento en accesos a planes de telefonía móvil pospago y comparativa con los planes prepago.
5. **📌 Conclusiones y Recomendaciones**: Resumen de los hallazgos clave y recomendaciones para mejorar la conectividad en base a los tres KPIs.


## 🚀 Despliegue

La app se encuentra desplegada en **Streamlit Cloud**

- Puedes acceder al Dashboard aquí: [Streamlit Cloud](https://streamlit.io/cloud).


## 🗂️ Estructura del Código

- `main.py`: Archivo principal que carga las distintas páginas de la app.
- `paginas/`: Carpeta que contiene cada página modularizada de la app (`resumen_general.py`, `kpi_1.py`, `kpi_2.py`, `kpi_3.py`, `conclusiones.py`).
- `data_loader.py`: Módulo para cargar datos desde la base de datos.
- `visualization.py`: Módulo para generar las visualizaciones utilizadas en cada KPI.

## 💡 Notas

Este dashboard fue diseñado para proporcionar una interfaz visual amigable para el análisis de datos de conectividad en Argentina. **Cualquier contribución o sugerencia** es bienvenida para mejorar la funcionalidad y alcance del análisis.

<div align="center">
<img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit Logo" width="150">
</div>
