import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import psycopg2
import json


# Crear un menú de selección en la barra lateral
st.sidebar.title("Navegación")
menu = st.sidebar.selectbox("Selecciona una sección:", 
                              ['Resumen General', 
                               'KPI 1 - Acceso a Internet', 
                               'KPI 2 - Cobertura de Fibra Óptica', 
                               'KPI 3 - Aumento en Planes Pospago', 
                               'Conclusiones'])  


# Resumen General - Página Principal
if menu == 'Resumen General':
    st.title("Dashboard de Conectividad en Argentina")
    
    st.write("""
    Este dashboard presenta un análisis sobre el sector de telecomunicaciones en Argentina. 
    A continuación, encontrarás un resumen de los principales KPIs, que buscan medir el progreso 
    en el acceso a internet, la cobertura de tecnologías avanzadas y el crecimiento de líneas pospago.
    """)

    # Tarjetas de KPIs
    st.subheader('KPIs Resumen')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Acceso a Internet", value="2% Aumento", delta="Proyección Trimestral")
    
    with col2:
        st.metric(label="Cobertura de Fibra Óptica", value="10% Aumento", delta="Provincias con menor cobertura")
    
    with col3:
        st.metric(label="Acceso a Líneas Pospago", value="5% Aumento", delta="Proyección Trimestral")

    st.write("### Explicación de los KPIs")
    st.write("""
    - **Acceso a Internet**: Proyección de un aumento del 2% en el acceso a internet por cada 100 hogares en las distintas provincias.
    - **Cobertura de Fibra Óptica**: Aumento del 10% trimestral en la cobertura de tecnologías avanzadas (fibra óptica) en provincias con menor acceso.
    - **Acceso a Líneas Pospago**: Proyección de un aumento del 5% en los accesos a líneas pospago durante el próximo trimestre.
    """)

