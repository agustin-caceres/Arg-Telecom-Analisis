import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from dash import dcc
import dash_leaflet as dl


# -- GRÁFICOS PARA KPI 1: ACCESO A INTERNET --

# PRIMER GRÁFICO: Penetración de Internet por cada 100 hogares
def graficar_penetracion_internet_dash(df_penetracion):
    """
    Genera un gráfico de barras agrupadas interactivo que muestra la penetración de internet 
    por cada 100 hogares en diferentes provincias y trimestres para Dash.

    Parámetros:
    - df_penetracion (DataFrame): DataFrame con las columnas 'nombre_provincia', 
                                  'anio', 'trimestre', y 'accesos_por_100_hogares'.

    Retorno:
    - fig: Gráfico interactivo en formato Plotly para ser integrado en Dash.
    """
    color_palette = ["#00B7C2", "#1B262C", "#3FC5F0", "#0F4C75", "#05DFD7"]

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
    fig = px.bar(
        df_penetracion_reciente, 
        x='nombre_provincia', 
        y='accesos_por_100_hogares', 
        color='anio_trimestre', 
        color_discrete_sequence=color_palette,
        title='Penetración de Internet por cada 100 Hogares (2023 en adelante)',
        labels={'accesos_por_100_hogares': 'Accesos por 100 Hogares', 'nombre_provincia': 'Provincia'},
        hover_data=['anio', 'trimestre'],
        barmode='group'
    )

    # Personalización del gráfico para el estilo oscuro
    fig.update_layout(
        xaxis_title='Provincia',  # Etiqueta del eje X
        yaxis_title='Accesos por 100 Hogares',  # Etiqueta del eje Y
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),  # Título en negrita
        legend_title_text='',  # Quita el título de la leyenda
        xaxis_tickangle=-30,  # Gira los nombres de las provincias en el eje X para mejor visibilidad
        yaxis_range=[0, df_penetracion_reciente['accesos_por_100_hogares'].max() + 10],  # Ajusta el rango del eje Y
        template="plotly_dark",  # Aplica el tema oscuro
        plot_bgcolor="#09090e",  # Fondo del gráfico
        paper_bgcolor="#09090e",  # Fondo del "papel" donde se dibuja el gráfico
        title_font_size=15,  # Tamaño de la fuente del título
        height=300,  # Limita la altura del gráfico para que se ajuste mejor al contenedor
        margin=dict(l=10, r=10, t=30, b=30),  # Reduce los márgenes para centrar el contenido en el contenedor
        
        # Ubicación de la leyenda dentro del gráfico (superior derecha)
        legend=dict(
            orientation="h",  # Orientación horizontal de la leyenda
            x=1,  # Posición horizontal de la leyenda
            y=1.2,  # Posición vertical de la leyenda, ajustada fuera del gráfico
            xanchor='right',  # Alinea la leyenda a la derecha
            yanchor='top',  # Alinea la leyenda en la parte superior
            bgcolor="rgba(0,0,0,0.1)",  # Fondo semitransparente de la leyenda
            bordercolor="rgba(255,255,255,0.1)",  # Borde semitransparente de la leyenda
            borderwidth=1  # Ancho del borde de la leyenda
        )
    )
    fig.update_traces(marker_line_width=0.5)  # Ajusta el ancho del borde de las barras para mejor visibilidad

    return fig


