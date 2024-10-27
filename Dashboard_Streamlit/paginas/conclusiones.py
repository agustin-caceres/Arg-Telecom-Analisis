import streamlit as st
import plotly.graph_objects as go

def display():
    st.title("Conclusiones y Recomendaciones para los KPIs")

    # Divider para separar secciones
    st.markdown('---')

    # Resumen de conclusiones clave
    st.subheader('📊 Conclusiones')

    # Conclusión 1: Crecimiento Estable
    st.markdown("**Crecimiento Estable en Accesos por 100 Hogares**")
    fig_crecimiento = go.Figure(go.Indicator(
        mode="gauge+number",
        value=70.44,  # Promedio alcanzado
        title={'text': "Promedio de Accesos por 100 Hogares"},
        gauge={'axis': {'range': [0, 120]}, 'bar': {'color': "blue"}}
    ))
    st.plotly_chart(fig_crecimiento)

    # Conclusión 2: Cobertura de Fibra Óptica
    st.markdown("**Cobertura de Fibra Óptica en el País**")
    fig_fibra = go.Figure(go.Indicator(
        mode="gauge+number",
        value=58.32,  # Porcentaje de cobertura de fibra óptica
        title={'text': "Cobertura de Fibra Óptica (%)"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "orange"}}
    ))
    st.plotly_chart(fig_fibra)

    # Conclusión 3: Comparativa Pospago vs Prepago
    st.markdown("")
    fig_barras_accesos = go.Figure()

    # Añadir barras para pospago y prepago
    fig_barras_accesos.add_trace(go.Bar(
        x=['Pospago', 'Prepago'],
        y=[7889718, 53901450],
        marker_color=['#1E90FF', '#87CEEB']
    ))

    # Configuración del gráfico
    fig_barras_accesos.update_layout(
        title='Distribución promedio de Accesos Pospago y Prepago (2023-2024)',
        xaxis_title='Tipo de Plan',
        yaxis_title='Número Promedio de Accesos',
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig_barras_accesos)

    # Divider para separar secciones
    st.markdown('---')

    # Sugerencias para el futuro
    st.subheader('📌 Recomendaciones')

    # KPI 1 - Estrategias Regionales
    st.markdown("**🗺️ KPI 1 - Focalizar esfuerzos en estrategias regionales ajustadas a las necesidades específicas de cada provincia, con énfasis en NEA y NOA**")
    st.progress(50)  # Progreso del 50%

    # KPI 2 - Reducción de la brecha
    st.markdown("**📡 KPI 2 - Desarrollar programas escalonados que atiendan las necesidades de cada contexto provincial, cerrando la brecha de conectividad.**")
    st.progress(30)  # Progreso del 30%

    # KPI 3 - Planes Pospago Flexibles
    st.markdown("**📱 KPI 3 - Ofrecer planes personalizados que incluyan beneficios de largo plazo, incentivando a los usuarios prepago a migrar a pospago.**")
    st.progress(60)  # Progreso del 60%
