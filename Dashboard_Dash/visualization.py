import plotly.express as px

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
        title='Penetración de Internet por cada 100 Hogares (2023 en adelante)',
        labels={'accesos_por_100_hogares': 'Accesos por 100 Hogares', 'nombre_provincia': 'Provincia'},
        hover_data=['anio', 'trimestre'],
        barmode='group'
    )

    # Personalización del gráfico para el estilo oscuro
    fig.update_layout(
        xaxis_title='Provincia',
        yaxis_title='Accesos por 100 Hogares',
        legend_title_text='',
        xaxis_tickangle=-45,
        yaxis_range=[0, df_penetracion_reciente['accesos_por_100_hogares'].max() + 10],
        template="plotly_dark",
        plot_bgcolor="#1e1e2f",
        paper_bgcolor="#1e1e2f",
        title_font_size=18,
        margin=dict(l=20, r=20, t=40, b=20),
        
        # Ubicación de la leyenda dentro del gráfico (superior derecha)
        legend=dict(
            orientation="h",
            x=1, # Ajusta esto para mover la leyenda horizontalmente
            y=1.2, # Ajusta esto para mover la leyenda verticalmente
            xanchor='right',
            yanchor='top',
            bgcolor="rgba(0,0,0,0.1)",
            bordercolor="rgba(255,255,255,0.1)",
            borderwidth=1
        )
    )
    fig.update_traces(marker_line_width=0.5)

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
        title='Comparativa de Acceso a Internet por 100 Hogares: Actual vs. Proyectado (2% Aumento)',
        labels={'Cantidad': 'Accesos por 100 Hogares', 'nombre_provincia': 'Provincia'},
        barmode='group',
        hover_data=['Acceso']
    )

    # Personalización del gráfico para el estilo oscuro
    fig.update_layout(
        xaxis_title='Provincia',
        yaxis_title='Accesos por 100 Hogares',
        legend_title_text='',
        xaxis_tickangle=-45,
        yaxis_range=[0, df_kpi_melted['Cantidad'].max() + 10],
        template="plotly_dark",
        plot_bgcolor="#1e1e2f",
        paper_bgcolor="#1e1e2f",
        title_font_size=18,
        margin=dict(l=20, r=20, t=40, b=20),
        
        # Ubicación de la leyenda dentro del gráfico (superior derecha)
        legend=dict(
            x=1, # Ajusta esto para mover la leyenda horizontalmente
            y=1.2, # Ajusta esto para mover la leyenda verticalmente
            xanchor='right',
            yanchor='top',
            bgcolor="rgba(0,0,0,0.1)", # Fondo semitransparente para la leyenda
            bordercolor="rgba(255,255,255,0.1)", # Borde suave para que no distraiga
            borderwidth=1
        )
    )
    fig.update_traces(marker_line_width=0.5)

    return fig
