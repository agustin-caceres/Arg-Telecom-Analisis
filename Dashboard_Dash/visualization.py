import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import json
from dash import dcc

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
            height=235,
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