# SEGUNDO GRÁFICO: Comparativa de acceso actual vs. proyectado
def graficar_comparativa_acceso_proyectado_dash(df_penetracion):
    """
    Genera un gráfico de barras agrupadas interactivo que muestra la comparativa de acceso a internet
    por cada 100 hogares en las provincias de Argentina, comparando el acceso actual con la proyección
    de un 2% de aumento para el próximo trimestre.

    Parámetros:
    - df_penetracion (DataFrame): DataFrame con las columnas 'nombre_provincia', 'anio_trimestre',
                                  'accesos_por_100_hogares', y otros datos necesarios.

    Retorno:
    - fig: Gráfico interactivo en formato Plotly para ser integrado en Dash.
    """

    color_palette = ["#00B7C2", "#0F4C75"]

    # Filtrar los datos a partir de 2023 y crear columna 'anio_trimestre'
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
    fig = px.bar(
        df_kpi_melted, 
        x='nombre_provincia', 
        y='Cantidad', 
        color='Acceso',
        color_discrete_sequence=color_palette,
        title='Comparativa de Acceso a Internet por 100 Hogares: Actual vs. Proyectado (2% Aumento)',
        labels={'Cantidad': 'Accesos por 100 Hogares', 'nombre_provincia': 'Provincia'},
        barmode='group',
        hover_data=['Acceso']
    )

    # Personalización del gráfico para el estilo oscuro
    fig.update_layout(
        xaxis_title='Provincia',  # Etiqueta del eje X
        yaxis_title='Accesos por 100 Hogares',  # Etiqueta del eje Y
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),  # Título en negrita
        legend_title_text='',  # Quita el título de la leyenda
        xaxis_tickangle=-30,  # Gira los nombres de las provincias en el eje X para mejor visibilidad
        yaxis_range=[0, df_kpi_melted['Cantidad'].max() + 10],  # Ajusta el rango del eje Y
        template="plotly_dark",  # Aplica el tema oscuro
        plot_bgcolor="#09090e",  # Fondo del gráfico
        paper_bgcolor="#09090e",  # Fondo del "papel" donde se dibuja el gráfico
        title_font_size=15,  # Tamaño de la fuente del título
        height=300,  # Limita la altura del gráfico para que se ajuste mejor al contenedor
        margin=dict(l=10, r=10, t=30, b=30),  # Reduce los márgenes para centrar el contenido en el contenedor
        
        # Ubicación de la leyenda dentro del gráfico (superior derecha)
        legend=dict(
            x=1,  # Posición horizontal de la leyenda
            y=1.2,  # Posición vertical de la leyenda, ajustada fuera del gráfico
            xanchor='right',  # Alinea la leyenda a la derecha
            yanchor='top',  # Alinea la leyenda en la parte superior
            bgcolor="rgba(0,0,0,0.1)",  # Fondo semitransparente de la leyenda
            bordercolor="rgba(255,255,255,0.1)",  # Borde semitransparente de la leyenda
            borderwidth=1  # Ancho del borde de la leyenda
        )
    )
    fig.update_traces(marker_line_width=0.5)  # Ajusta el ancho del borde de las barras para mejor visibilidad

    return fig


# TERCER GRÁFICO: Evolución de la penetración de internet por provincia
def graficar_evolucion_penetracion_provincia_dash(df_penetracion, provincia):

    """
    Genera un gráfico de líneas que muestra la evolución de la penetración de internet 
    por cada 100 hogares en una provincia seleccionada, incluyendo una proyección con un 
    aumento del 2% en el último trimestre disponible para Dash.

    Parámetros:
    - df_penetracion (DataFrame): DataFrame con las columnas 'nombre_provincia', 'anio_trimestre', 
                                  y 'accesos_por_100_hogares'.
    - provincia (str): Nombre de la provincia seleccionada.

    Retorno:
    - fig: Gráfico en formato Plotly para ser integrado en Dash.
    """
    # Filtrar datos a partir de 2023 y crear columna 'anio_trimestre'
    df_penetracion_reciente = df_penetracion[df_penetracion['anio'] >= 2023].copy()
    df_penetracion_reciente['anio_trimestre'] = df_penetracion_reciente['anio'].astype(str) + ' T' + df_penetracion_reciente['trimestre'].astype(str)

    # Filtrar los datos por la provincia seleccionada
    df_provincia_filtrada = df_penetracion_reciente[df_penetracion_reciente['nombre_provincia'] == provincia]

    # Ordenar por año y trimestre para asegurar el orden cronológico
    df_provincia_filtrada = df_provincia_filtrada.sort_values(by=['anio', 'trimestre'])

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
        df_completo = pd.concat([df_provincia_filtrada, df_proyeccion]).sort_values(by=['anio', 'trimestre'])

        # Crear la figura del gráfico
        fig = go.Figure()

        # Agregar la línea principal (sin el punto de proyección)
        fig.add_trace(go.Scatter(
            x=df_completo['anio_trimestre'][:-1],
            y=df_completo['accesos_por_100_hogares'][:-1],
            mode='lines+markers',
            line=dict(color='#00B7C2', width=2),  # Color y grosor de la línea principal
            name='Acceso Histórico'
        ))

        # Agregar el último punto de proyección con color diferente
        fig.add_trace(go.Scatter(
            x=df_completo['anio_trimestre'][-2:],  # Solo el último punto
            y=df_completo['accesos_por_100_hogares'][-2:],
            mode='lines+markers',
            line=dict(color='#FCF876', width=2, dash='dash'),  # Línea punteada para la proyección
            marker=dict(color='#FCF876', size=6),  # Color y tamaño del marcador de proyección
            name='Proyección'
        ))

        # Personalización del gráfico para el estilo oscuro
        fig.update_layout(
            xaxis_title='Año y Trimestre',
            yaxis_title='Accesos por 100 Hogares',
            xaxis_tickangle=-15,
            template="plotly_dark",
            plot_bgcolor="#09090e",
            paper_bgcolor="#09090e",
            title_font_size=1,
            height=225,
            margin=dict(l=10, r=10, t=30, b=30),
            showlegend=False  # Oculta la leyenda
        )

        # Añadir anotación en el punto proyectado
        fig.add_annotation(
            x='2024 T2',
            y=acceso_proyectado,
            text="Proyección",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(color="lightgrey")
        )

    return fig


