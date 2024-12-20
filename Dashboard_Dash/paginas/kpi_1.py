import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from data_loader import load_internet_penetration_data
from visualization import (
    graficar_penetracion_internet_dash,
    graficar_comparativa_acceso_proyectado_dash,
    graficar_evolucion_penetracion_provincia_dash,
    graficar_mapa_penetracion_dash
)

# Cargar los datos
df_penetracion = load_internet_penetration_data()

# Ruta al archivo GeoJSONa
geojson_path = 'assets/argentina_nivel_1_normalizado.geojson'

# Generar los gráficos iniciales
fig_penetracion_internet = graficar_penetracion_internet_dash(df_penetracion)
fig_comparativa_acceso_proyectado = graficar_comparativa_acceso_proyectado_dash(df_penetracion)
provincia_inicial = df_penetracion['nombre_provincia'].unique()[0]  # Provincia predeterminada
fig_lineas = graficar_evolucion_penetracion_provincia_dash(df_penetracion, provincia_inicial)
fig_mapa = graficar_mapa_penetracion_dash(geojson_path)

# Lista de provincias para el dropdown
provincias = df_penetracion['nombre_provincia'].unique()

# Layout
def layout():
    return html.Div([
        # Fila para el gráfico de barras (ocupa el ancho completo)
        html.Div([
            html.Button("Cambiar gráfico", id="cambiar-grafico-btn", className="btn-cambiar-grafico"),
            dcc.Graph(id="grafico-barras", figure=fig_penetracion_internet)
        ], className="graph-container", style={"width": "100%"}),  # Forzamos el ancho completo

        # Contenedor de la fila inferior con gráficos alineados
        html.Div([
            # Contenedor del gráfico de líneas con título y dropdown alineados
            html.Div([
                html.Div([
                    html.H4("Evolución de la Penetración de Internet por Provincia", className="graph-title"),
                    dcc.Dropdown(
                        id="dropdown-provincia",
                        options=[{"label": prov.capitalize(), "value": prov} for prov in provincias],
                        value=provincia_inicial,
                        placeholder="Selecciona una provincia",
                        clearable=False,
                        className="dropdown-button"
                    )
                ], className="graph-header"),  # Usamos graph-header para alinear título y dropdown
                dcc.Graph(id="grafico-lineas", figure=fig_lineas, style={'height': '200px'})
            ], className="line-graph-container", style={"flex": "1"}),

            # Contenedor del gráfico de mapa
            html.Div([
                dcc.Graph(id="grafico-mapa", figure=fig_mapa, style={'height': '294px'})
            ], className="line-graph-container", style={"flex": "1"})
            
        ], style={"display": "flex", "gap": "20px", "width": "100%"})  # Ancho completo para la fila inferior
    ], style={"background-color": "#09090e", "padding": "20px"})






# Callback para cambiar el gráfico de barras al presionar el botón
@callback(
    Output("grafico-barras", "figure"),
    Input("cambiar-grafico-btn", "n_clicks"),
    prevent_initial_call=True
)
def actualizar_grafico_barras(n_clicks):
    if n_clicks % 2 == 1:
        return fig_comparativa_acceso_proyectado
    else:
        return fig_penetracion_internet

# Callback para actualizar el gráfico de líneas basado en la provincia seleccionada
@callback(
    Output("grafico-lineas", "figure"),
    Input("dropdown-provincia", "value")
)
def actualizar_grafico_lineas(provincia):
    return graficar_evolucion_penetracion_provincia_dash(df_penetracion, provincia)
