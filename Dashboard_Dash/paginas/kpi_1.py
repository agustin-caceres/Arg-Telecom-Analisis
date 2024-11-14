import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from data_loader import load_internet_penetration_data
from visualization import (
    graficar_penetracion_internet_dash,
    graficar_comparativa_acceso_proyectado_dash,
    graficar_evolucion_penetracion_provincia_dash
)

# Cargar los datos
df_penetracion = load_internet_penetration_data()

# Generar los gráficos iniciales
fig_penetracion_internet = graficar_penetracion_internet_dash(df_penetracion)
fig_comparativa_acceso_proyectado = graficar_comparativa_acceso_proyectado_dash(df_penetracion)
provincia_inicial = df_penetracion['nombre_provincia'].unique()[0]  # Provincia predeterminada
fig_lineas = graficar_evolucion_penetracion_provincia_dash(df_penetracion, provincia_inicial)

# Lista de provincias para el dropdown
provincias = df_penetracion['nombre_provincia'].unique()

# Layout de la página
def layout():
    return dbc.Container([
        # Fila para los gráficos de barras
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Button("Cambiar gráfico", id="cambiar-grafico-btn", className="btn-cambiar-grafico"),
                    dcc.Graph(id="grafico-barras", figure=fig_penetracion_internet)
                ], className="graph-container")
            ], width=12)
        ], style={"padding": "20px"}),

        # Fila para el gráfico de líneas con título y dropdown alineados
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.H4("Evolución de la Penetración de Internet por Provincia", className="graph-title"),
                        dcc.Dropdown(
                            id="dropdown-provincia",
                            options=[{"label": prov.capitalize(), "value": prov} for prov in provincias],
                            value=provincias[0],
                            placeholder="Selecciona una provincia",
                            className="dropdown-button",
                            clearable=False
                        )
                    ], className="graph-header"),  # Usamos graph-header aquí
                    dcc.Graph(id="grafico-lineas", figure=fig_lineas)
                ], className="line-graph-container")
            ], width=6)
        ], style={"padding": "20px"}),

    ], fluid=True, style={"background-color": "#09090e"})


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