# CUARTO GRÁFICO: Mapa de coropletas con la penetración de internet por provincia
def graficar_mapa_penetracion_dash(geojson_path):
    """
    Genera un mapa de coropletas interactivo que muestra la penetración de internet
    por cada 100 hogares en cada provincia de Argentina.
    """
    color_palette = ["#00B7C2", "#1B262C", "#3FC5F0", "#0F4C75", "#05DFD7"]
    color_palette_invertida = color_palette[::-1]  # Invertir la lista de colores

    data = {
        'nombre_provincia': [
            'tierra del fuego', 'santa cruz', 'chubut', 'rio negro', 'neuquen', 'la pampa', 'buenos aires', 
            'mendoza', 'san luis', 'cordoba', 'santa fe', 'entre rios', 'la rioja', 'san juan', 'corrientes', 
            'misiones', 'santiago del estero', 'catamarca', 'tucuman', 'salta', 'jujuy', 'chaco', 'formosa', 'caba'
        ],
        'accesos_por_100_hogares': [
            109.78, 67.58, 84.89, 71.14, 79.50, 100.49, 81.10, 52.59, 102.70, 90.70, 80.40, 69.31, 80.03, 51.62, 51.94, 
            56.76, 49.41, 68.82, 60.48, 56.30, 57.65, 46.70, 39.61, 119.53
        ]
    }


    # Convertir los datos en un DataFrame
    df = pd.DataFrame(data)

    # Cargar el archivo GeoJSON
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    
    # Crear el gráfico
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_data,
        locations='nombre_provincia',  # Columna de mapeo en el DataFrame
        featureidkey="properties.NAME_1",  # Columna de mapeo en el GeoJSON
        color='accesos_por_100_hogares',  # Variable a visualizar
        color_continuous_scale=color_palette_invertida,  # Escala de color
        range_color=(df['accesos_por_100_hogares'].min(),
                     df['accesos_por_100_hogares'].max()),
        mapbox_style="carto-darkmatter",  # Estilo de mapa oscuro
        zoom=4,
        center={"lat": -38.4161, "lon": -63.6167},  # Coordenadas de Argentina
        title="Penetración de Internet por Provincia"
    )

    # Ajustar layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="#000000",  # Fondo de la figura
        plot_bgcolor="#000000",  # Fondo del gráfico
        font=dict(color="white"),  # Color del texto
        height=300,
        title=dict(
            text="",
            font=dict(size=20),
            x=0.5,  # Centrar título
            xanchor="center",
        ),
        coloraxis_colorbar={
            'title': 'Accesos (%)',
            'tickvals': [0, 25, 50, 75, 100],
            'ticktext': ['0%', '25%', '50%', '75%', '100%'],
            'orientation': 'h',  # Orientación horizontal
            'yanchor': 'middle',  # Coloca la barra arriba
            'xanchor': 'center',  # Centrado
            'tickfont': {"color": "white", "size": 10},  # Tamaño de los ticks más pequeños
            'titlefont': {"color": "white", "size": 12},  # Título de la barra más pequeño
            'thickness': 5,  # Grosor de la barra
            'len': 0.7,  # Longitud de la barra (70% de la longitud total)
            'bgcolor': 'rgba(0, 0, 0, 0)',  # Fondo transparente
        },
        hoverlabel=dict(
            bgcolor="rgba(0, 0, 0, 1)",  # Fondo del tooltip
            font_size=12,  # Tamaño de la fuente
            font_color="white",  # Color del texto
        )
    )

    return fig




