import streamlit as st

def display():
    st.title("Dashboard de Conectividad en Argentina")
    
    st.write("""
    Este dashboard presenta un análisis sobre el sector de telecomunicaciones en Argentina. 
    A continuación, encontrarás un resumen de los principales KPIs que miden el progreso 
    en el acceso a internet, la cobertura de tecnologías avanzadas y el crecimiento de líneas pospago.
    """)

    # Estilo de las tarjetas de KPI
    kpi_style = """
    <style>
    .card {
        background-color: #2b2b3d;
        padding: 20px;
        margin: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    .card h3 {
        color: #ffffff;
        font-size: 22px;
        margin: 0;
    }
    .card p {
        color: #21ba45;
        font-size: 18px;
        margin: 10px 0 0;
    }
    .card strong {
        font-size: 36px;
        color: #ffffff;
    }
    .card i {
        font-size: 50px;
        color: #21ba45;
    }
    </style>
    """

    # Aplicar el estilo de las tarjetas
    st.markdown(kpi_style, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class="card">
            <i class="fas fa-wifi"></i>
            <h3>Acceso a Internet</h3>
            <strong>2% Aumento</strong>
            <p>Proyección Trimestral</p>
        </div>""", unsafe_allow_html=True)
        
    with col2:
        st.markdown("""<div class="card">
            <i class="fas fa-network-wired"></i>
            <h3>Cobertura de Fibra Óptica</h3>
            <strong>10% Aumento</strong>
            <p>Provincias con menor cobertura</p>
        </div>""", unsafe_allow_html=True)
       
    with col3:
        st.markdown("""<div class="card">
            <i class="fas fa-mobile-alt"></i>
            <h3>Acceso a Líneas Pospago</h3>
            <strong>5% Aumento</strong>
            <p>Proyección Trimestral</p>
        </div>""", unsafe_allow_html=True)

    # Explicación de los KPIs
    st.write("### Explicación de los KPIs")
    st.write("""
    - **Acceso a Internet**: Proyección de un aumento del 2% en el acceso a internet por cada 100 hogares en las distintas provincias.
    - **Cobertura de Fibra Óptica**: Aumento del 10% trimestral en la cobertura de tecnologías avanzadas (fibra óptica) en provincias con menor acceso.
    - **Acceso a Líneas Pospago**: Proyección de un aumento del 5% en los accesos a líneas pospago durante el próximo trimestre.
    """)