# KPI 1 - Acceso a Internet
elif menu == 'KPI 1 - Acceso a Internet':
    st.title('Análisis de Penetración de Internet (KPI 1)')

    # Conexión a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="telecomunicaciones",
        user="adminDB",
        password="Home_coming1306"
    )

    # Consulta SQL para obtener la penetración de internet por provincia y año
    query = """
    SELECT 
        p.nombre_provincia, 
        pe.anio, 
        pe.trimestre,
        ph.accesos_por_100_hogares
    FROM 
        penetracion_internet_hogares ph
    JOIN 
        provincias p ON ph.id_provincia = p.id_provincia
    JOIN 
        periodos pe ON ph.id_periodo = pe.id_periodo;
    """

    # Ejecutar la consulta y cargar los resultados en un DataFrame de Pandas
    df_penetracion = pd.read_sql(query, conn)
    conn.close()

    # Filtrar los datos a partir de 2023
    df_penetracion_reciente = df_penetracion[df_penetracion['anio'] >= 2023].sort_values('accesos_por_100_hogares')

    # Crear columna 'anio_trimestre'
    df_penetracion_reciente['anio_trimestre'] = df_penetracion_reciente['anio'].astype(str) + ' T' + df_penetracion_reciente['trimestre'].astype(str)

    # Figura
    plt.figure(figsize=(16, 9))

    # Gráfico de barras agrupadas
    sns.barplot(x='nombre_provincia', y='accesos_por_100_hogares', hue='anio_trimestre', 
                data=df_penetracion_reciente, dodge=True, palette='inferno_r')

    # Título y etiquetas
    plt.title('Penetración de Internet por cada 100 Hogares (2023 en adelante)', fontsize=18)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.xlabel('Provincia', fontsize=14)
    plt.ylabel('Accesos por 100 Hogares', fontsize=14)

    # Ajuste del límite superior del eje Y
    plt.ylim(0, df_penetracion_reciente['accesos_por_100_hogares'].max() + 10)

    # Ajuste de la leyenda
    plt.legend(title='Año y Trimestre', bbox_to_anchor=(0.5, 0.987), loc='upper center', ncol=5)

    # Líneas de fondo en el eje Y
    plt.grid(True, which='both', axis='y', linestyle='-', linewidth=0.5, alpha=0.3)

    # Visualización
    plt.tight_layout()
    st.pyplot(plt)

    # Título de la sección: Evolución de la Penetración
    st.header('Evolución de la Penetración de Internet por Provincia')

    # Sidebar para seleccionar la provincia
    provincia_seleccionada = st.selectbox(
    'Selecciona una provincia:', 
    sorted(df_penetracion_reciente['nombre_provincia'].unique())
    )

    # Filtrar los datos por la provincia seleccionada
    df_provincia_filtrada = df_penetracion_reciente[df_penetracion_reciente['nombre_provincia'] == provincia_seleccionada]

    # Crear gráfico de líneas
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='anio_trimestre', y='accesos_por_100_hogares', data=df_provincia_filtrada, marker='o')

    # Título y etiquetas
    plt.title(f'Evolución de la Penetración de Internet por Provincia: {provincia_seleccionada} (2023 en adelante)', fontsize=16)
    plt.xlabel('Año y Trimestre', fontsize=12)
    plt.ylabel('Accesos por 100 Hogares', fontsize=12)

    # Rotar etiquetas del eje X para mejorar la legibilidad
    plt.xticks(rotation=45)

    # Mostrar gráfico en Streamlit
    st.pyplot(plt)

    # Mapa de Penetración
    st.title('Mapa de Penetración de Internet por Provincia')

    # Shapefile de las provincias argentinas
    shapefile_path = 'dashboard/Mapa/provincia.shp'  # Ruta al  
    gdf_provincias = gpd.read_file(shapefile_path)

    # Usar la columna 'nam' para los nombres de las provincias
    gdf_provincias['nombre_provincia'] = gdf_provincias['nam'].str.lower()

    # Conexión a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="telecomunicaciones",
        user="adminDB",
        password="Home_coming1306"
    )

    # Consulta SQL para obtener la penetración de internet por provincia y año
    query = """
    SELECT 
        p.nombre_provincia, 
        AVG(ph.accesos_por_100_hogares) AS promedio_accesos
    FROM 
        penetracion_internet_hogares ph
    JOIN 
        provincias p ON ph.id_provincia = p.id_provincia
    JOIN 
        periodos pe ON ph.id_periodo = pe.id_periodo
    WHERE 
        pe.anio >= 2024
    GROUP BY 
        p.nombre_provincia;
    """

    # Ejecutar la consulta y cargar los resultados en un DataFrame de Pandas
    df_penetracion_provincia = pd.read_sql(query, conn)
    conn.close()

    # Normalizar los nombres de las provincias en el DataFrame
    df_penetracion_provincia['nombre_provincia'] = df_penetracion_provincia['nombre_provincia'].str.lower()

    # Hacer el merge de los datos de penetración con el GeoDataFrame de provincias
    gdf_provincias = gdf_provincias.merge(df_penetracion_provincia, on='nombre_provincia')

    # Agregar un filtro interactivo para seleccionar provincias
    provincias_seleccionadas = st.multiselect(
        'Selecciona las provincias a visualizar:',
        options=gdf_provincias['nombre_provincia'].unique(),
        default=gdf_provincias['nombre_provincia'].unique()
    )

    # Filtrar el GeoDataFrame en función de las provincias seleccionadas
    gdf_provincias_filtrado = gdf_provincias[gdf_provincias['nombre_provincia'].isin(provincias_seleccionadas)]

    # Crear el mapa base con Folium y centrado en Argentina
    m = folium.Map(
        location=[-38.4161, -63.6167],  # Centro de Argentina
        zoom_start=4
    )

    # Crear el mapa coroplético con los datos de penetración
    folium.Choropleth(
        geo_data=gdf_provincias_filtrado,
        name='choropleth',
        data=gdf_provincias_filtrado,
        columns=['nombre_provincia', 'promedio_accesos'],
        key_on='feature.properties.nombre_provincia',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Accesos por 100 Hogares',
    ).add_to(m)

    # Agregar pop-ups con información detallada de cada provincia
    for _, row in gdf_provincias_filtrado.iterrows():
        folium.Marker(
            location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
            popup=f"{row['nombre_provincia'].capitalize()}: {row['promedio_accesos']:.2f} accesos por 100 hogares"
        ).add_to(m)

    # Mostrar el mapa en Streamlit
    folium_static(m)