# -- GRÁFICOS PARA KPI 2: COBERTURA DE FIBRA ÓPTICA --


# PRIMER GRÁFICO: Porcentaje de localidades con fibra óptica por provincia
def graficar_porcentaje_localidades_fibra(df_cobertura):
    """
    Genera un gráfico de barras horizontales que muestra el porcentaje de localidades con fibra óptica por provincia.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'nombre_provincia', 'localidad', y 'fibra_optica'.

    Retorno:
    - fig: Gráfico generado con Plotly.
    """

    # Definir la paleta de colores
    color_palette = ["#FBB454", "#FF7777", "#FF9551"]

    # Calcular el porcentaje de localidades con fibra óptica
    df_fibra_optica = df_cobertura[df_cobertura['fibra_optica'] == True]
    total_localidades_provincia = df_cobertura.groupby('nombre_provincia')['localidad'].count()
    localidades_fibra_provincia = df_fibra_optica.groupby('nombre_provincia')['localidad'].count()

    porcentaje_fibra_optica = (localidades_fibra_provincia / total_localidades_provincia) * 100
    porcentaje_fibra_optica = porcentaje_fibra_optica.sort_values()

    # Crear gráfico de barras horizontales
    fig = px.bar(
        porcentaje_fibra_optica,
        x=porcentaje_fibra_optica.values,
        y=porcentaje_fibra_optica.index,
        labels={'x': 'Porcentaje de Localidades con Fibra Óptica', 'y': 'Provincia'},
        title='Porcentaje de Localidades con Fibra Óptica por Provincia',
        text=porcentaje_fibra_optica.values,
        orientation='h',  # Barras horizontales
        color=porcentaje_fibra_optica.values,  # Asignar color gradual según el porcentaje
        color_continuous_scale=color_palette  
    )
    # Actualizar el gráfico para ajustar la altura, márgenes, rotación de etiquetas y posición del texto dentro de las barras
    fig.update_traces(
        texttemplate='%{text:.2f}%',   # Muestra los valores de porcentaje dentro de las barras con 2 decimales
        textposition='inside',         # Coloca los nombres dentro de las barras
        insidetextanchor='middle'       # Alinea el texto al principio de las barras
    )

    # Configuración del gráfico
    fig.update_layout(
        title_x=0.5,  # Centrar el título
        title_y=0.97,  # Ajustar el título verticalmente
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),
        xaxis_title='Porcentaje de Localidades con Fibra Óptica',
        yaxis_title='Provincia',
        template="plotly_dark",  # Tema oscuro
        plot_bgcolor="#09090e",  # Fondo del gráfico
        paper_bgcolor="#09090e",  # Fondo del "papel" donde se dibuja el gráfico
        height=620,  # Limitar la altura del gráfico para que se ajuste mejor
        margin=dict(l=40, r=40, t=40, b=40)  # Márgenes del gráfico
    )

    return fig


