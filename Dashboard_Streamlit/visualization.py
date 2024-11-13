import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
import json
from streamlit_folium import st_folium


# -- GRÁFICOS PARA KPI 1: ACCESO A INTERNET --

# PRIMER GRÁFICO: Penetración de Internet por cada 100 hogares
def graficar_penetracion_internet(df_penetracion):
    """
    Genera un gráfico de barras agrupadas interactivo que muestra la penetración de internet 
    por cada 100 hogares en diferentes provincias y trimestres.

    Parámetros:
    - df_penetracion (DataFrame): DataFrame con las columnas 'nombre_provincia', 
                                  'anio', 'trimestre', y 'accesos_por_100_hogares'.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Filtrar los datos a partir de 2023
    df_penetracion_reciente = df_penetracion[df_penetracion['anio'] >= 2023].sort_values('accesos_por_100_hogares')

    # Crear columna 'anio_trimestre'
    df_penetracion_reciente['anio_trimestre'] = df_penetracion_reciente['anio'].astype(str) + ' T' + df_penetracion_reciente['trimestre'].astype(str)

    # Crear una columna temporal para ordenar correctamente por año y trimestre
    df_penetracion_reciente['orden'] = df_penetracion_reciente['anio'] * 10 + df_penetracion_reciente['trimestre']

    # Ordenar el DataFrame por la nueva columna 'orden'
    df_penetracion_reciente = df_penetracion_reciente.sort_values(by='orden')

    # Eliminar la columna temporal después de la ordenación
    df_penetracion_reciente.drop(columns=['orden'], inplace=True)
   
    # Gráfico interactivo de barras agrupadas
    fig_barras = px.bar(
        df_penetracion_reciente, 
        x='nombre_provincia', 
        y='accesos_por_100_hogares', 
        color='anio_trimestre', 
        title='Penetración de Internet por cada 100 Hogares (2023 en adelante)',
        labels={'accesos_por_100_hogares': 'Accesos por 100 Hogares', 'nombre_provincia': 'Provincia'},
        hover_data=['anio', 'trimestre'],  # Mostrar detalles al pasar el ratón
        barmode='group'  # Agrupar las barras
    )

    # Personalización del gráfico
    fig_barras.update_layout(
        xaxis_title='Provincia',
        yaxis_title='Accesos por 100 Hogares',
        legend_title_text='Año y Trimestre',
        xaxis_tickangle=-45,  # Rotar las etiquetas del eje X
        yaxis_range=[0, df_penetracion_reciente['accesos_por_100_hogares'].max() + 10]
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig_barras)


# SEGUNDO GRÁFICO: Comparativa de acceso actual vs. proyectado
def graficar_comparativa_acceso_proyectado(df_penetracion):
    """
    Genera un gráfico de barras agrupadas interactivo que muestra la comparativa de acceso a internet
    por cada 100 hogares en las provincias de Argentina, comparando el acceso actual con la proyección
    de un 2% de aumento para el próximo trimestre.

    Parámetros:
    - df_penetracion (DataFrame): DataFrame con las columnas 'nombre_provincia', 'anio_trimestre',
                                  'accesos_por_100_hogares', y otros datos necesarios.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Crear df_penetracion_reciente para filtrar datos a partir de 2023 y crear columna 'anio_trimestre'
    df_penetracion_reciente = df_penetracion[df_penetracion['anio'] >= 2023].copy()
    df_penetracion_reciente['anio_trimestre'] = df_penetracion_reciente['anio'].astype(str) + ' T' + df_penetracion_reciente['trimestre'].astype(str)

    # Filtrar datos para el último trimestre registrado (2024 T1) y copiar para la proyección
    df_kpi = df_penetracion_reciente[df_penetracion_reciente['anio_trimestre'] == '2024 T1'].copy()

    # Agregar columna con el nuevo acceso proyectado con un 2% de aumento
    df_kpi['acceso_proyectado'] = df_kpi['accesos_por_100_hogares'] * 1.02

    # Reorganizar el DataFrame para Plotly
    df_kpi_melted = df_kpi.melt(id_vars='nombre_provincia', 
                                value_vars=['accesos_por_100_hogares', 'acceso_proyectado'], 
                                var_name='Acceso', 
                                value_name='Cantidad')

    # Cambiar nombres de las categorías para la leyenda
    df_kpi_melted['Acceso'] = df_kpi_melted['Acceso'].replace({
        'accesos_por_100_hogares': 'Acceso Actual (2024 T1)',
        'acceso_proyectado': 'Acceso Proyectado (2024 T2 con 2% aumento)'
    })

    # Crear gráfico de barras agrupadas interactivo
    fig_barras = px.bar(
        df_kpi_melted, 
        x='nombre_provincia', 
        y='Cantidad', 
        color='Acceso',
        title='Comparativa de Acceso a Internet por 100 Hogares: Actual vs. Proyectado (2% Aumento)',
        labels={'Cantidad': 'Accesos por 100 Hogares', 'nombre_provincia': 'Provincia'},
        barmode='group',  # Agrupar las barras por tipo de acceso
        hover_data=['Acceso']  # Mostrar detalles al pasar el ratón
    )

    # Personalización del gráfico
    fig_barras.update_layout(
        xaxis_title='Provincia',
        yaxis_title='Accesos por 100 Hogares',
        legend_title_text='Tipo de Acceso',
        xaxis_tickangle=-45,  # Rotar etiquetas para mejor lectura
        yaxis_range=[0, df_kpi_melted['Cantidad'].max() + 10]
    )

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig_barras, use_container_width=True)