# KPI 2 - Cobertura de Fibra Óptica
elif menu == 'KPI 2 - Cobertura de Fibra Óptica':
    st.title('KPI 2: Cobertura de Fibra Óptica')

    import streamlit as st
    import psycopg2
    import pandas as pd
    import plotly.express as px
    import json

    # Conexión a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="telecomunicaciones",
        user="adminDB",
        password="Home_coming1306"
    )

    # Consulta SQL
    query = """
    SELECT 
        l.localidad, 
        p.nombre_provincia, 
        mc.fibra_optica, 
        mc.wireless, 
        mc.poblacion 
    FROM 
        mapa_conectividad mc
    JOIN 
        localidades l ON mc.id_localidad = l.id_localidad
    JOIN 
        provincias p ON l.id_provincia = p.id_provincia
    WHERE 
        mc.fibra_optica = TRUE OR mc.wireless = TRUE
    ORDER BY 
        p.nombre_provincia, l.localidad;
    """
    
    # Cargar los datos
    df_tecnologias = pd.read_sql(query, conn)
    conn.close()

    # Filtro interactivo de provincias
    provincias = df_tecnologias['nombre_provincia'].unique()
    provincia_seleccionada = st.multiselect('Selecciona la Provincia', provincias, default=provincias)

    # Filtrar el DataFrame por las provincias seleccionadas
    df_filtrado = df_tecnologias[df_tecnologias['nombre_provincia'].isin(provincia_seleccionada)]

    # --- Gráfico 1: Porcentaje de localidades con fibra óptica por provincia ---
    df_fibra_optica = df_filtrado[df_filtrado['fibra_optica'] == True]

    total_localidades_provincia = df_filtrado.groupby('nombre_provincia')['localidad'].count()
    localidades_fibra_provincia = df_fibra_optica.groupby('nombre_provincia')['localidad'].count()

    porcentaje_fibra_optica = (localidades_fibra_provincia / total_localidades_provincia) * 100
    porcentaje_fibra_optica = porcentaje_fibra_optica.sort_values()

    # Gráfico de barras con tooltips
    fig1 = px.bar(
        porcentaje_fibra_optica,
        x=porcentaje_fibra_optica.values,
        y=porcentaje_fibra_optica.index,
        labels={'x': 'Porcentaje de Localidades con Fibra Óptica', 'y': 'Provincia'},
        title='Porcentaje de Localidades con Fibra Óptica por Provincia',
        text=porcentaje_fibra_optica.values
    )
    fig1.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    st.plotly_chart(fig1)

    # --- Gráfico 2: Cobertura actual vs proyectada ---
    prov_menor_cobertura_fibra = df_filtrado.groupby('nombre_provincia')['fibra_optica'].mean()
    prov_menor_cobertura_fibra = prov_menor_cobertura_fibra[prov_menor_cobertura_fibra < prov_menor_cobertura_fibra.quantile(0.25)]
    prov_menor_cobertura_fibra_proyectado = prov_menor_cobertura_fibra * 1.30

    df_fibra_optica = pd.DataFrame({
        'Provincia': prov_menor_cobertura_fibra.index,
        'Cobertura Actual': prov_menor_cobertura_fibra.values,
        'Cobertura Proyectada': prov_menor_cobertura_fibra_proyectado.values
    })

    df_fibra_optica_melted = df_fibra_optica.melt(id_vars='Provincia', 
                                                  value_vars=['Cobertura Actual', 'Cobertura Proyectada'], 
                                                  var_name='Cobertura', value_name='Porcentaje')

    # Gráfico con tooltips
    fig2 = px.bar(
        df_fibra_optica_melted,
        x='Provincia', 
        y='Porcentaje', 
        color='Cobertura',
        barmode='group',
        text='Porcentaje',
        title='Cobertura de Fibra Óptica Actual vs. Proyectada (10% Aumento)'
    )
    fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    st.plotly_chart(fig2)


    # --- Mapa: Visualización geográfica de la cobertura de fibra óptica ---
    import streamlit as st
    import folium
    import pandas as pd
    from streamlit_folium import st_folium
    import json

    # --- Mapa: Visualización geográfica de la cobertura de fibra óptica ---

    import streamlit as st
    import folium
    import pandas as pd
    from streamlit_folium import st_folium
    import json