# SEGUNDO GRÁFICO: Cobertura de fibra óptica actual vs. proyectada
def graficar_cobertura_fibra_optica_proyectada(df_cobertura):
    """
    Genera un gráfico de barras que muestra la cobertura de fibra óptica actual vs. proyectada
    en provincias con menor cobertura.

    Parámetros:
    - df (DataFrame): DataFrame que contiene las columnas 'nombre_provincia' y 'fibra_optica'.
    """

    # Filtrar provincias con menor cobertura (por debajo del 25% del total)
    prov_menor_cobertura_fibra = df_cobertura.groupby('nombre_provincia')['fibra_optica'].mean()
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

    # Crear el gráfico de barras agrupadas
    fig = px.bar(
        df_fibra_optica_melted,
        x='Provincia', 
        y='Porcentaje', 
        color='Cobertura',
        barmode='group',
        text='Porcentaje',
        title='Cobertura de Fibra Óptica Actual vs. Proyectada (30% Aumento)',
        labels={'Provincia': 'Provincia', 'Porcentaje': 'Cobertura (%)'},
        color_discrete_map={
            'Cobertura Actual': '#fff590',  
            'Cobertura Proyectada': '#ff9551' 
        }
    )

    # Ajustes visuales para mejorar la legibilidad
    fig.update_traces(
        texttemplate='%{text:.2f}%',  # Mostrar los porcentajes con 2 decimales
        textposition='outside',       # Colocar el texto fuera de las barras
        insidetextanchor='middle'     # Centrar el texto dentro de las barras (si se usa "inside")
    )
    
    # Mejorar la presentación visual
    fig.update_layout(
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),
        xaxis_tickangle=0,  # Rotar las etiquetas del eje X para mejor visualización
        template="plotly_dark",  # Tema oscuro
        plot_bgcolor="#09090e",  # Fondo del gráfico
        paper_bgcolor="#09090e",  # Fondo del "papel" donde se dibuja el gráfico
        height=300,          # Ajustar la altura del gráfico
        margin=dict(l=40, r=40, t=30, b=5),  # Márgenes para evitar que se corten las etiquetas
        title={'x': 0.5, 'xanchor': 'center'},  # Centrar el título
        showlegend=False,  # Oculta la leyenda
    )

    return fig


# TERCER GRÁFICO: Mapa Interactivo de Provincias
def graficar_cobertura_fibra_optica(geojson_path):
    """
    Genera un gráfico de mapa coroplético que muestra la cobertura de fibra óptica por provincia con tema oscuro.

    Args:
        geojson_path (str): Ruta al archivo GeoJSON con la geometría de las provincias.

    Returns:
        plotly.graph_objs.Figure: Figura del gráfico generada.
    """
    color_palette = ["#fff590", "#f59e44", "#ff7876"]

    # Datos de cobertura de fibra óptica por provincia obtenidos de Streamlit directamente.
    datos = {
        'nombre_provincia': [
            'tierra del fuego', 'santa cruz', 'chubut', 'rio negro', 'neuquen', 'la pampa', 'buenos aires', 
            'mendoza', 'san luis', 'cordoba', 'santa fe', 'entre rios', 'la rioja', 'san juan', 'corrientes', 
            'misiones', 'santiago del estero', 'catamarca', 'tucuman', 'salta', 'jujuy', 'chaco', 'formosa', 'caba'
        ],
        'fibra_optica': [
            100, 93.33, 39.39, 70.15, 46.67, 66.67, 71.95, 48.00, 40.66, 52.62, 49.50, 40.94, 51.79, 18.06, 45.65, 
            53.42, 64.04, 60.42, 37.29, 79.44, 65.75, 77.05, 27.12, 100
        ]
    }

    # Convertir los datos en un DataFrame
    df = pd.DataFrame(datos)

    # Cargar el archivo GeoJSON
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Crear el gráfico
    fig = px.choropleth_mapbox(
        df,
        geojson=geojson_data,
        locations='nombre_provincia',  # Columna de mapeo en el DataFrame
        featureidkey="properties.NAME_1",  # Columna de mapeo en el GeoJSON
        color='fibra_optica',  # Variable a visualizar
        color_continuous_scale=color_palette,  # Escala de color
        range_color=(0, 100),  # Rango de valores
        mapbox_style="carto-darkmatter",
        zoom=4,
        center={"lat": -38.4161, "lon": -63.6167},  # Coordenadas de Argentina
        title="Cobertura de Fibra Óptica por Provincia",
        hover_name='nombre_provincia',  # Añadir el nombre de la provincia al tooltip
        hover_data={"fibra_optica": True},  # Mostrar el valor de fibra_optica en el tooltip
    )

    # Crear un hovertemplate dinámico con el color de la provincia
    hovertemplate = (
        "<b>%{hovertext}</b><br>"  # Mostrar nombre de la provincia
        "Cobertura de Fibra Óptica: %{customdata[0]}%<br>"  # Mostrar porcentaje de cobertura
    )

    # Asignar el hovertemplate dinámico
    fig.update_traces(hovertemplate=hovertemplate)

    # Ajustar layout
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="#000000",  # Fondo de la figura
        plot_bgcolor="#000000",  # Fondo del gráfico
        font=dict(color="white"),  # Color del texto
        height=300,
        title=dict(
            text="",
            font=dict(size=20),
            x=0.5,  # Centrar título
            xanchor="center",
        ),
        coloraxis_colorbar={
            'title': 'Cobertura (%)',
            'tickvals': [0, 25, 50, 75, 100],
            'ticktext': ['0%', '25%', '50%', '75%', '100%'],
            'orientation': 'h',  # Orientación horizontal
            'yanchor': 'middle',  # Coloca la barra arriba
            'xanchor': 'center',  # Centrado
            'tickfont': {"color": "white", "size": 10},  # Tamaño de los ticks más pequeños
            'titlefont': {"color": "white", "size": 12},  # Título de la barra más pequeño
            'thickness': 5,  # Grosor de la barra
            'len': 0.7,  # Longitud de la barra (70% de la longitud total)
            'bgcolor': 'rgba(0, 0, 0, 0)',  # Fondo transparente
        },
        hoverlabel=dict(
            bgcolor="rgba(0, 0, 0, 1)",  # Fondo del tooltip
            font_size=12,  # Tamaño de la fuente
            font_color="white",  # Color del texto
        )
    )

    return fig