# TERCER GRÁFICO: Evolución de la penetración de internet por provincia
def graficar_evolucion_penetracion_provincia(df_penetracion, provincia):
    """
    Genera un gráfico de líneas que muestra la evolución de la penetración de internet 
    por cada 100 hogares en una provincia seleccionada, incluyendo una proyección con un 
    aumento del 2% en el último trimestre disponible.

    Parámetros:
    - df_penetracion (DataFrame): DataFrame con las columnas 'nombre_provincia', 'anio_trimestre', 
                                  y 'accesos_por_100_hogares'.
    - provincia (str): Nombre de la provincia seleccionada.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Filtrar datos a partir de 2023 y crear columna 'anio_trimestre'
    df_penetracion_reciente = df_penetracion[df_penetracion['anio'] >= 2023].copy().sort_values('accesos_por_100_hogares')
    df_penetracion_reciente['anio_trimestre'] = df_penetracion_reciente['anio'].astype(str) + ' T' + df_penetracion_reciente['trimestre'].astype(str)

    # Filtrar los datos por la provincia seleccionada
    df_provincia_filtrada = df_penetracion_reciente[df_penetracion_reciente['nombre_provincia'] == provincia]

    # Obtener los datos del último trimestre para calcular la proyección
    df_kpi = df_provincia_filtrada[df_provincia_filtrada['anio_trimestre'] == '2024 T1']

    # Proyectar un aumento del 2% en accesos para 2024 T2
    if not df_kpi.empty:
        acceso_actual = df_kpi['accesos_por_100_hogares'].values[0]
        acceso_proyectado = acceso_actual * 1.02

        # Crear los datos de proyección
        datos_proyectados = {
            'anio_trimestre': ['2024 T2'],
            'accesos_por_100_hogares': [acceso_proyectado],
            'nombre_provincia': provincia
        }

        df_proyeccion = pd.DataFrame(datos_proyectados)

        # Concatenar los datos históricos y proyectados
        df_completo = pd.concat([df_provincia_filtrada, df_proyeccion])

        # Gráfico interactivo de líneas
        fig_lineas = px.line(
            df_completo, 
            x='anio_trimestre', 
            y='accesos_por_100_hogares', 
            title=f'Evolución de la Penetración de Internet por Provincia: {provincia} (2023 en adelante)',
            labels={'anio_trimestre': 'Año y Trimestre', 'accesos_por_100_hogares': 'Accesos por 100 Hogares'},
            markers=True
        )

        # Personalización del gráfico
        fig_lineas.update_layout(
            xaxis_title='Año y Trimestre',
            yaxis_title='Accesos por 100 Hogares',
            xaxis_tickangle=-45
        )

        # Añadir anotación en el punto proyectado
        fig_lineas.add_annotation(
            x='2024 T2',
            y=acceso_proyectado,
            text="Proyección",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_lineas, use_container_width=True)


# CUARTO GRÁFICO: Mapa de coropletas con la penetración de internet por provincia
def graficar_mapa_penetracion(df_penetracion_provincia, geojson_path):
    """
    Genera un mapa de coropletas interactivo que muestra la penetración de internet
    por cada 100 hogares en cada provincia de Argentina.

    Parámetros:
    - df_penetracion_provincia (DataFrame): DataFrame con los nombres de las provincias y
                                            su penetración promedio.
    - geojson_path (str): Ruta al archivo GeoJSON con las geometrías de las provincias.

    Retorno:
    - None: Muestra el mapa interactivo en Streamlit.
    """
    # Cargar el archivo GeoJSON
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Crear el mapa centrado en Argentina
    m = folium.Map(location=[-38.4161, -63.6167], zoom_start=4)

    # Crear mapa de coropletas con Folium
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name="Penetración de Internet",
        data=df_penetracion_provincia.set_index('nombre_provincia'),
        columns=[df_penetracion_provincia.set_index('nombre_provincia').index, 'promedio_accesos'],
        key_on="feature.properties.nombre",  # Usar la clave correcta del GeoJSON
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Accesos por 100 Hogares",
    ).add_to(m)

    # Añadir tooltips personalizados para cada provincia
    for feature in geojson_data['features']:
        nombre_provincia = feature['properties']['nombre'].lower()
        penetracion = df_penetracion_provincia.set_index('nombre_provincia').get('promedio_accesos').get(nombre_provincia, 'No data')
        
        popup_text = f"{nombre_provincia.capitalize()}: {penetracion:.2f} accesos por 100 hogares" if penetracion != 'No data' else f"{nombre_provincia.capitalize()}: No data"
        
        folium.GeoJson(
            feature,
            tooltip=folium.Tooltip(popup_text)
        ).add_to(m)

    # Añadir controles de capas
    folium.LayerControl().add_to(m)

    # Mostrar el mapa en Streamlit
    st.subheader("Mapa de Penetración por Provincia")
    st_folium(m, width=725)


# -- GRÁFICOS PARA KPI 2: COBERTURA DE FIBRA ÓPTICA --

# PRIMER GRÁFICO: Porcentaje de localidades con fibra óptica por provincia
def graficar_porcentaje_localidades_fibra(df):
    """
    Genera un gráfico de barras que muestra el porcentaje de localidades con fibra óptica por provincia.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'nombre_provincia', 'localidad', y 'fibra_optica'.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Filtro interactivo de provincias
    provincias = df['nombre_provincia'].unique()
    provincia_seleccionada = st.multiselect('Selecciona la Provincia', provincias, default=provincias)

    # Filtrar el DataFrame por las provincias seleccionadas
    df_filtrado = df[df['nombre_provincia'].isin(provincia_seleccionada)]

    # Calcular el porcentaje de localidades con fibra óptica
    df_fibra_optica = df_filtrado[df_filtrado['fibra_optica'] == True]
    total_localidades_provincia = df_filtrado.groupby('nombre_provincia')['localidad'].count()
    localidades_fibra_provincia = df_fibra_optica.groupby('nombre_provincia')['localidad'].count()

    porcentaje_fibra_optica = (localidades_fibra_provincia / total_localidades_provincia) * 100
    porcentaje_fibra_optica = porcentaje_fibra_optica.sort_values()

    # Crear gráfico de barras
    fig = px.bar(
        porcentaje_fibra_optica,
        x=porcentaje_fibra_optica.values,
        y=porcentaje_fibra_optica.index,
        labels={'x': 'Porcentaje de Localidades con Fibra Óptica', 'y': 'Provincia'},
        title='Porcentaje de Localidades con Fibra Óptica por Provincia',
        text=porcentaje_fibra_optica.values
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# SEGUNDO GRÁFICO: Cobertura de fibra óptica actual vs. proyectada
def graficar_cobertura_fibra_optica_proyectada(df):
    """
    Genera un gráfico de barras que muestra la cobertura de fibra óptica actual vs. proyectada
    en provincias con menor cobertura.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'nombre_provincia' y 'fibra_optica'.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Filtrar provincias con menor cobertura (por debajo del 25% del total)
    prov_menor_cobertura_fibra = df.groupby('nombre_provincia')['fibra_optica'].mean()
    prov_menor_cobertura_fibra = prov_menor_cobertura_fibra[prov_menor_cobertura_fibra < prov_menor_cobertura_fibra.quantile(0.25)]
    
    # Proyección de aumento del 30% en la cobertura
    prov_menor_cobertura_fibra_proyectado = prov_menor_cobertura_fibra * 1.30

    # Crear un DataFrame para el gráfico
    df_fibra_optica = pd.DataFrame({
        'Provincia': prov_menor_cobertura_fibra.index,
        'Cobertura Actual': prov_menor_cobertura_fibra.values,
        'Cobertura Proyectada': prov_menor_cobertura_fibra_proyectado.values
    })

    # Transformar el DataFrame para mostrar la cobertura actual vs proyectada
    df_fibra_optica_melted = df_fibra_optica.melt(id_vars='Provincia', 
                                                  value_vars=['Cobertura Actual', 'Cobertura Proyectada'], 
                                                  var_name='Cobertura', value_name='Porcentaje')

    # Gráfico de barras agrupadas
    fig = px.bar(
        df_fibra_optica_melted,
        x='Provincia', 
        y='Porcentaje', 
        color='Cobertura',
        barmode='group',
        text='Porcentaje',
        title='Cobertura de Fibra Óptica Actual vs. Proyectada (30% Aumento)'
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# TERCER GRÁFICO: Mapa de coropletas con la cobertura de fibra óptica por provincia
def graficar_mapa_cobertura_fibra(df, geojson_path):
    """
    Genera un mapa de coropletas interactivo que muestra el porcentaje de cobertura de fibra óptica
    por cada provincia en Argentina.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'nombre_provincia' y 'fibra_optica'.
    - geojson_path (str): Ruta al archivo GeoJSON con las geometrías de las provincias.

    Retorno:
    - None: Muestra el mapa interactivo en Streamlit.
    """
    # Calcular el porcentaje de cobertura de fibra óptica por provincia
    cobertura_provincia = df.groupby('nombre_provincia')['fibra_optica'].mean() * 100

    # Cargar el archivo GeoJSON
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Crear el mapa centrado en Argentina
    m = folium.Map(location=[-38.4161, -63.6167], zoom_start=4)

    # Crear el mapa de coropletas con cobertura de fibra óptica
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name="Cobertura de Fibra Óptica",
        data=cobertura_provincia,
        columns=[cobertura_provincia.index, cobertura_provincia],
        key_on="feature.properties.nombre",  # Clave en el GeoJSON que corresponde con las provincias
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Cobertura de Fibra Óptica (%)",
    ).add_to(m)

    # Añadir tooltips personalizados con nombre y porcentaje de cobertura
    for feature in geojson_data['features']:
        nombre_provincia = feature['properties']['nombre'].lower()  # Aseguramos que coincide en minúsculas
        cobertura = cobertura_provincia.get(nombre_provincia, 'No data')
        
        # Crear el texto para el tooltip
        popup_text = f"{nombre_provincia.capitalize()}: {cobertura:.2f}% cobertura" if cobertura != 'No data' else f"{nombre_provincia.capitalize()}: No data"
        
        folium.GeoJson(
            feature,
            tooltip=folium.Tooltip(popup_text)
        ).add_to(m)

    # Añadir controles de capas
    folium.LayerControl().add_to(m)

    # Mostrar el mapa en Streamlit
    st.subheader("Cobertura de Fibra Óptica por Provincia")
    st_folium(m, width=725)


# CUARTO GRÁFICO: Proyección de aumento en la cobertura de fibra óptica
def mostrar_tarjetas_cobertura(df):
    """
    Muestra tarjetas de métricas que indican el progreso hacia el 10% de aumento
    en la cobertura de fibra óptica a nivel nacional.

    Parámetros:
    - df (DataFrame): DataFrame que contiene la columna 'fibra_optica' por provincia.
    """
    # Calcular porcentaje de cobertura de fibra óptica por provincia
    cobertura_provincia = df.groupby('nombre_provincia')['fibra_optica'].mean() * 100
    
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
        delta=f"+{promedio_cobertura_actual:.2f}% del total actual"
    )

    # Tarjeta 2: Proyección 10%
    col2.metric(
        label="Cobertura Proyectada",
        value=f"{objetivo_cobertura:.2f}%",
        delta=f"+{(objetivo_cobertura - promedio_cobertura_actual):.2f}% adicional proyectado"
    )

# -- GRÁFICOS PARA KPI 3: AUMENTO EN PLANES POSPAGO --

# PRIMER GRÁFICO: Evolución trimestral de accesos a líneas pospago
def graficar_evolucion_accesos_pospago(df):
    """
    Genera un gráfico de barras horizontales que muestra la evolución trimestral de
    los accesos a líneas pospago a partir del año 2023.

    Parámetros:
    - df (DataFrame): DataFrame con las columnas 'anio', 'trimestre' y 'total_accesos_pospago'.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Filtrar datos a partir de 2023
    df_pospago_reciente = df[df['anio'] >= 2023].copy()

    # Crear columna combinada para año y trimestre
    df_pospago_reciente['anio_trimestre'] = df_pospago_reciente['anio'].astype(str) + ' T' + df_pospago_reciente['trimestre'].astype(str)

    # Crear el gráfico de barras horizontales
    fig = px.bar(
        df_pospago_reciente, 
        x='total_accesos_pospago', 
        y='anio_trimestre', 
        orientation='h',
        title='Evolución Trimestral del Acceso a Líneas Pospago (2023 en adelante)',
        labels={'total_accesos_pospago': 'Total de Accesos Pospago', 'anio_trimestre': 'Año y Trimestre'},
        text='total_accesos_pospago',
        color='total_accesos_pospago',
        color_continuous_scale='Blues'
    )

    # Ajustes del gráfico
    fig.update_layout(
        xaxis_title='Total de Accesos Pospago',
        yaxis_title='Año y Trimestre',
        title_font_size=16,
        xaxis_tickformat=',',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# SEGUNDO GRÁFICO: Proyección de aumento en accesos pospago
def graficar_proyeccion_accesos_pospago():
    """
    Genera un gráfico de líneas que muestra la evolución histórica de accesos a planes pospago
    y una proyección de aumento del 5% para el tercer trimestre de 2024.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Datos históricos y proyección
    trimestres = ['2023 T1', '2023 T2', '2023 T3', '2023 T4', '2024 T1', '2024 T2']
    accesos_postpago = [7028083, 7310125, 7903181, 8301200, 8398514, 8397205]  # Datos oficiales

    # Proyección del 5% para el tercer trimestre de 2024
    proyeccion_t3_2024 = accesos_postpago[-1] * 1.05

    # Agregar el trimestre proyectado
    trimestres.append('2024 T3')
    accesos_postpago.append(proyeccion_t3_2024)

    # Crear la figura de líneas
    fig = go.Figure()

    # Datos históricos
    fig.add_trace(go.Scatter(
        x=trimestres[:-1], 
        y=accesos_postpago[:-1], 
        mode='lines+markers', 
        name='Datos Históricos',
        line=dict(color='blue')
    ))

    # Proyección
    fig.add_trace(go.Scatter(
        x=trimestres[-2:], 
        y=accesos_postpago[-2:], 
        mode='lines+markers', 
        name='Proyección', 
        line=dict(dash='dash', color='orange')
    ))

    # Anotación del valor proyectado
    fig.add_annotation(
        x='2024 T3',
        y=proyeccion_t3_2024,
        text=f'{proyeccion_t3_2024:,.0f}',
        showarrow=True,
        arrowhead=2
    )

    # Configuración del gráfico
    fig.update_layout(
        title='Proyección del 5% en Accesos de Planes Pospago (2024 T3)',
        xaxis_title='Período (Año y Trimestre)',
        yaxis_title='Accesos de Planes Pospago',
        legend_title_text='Datos',
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# TERCER GRÁFICO: Distribución de accesos pospago y prepago 
def graficar_distribucion_accesos(df):
    """
    Genera un gráfico de torta que muestra la distribución de accesos pospago y prepago
    para el primer y segundo trimestre de 2024.

    Parámetros:
    - df (DataFrame): DataFrame con las columnas 'anio', 'total_accesos_pospago' y 'total_accesos_prepago'.

    Retorno:
    - None: Muestra el gráfico interactivo en Streamlit.
    """
    # Filtrar los datos para 2024 T1 y T2
    df_t2_2024 = df[df['anio'] == 2024]

    # Sumar los accesos pospago y prepago
    accesos_pospago = df_t2_2024['total_accesos_pospago'].sum()
    accesos_prepago = df_t2_2024['total_accesos_prepago'].sum()

    # Crear el gráfico de torta
    fig = px.pie(
        values=[accesos_pospago, accesos_prepago],
        names=['Pospago', 'Prepago'],
        title='Distribución de Accesos Pospago y Prepago (2024 T1 y T2)',
        color_discrete_sequence=['#1E90FF', '#87CEEB']
    )

    # Configuración del gráfico
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        hole=0.3  # Gráfico de dona
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)


# CUARTO GRÁFICO: Tarjetas de métricas para accesos pospago
def mostrar_tarjetas_accesos_pospago(df):
    """
    Muestra tarjetas de métricas que indican el progreso hacia el 5% de aumento en los accesos pospago.

    Parámetros:
    - df (DataFrame): DataFrame con la columna 'total_accesos_pospago' y el último valor disponible de accesos.
    """
    # Filtrar los datos recientes de accesos pospago
    df_pospago_reciente = df[df['anio'] >= 2023]

    # Obtener los accesos pospago actuales (último trimestre disponible)
    accesos_pospago_actuales = df_pospago_reciente['total_accesos_pospago'].iloc[-1]
    
    # Calcular la proyección de aumento del 5%
    proyeccion_5p = accesos_pospago_actuales * 1.05
    delta_proyeccion = proyeccion_5p - accesos_pospago_actuales

    # Crear columnas para mostrar las métricas
    col1, col2 = st.columns(2)

    # Tarjeta 1: Accesos Pospago Actuales (Último trimestre disponible)
    col1.metric(
        label="Accesos Pospago Actuales",
        value=f"{accesos_pospago_actuales:,.0f}",
        delta=f"+{accesos_pospago_actuales:,.0f}",
        delta_color="normal"
    )

    # Tarjeta 2: Proyección del 5% de Aumento
    col2.metric(
        label="Proyección Pospago (+5%)",
        value=f"{proyeccion_5p:,.0f}",
        delta=f"+{delta_proyeccion:,.0f}",
        delta_color="inverse"
    )