# --- Mapa: Visualización geográfica de la cobertura de fibra óptica ---

    # Cargar el archivo GeoJSON
    geojson_path = 'dashboard/ProvinciasArgentina_actualizado.geojson'
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Calcular porcentaje de cobertura de fibra óptica por provincia
    cobertura_provincia = df_filtrado.groupby('nombre_provincia')['fibra_optica'].mean() * 100

    # Crear el mapa centrado en Argentina con Folium
    m = folium.Map(location=[-38.4161, -63.6167], zoom_start=4)

    # Añadir el GeoJSON al mapa con colores personalizados según la cobertura
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name="Cobertura de Fibra Óptica",
        data=cobertura_provincia,
        columns=[cobertura_provincia.index, cobertura_provincia],
        key_on="feature.properties.nombre",  # Debe coincidir con la clave 'nombre' en el GeoJSON
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Cobertura de Fibra Óptica (%)",
    ).add_to(m)

    # Añadir tooltips personalizados (con nombre y cobertura) a cada provincia
    for feature in geojson_data['features']:
        nombre_provincia = feature['properties']['nombre']
        
        # Obtener la cobertura de la provincia; si no hay datos, mostrar 'No data'
        cobertura = cobertura_provincia.get(nombre_provincia, 'No data')
        
        # Crear el popup/tooltip con nombre y cobertura
        if cobertura != 'No data':
            popup_text = f"{nombre_provincia}: {cobertura:.2f}% cobertura"
        else:
            popup_text = f"{nombre_provincia}: No data"
        
        # Añadir un Popup (ventana emergente) a cada geometría del GeoJSON
        folium.GeoJson(
            feature,
            tooltip=folium.Tooltip(popup_text)
        ).add_to(m)

    # Añadir controles de capas
    folium.LayerControl().add_to(m)

    # Mostrar el mapa en Streamlit
    st.title('Cobertura de Fibra Óptica por Provincia')

    # Renderizar el mapa de Folium dentro de Streamlit
    st_data = st_folium(m, width=725)


    # --- KPIs Adicionales: Progreso hacia el 10% proyectado ---
    


    # Calcular el promedio actual de cobertura de fibra óptica a nivel nacional
    promedio_cobertura_actual = cobertura_provincia.mean()

    # Progreso hacia el 10% proyectado (actual + 10%)
    objetivo_cobertura = promedio_cobertura_actual * 1.10

    # Mostrar los KPIs en tarjetas
    st.subheader('Progreso hacia el 10% de aumento en la cobertura de fibra óptica')

    col1, col2 = st.columns(2)

    # Tarjeta 1: Cobertura Actual
    col1.metric(
        label="Cobertura Actual Promedio",
        value=f"{promedio_cobertura_actual:.2f}%",
        delta=f"+{(promedio_cobertura_actual):.2f}% del total actual"
    )

    # Tarjeta 2: Proyección 10%
    col2.metric(
        label="Cobertura Proyectada",
        value=f"{objetivo_cobertura:.2f}%",
        delta=f"+{(objetivo_cobertura - promedio_cobertura_actual):.2f}% adicional proyectado"
    )








    # Reutiliza el código que ya has implementado para KPI 2