# -- GRÁFICOS PARA KPI 3: AUMENTO EN PLANES POSPAGO --


# PRIMER GRÁFICO: Evolución trimestral de accesos a líneas pospago
def graficar_evolucion_accesos_pospago(df_accesos_movil):
    """
    Genera un gráfico de barras horizontales que muestra la evolución trimestral de
    los accesos a líneas pospago a partir del año 2023.

    Parámetros:
    - df (DataFrame): DataFrame con las columnas 'anio', 'trimestre' y 'total_accesos_pospago'.

    Retorno:
    - fig: Gráfico generado con Plotly.
    """
    # Definir la paleta de colores
    color_palette = ["#BC7AF9", "#A084E8", "#8B5DFF", "#7E30E1", "#6a3382", "#D67BFF"]

    # Filtrar datos a partir de 2023
    df_pospago_reciente = df_accesos_movil[df_accesos_movil['anio'] >= 2023].copy()

    # Crear columna combinada para año y trimestre
    df_pospago_reciente['anio_trimestre'] = df_pospago_reciente['anio'].astype(str) + ' T' + df_pospago_reciente['trimestre'].astype(str)

    # Crear el gráfico de barras horizontales
    fig = px.bar(
        df_pospago_reciente, 
        x='total_accesos_pospago', 
        y='anio_trimestre', 
        orientation='h',
        title='Evolución Trimestral del Acceso a Líneas Pospago (2023 en adelante)',
        color='anio_trimestre',  # Usamos 'anio_trimestre' como la variable de color
        color_discrete_sequence=color_palette,  # Aplicamos la paleta de colores definida
    )

    # Ajustes del gráfico
    fig.update_layout(
        xaxis_title='Total de Accesos Pospago',
        yaxis_title='Año y Trimestre',
        title_font_size=15,
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),  # Título en negrita
        title_y=0.95,  # Posiciona el título un poco más abajo (ajusta este valor según lo necesites)
        legend_title_text='',  # Quita el título de la leyenda
        xaxis_tickformat=',',
        template="plotly_dark",  # Aplica el tema oscuro
        plot_bgcolor="#09090e",  # Fondo del gráfico
        paper_bgcolor="#09090e",  # Fondo del "papel" donde se dibuja el gráfico
        height=295,  # Limita la altura del gráfico para que se ajuste mejor al contenedor
        margin=dict(t=50, b=20, l=50, r=50),  # Márgenes automáticos para el margen superior e inferior,
        legend=dict(
            # x=1,  # Posición horizontal de la leyenda
            y=1.1,  # Posición vertical de la leyenda, ajustada fuera del gráfico
            xanchor='right',  # Alinea la leyenda a la derecha
            yanchor='top',  # Alinea la leyenda en la parte superior
            #bgcolor="rgba(0,0,0,0.1)",  # Fondo semitransparente de la leyenda
            #bordercolor="rgba(255,255,255,0.1)",  # Borde semitransparente de la leyenda
            #borderwidth=1  # Ancho del borde de la leyenda
        )
    )


    return fig


