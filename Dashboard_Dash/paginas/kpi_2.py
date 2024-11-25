import dash_bootstrap_components as dbc
from dash import dcc, html
from data_loader import cargar_datos_cobertura_fibra
from visualization import graficar_porcentaje_localidades_fibra, graficar_cobertura_fibra_optica_proyectada, graficar_cobertura_fibra_optica

# Carga de datos
df_cobertura = cargar_datos_cobertura_fibra()

# Ruta al archivo GeoJSONa
geojson_path = 'assets/argentina_nivel_1_normalizado.geojson'

# Generar los gráficos
df_porcentaje = graficar_porcentaje_localidades_fibra(df_cobertura)
df_proyeccion = graficar_cobertura_fibra_optica_proyectada(df_cobertura)
df_mapa = graficar_cobertura_fibra_optica(geojson_path)

# Layout
def layout():
    return html.Div([
        # Contenedor principal con dos columnas (izquierda y derecha)
        html.Div([
            # Columna izquierda: el gráfico de barras horizontales
            html.Div([
                dcc.Graph(
                    id='porcentaje-localidades-fibra',
                    figure=df_porcentaje,  # Asegúrate de pasar df
                    style={"height": "100%"}
                )
            ], className="bar2-graph-container", style={"width": "45%", "display": "flex", "flexDirection": "column"}),  # 55% de ancho para la columna izquierda

            # Columna derecha: dividida en dos partes, un gráfico arriba y otro abajo
            html.Div([
                # Gráfico en la parte superior
                html.Div([
                    dcc.Graph(
                        id='grafico-superior',
                        figure=df_proyeccion,  # Gráfico superior
                        style={"height": "100%"}
                    )
                ], className="bar3-graph-container", style={"height": "45%"}),  # La mitad superior de la columna derecha

                # Gráfico en la parte inferior
                html.Div([
                    dcc.Graph(
                        id='grafico-inferior',
                        figure=df_mapa,  # Gráfico inferior aquí
                        style={"height": "100%"}
                    )
                ], className="map3-graph-container", style={"height": "45%"}),  # La mitad inferior de la columna derecha
            ], style={"width": "55%", "display": "flex", "flexDirection": "column"}),  # 45% de ancho para la columna derecha

        ], style={"display": "flex", "gap": "20px", "width": "100%", "height": "100vh"})  # Usamos "height": "100vh" para que ocupe todo el alto de la pantalla
    ], style={"background-color": "#09090e", "padding": "20px"})