# KPI 3 - Aumento de planes Pospago
elif menu == 'KPI 3 - Aumento en Planes Pospago':
    st.title('KPI 3: Aumento en Planes Pospago')


    # Consulta a la base de datos
    conn = psycopg2.connect(
        host="localhost",
        database="telecomunicaciones",
        user="adminDB",
        password="Home_coming1306"
    )
    
    # Ejecutar la consulta para obtener los accesos pospago y prepago
    query = """
        SELECT 
            pe.anio,
            pe.trimestre,
            atm.total_accesos_pospago,
            atm.total_accesos_prepago
        FROM 
            accesos_telefonia_movil atm
        JOIN
            periodos pe ON atm.id_periodo = pe.id_periodo
        ORDER BY 
            pe.anio, pe.trimestre;
    """
    
    df_telefonia = pd.read_sql(query, conn)
    conn.close()

    # --- Gráfico 1: Evolución trimestral del acceso a líneas pospago ---
    st.subheader('Evolución Trimestral del Acceso a Líneas Pospago (2023 en adelante)')
    
    # Filtro interactivo desde 2023
    df_pospago_reciente = df_telefonia[df_telefonia['anio'] >= 2023]

    # Crear columna combinada para año y trimestre
    df_pospago_reciente['anio_trimestre'] = df_pospago_reciente['anio'].astype(str) + ' T' + df_pospago_reciente['trimestre'].astype(str)

    # Crear el gráfico de barras
    plt.figure(figsize=(12, 4))
    sns.barplot(y='anio_trimestre', x='total_accesos_pospago', data=df_pospago_reciente, palette='Blues_d')

    plt.title('Evolución Trimestral del Acceso a Líneas Pospago (2023 en adelante)', fontsize=16)
    plt.xlabel('Total de Accesos Pospago', fontsize=12)
    plt.ylabel('Año y Trimestre', fontsize=12)

    # Añadir los valores en cada barra
    for index, value in enumerate(df_pospago_reciente['total_accesos_pospago']):
        plt.text(value, index, f'{value:,.0f}', color='black', va="center")

    st.pyplot(plt)


    # --- Gráfico 2: Proyección de un aumento del 5% ---
    st.subheader('Proyección de Aumento del 5% en Accesos de Planes Pospago (2024 T3)')

    # Datos históricos y proyección
    trimestres = ['2023 T1', '2023 T2', '2023 T3', '2023 T4', '2024 T1', '2024 T2']
    accesos_postpago = [7028083, 7310125, 7903181, 8301200, 8398514, 8397205]  # Datos oficiales

    # Proyección del 5% para el tercer trimestre de 2024
    proyeccion_t3_2024 = 8397205 * 1.05

    # Agregar el trimestre proyectado
    trimestres.append('2024 T3')
    accesos_postpago.append(proyeccion_t3_2024)

    # Gráfico de líneas
    plt.figure(figsize=(12, 6))
    plt.plot(trimestres[:-1], accesos_postpago[:-1], marker='o', label='Datos Históricos')
    plt.plot(trimestres[-2:], accesos_postpago[-2:], marker='o', linestyle='--', color='orange', label='Proyección')

    # Anotación para el valor proyectado
    plt.annotate(f'{proyeccion_t3_2024:,.0f}', xy=('2024 T3', proyeccion_t3_2024), xytext=(-25, 6), textcoords='offset points')

    plt.title('Proyección del 5% en Accesos de Planes Pospago (2024 T3)', fontsize=16)
    plt.xlabel('Período (Año y Trimestre)', fontsize=12)
    plt.ylabel('Accesos de Planes Pospago', fontsize=12)
    plt.legend()

    st.pyplot(plt)


    # --- Gráfico 3: Distribución de accesos pospago y prepago ---
    st.subheader('Distribución de Accesos Pospago y Prepago (2024 T1 y T2)')

    # Filtrar los datos para 2024 T1 y T2
    df_t2_2024 = df_telefonia[df_telefonia['anio'] == 2024]

    # Sumar los accesos pospago y prepago
    accesos_pospago = df_t2_2024['total_accesos_pospago'].sum()
    accesos_prepago = df_t2_2024['total_accesos_prepago'].sum()

    # Gráfico de torta
    plt.figure(figsize=(7, 7))
    plt.pie([accesos_pospago, accesos_prepago], labels=['Pospago', 'Prepago'], autopct='%1.1f%%', colors=['#1E90FF', '#87CEEB'], startangle=90, wedgeprops={'edgecolor': 'black'})
    plt.title('Distribución de Accesos Pospago y Prepago (2024 T1 y T2)', fontsize=16)
    plt.axis('equal')  # Mantener el gráfico circular

    st.pyplot(plt)


    # --- KPIs Adicionales ---
    st.subheader('Progreso hacia el 5% de aumento en los accesos a líneas pospago')

    col1, col2 = st.columns(2)

    # Tarjeta 1: Accesos Pospago actuales (Último trimestre disponible)
    accesos_pospago_actuales = df_pospago_reciente['total_accesos_pospago'].iloc[-1]
    proyeccion_5p = accesos_pospago_actuales * 1.05

    col1.metric("Accesos Pospago Actuales", f"{accesos_pospago_actuales:,}", delta=f"+{accesos_pospago_actuales:,}")

    # Tarjeta 2: Proyección del 5%
    col2.metric("Proyección Pospago (5%)", f"{proyeccion_5p:,.0f}", delta=f"+{proyeccion_5p - accesos_pospago_actuales:,.0f}")