# SEGUNDO GRÁFICO: Proyección de aumento en accesos pospago
def graficar_proyeccion_accesos_pospago(df_accesos_movil):
    """
    Genera un gráfico de líneas que muestra la evolución histórica de accesos a planes pospago
    y una proyección de aumento del 5% para el tercer trimestre de 2024.
    
    Retorno:
    - fig: Gráfico generado con Plotly.
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
        line=dict(color='#A084E8', width=2),
        name='Datos Históricos'
        
    ))

    # Proyección
    fig.add_trace(go.Scatter(
        x=trimestres[-2:], 
        y=accesos_postpago[-2:], 
        mode='lines+markers', 
        line=dict(color='#fa60ff', width=2, dash='dash'),
        marker=dict(color='#fa60ff', size=6),  # Color y tamaño del marcador de proyección
        name='Proyección'
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
        title_font_size=15,
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),  # Título en negrita
        legend_title_text='Datos',
        showlegend=False,  # Oculta la leyenda
        template="plotly_dark",  # Aplica el tema oscuro
        plot_bgcolor="#09090e",  # Fondo del gráfico
        paper_bgcolor="#09090e",  # Fondo del "papel" donde se dibuja el gráfico
        height=300,  # Limita la altura del gráfico para que se ajuste mejor al contenedor
        margin=dict(l=10, r=10, t=30, b=30),
    )

    return fig


# TERCER GRÁFICO: Distribución de accesos pospago y prepago
def graficar_distribucion_accesos(df_accesos_movil):
    """
    Genera un gráfico de torta que muestra la distribución de accesos pospago y prepago
    para el primer y segundo trimestre de 2024.

    Parámetros:
    - df (DataFrame): DataFrame con las columnas 'anio', 'total_accesos_pospago' y 'total_accesos_prepago'.

    Retorno:
    - fig: Figura de Plotly lista para ser usada en Dash.
    """
    # Filtrar los datos para 2024 T1 y T2
    df_t2_2024 = df_accesos_movil[df_accesos_movil['anio'] == 2024]

    # Sumar los accesos pospago y prepago
    accesos_pospago = df_t2_2024['total_accesos_pospago'].sum()
    accesos_prepago = df_t2_2024['total_accesos_prepago'].sum()

    # Crear el gráfico de torta
    fig = px.pie(
        values=[accesos_pospago, accesos_prepago],
        names=['Pospago', 'Prepago'],
        title='Distribución de Accesos Pospago y Prepago (2024 T1 y T2)',
        color_discrete_sequence=['#a84ece', '#fa60ff'] #a84ece
    )

    # Configuración del gráfico
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        hole=0.3  # Gráfico de dona
    )

    # Ajustes adicionales al diseño
    fig.update_layout(
        title_font=dict(family='Roboto, sans-serif', size=15, color='white', weight='bold'),
        paper_bgcolor='#09090e',  # Fondo del "papel"
        plot_bgcolor='#09090e',  # Fondo del gráfico
        showlegend=True,  # Oculta la leyenda
        font=dict(color='white'),  # Color de fuente general
        margin=dict(t=50, b=20, l=20, r=20)  # Ajustar márgenes
        
    )

    return fig