# Página de Conclusiones
elif menu == 'Conclusiones':
    st.title('Conclusiones y Oportunidades de Mejora')

    # Resumen de conclusiones clave
    st.subheader('Resumen de Conclusiones Clave')
    
    conclusions = [
        "El acceso a internet ha mostrado un aumento sostenido, con un incremento del 2% en la penetración general.",
        "La cobertura de fibra óptica ha aumentado un 10% en las provincias de menor acceso, con un porcentaje actual de 58.33%.",
        "El acceso a líneas pospago ha aumentado significativamente, con un crecimiento proyectado del 5% para el tercer trimestre de 2024.",
        "La tendencia de acceso a servicios de telecomunicaciones, como la telefonía móvil, muestra un crecimiento estable, pero aún existen áreas de mejora en el acceso a servicios de calidad."
    ]
    
    for conclusion in conclusions:
        st.markdown(f"- {conclusion}")

    # Gráfico de respaldo para el KPI de cobertura de fibra óptica
    st.subheader('Cobertura de Fibra Óptica Actual')
    # Puedes reutilizar el gráfico del KPI 2 aquí
    # st.plotly_chart(fig_fibra_optica)  # Asegúrate de tener la variable correspondiente

    # Indicadores de Rendimiento
    st.subheader('Indicadores de Rendimiento')

    # KPIs cumplidos
    st.markdown("**KPIs Cumplidos:**")
    st.markdown("- KPI 1: Aumento del 2% en el acceso a internet.")
    st.markdown("- KPI 2: Aumento del 10% en la cobertura de fibra óptica.")
    st.markdown("- KPI 3: Aumento del 5% en el acceso a líneas pospago proyectado.")

    # Sugerencias para el futuro
    st.markdown("**Sugerencias para el Futuro:**")
    suggestions = [
        "Mejorar la infraestructura en las provincias con menor cobertura de fibra óptica.",
        "Desarrollar campañas informativas para aumentar la adopción de planes pospago en zonas rurales.",
        "Monitorear y ajustar las proyecciones de crecimiento según los datos trimestrales para mantener la estrategia alineada con el mercado."
    ]
    
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")




