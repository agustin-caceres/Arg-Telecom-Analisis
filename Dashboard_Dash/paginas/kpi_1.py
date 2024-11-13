import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from data_loader import load_internet_penetration_data
from visualization import (
    graficar_penetracion_internet_dash,
    graficar_comparativa_acceso_proyectado_dash
)

# Cargar los datos
df_penetracion = load_internet_penetration_data()

# Generar los gráficos
fig_penetracion_internet = graficar_penetracion_internet_dash(df_penetracion)
fig_comparativa_acceso_proyectado = graficar_comparativa_acceso_proyectado_dash(df_penetracion)

# Layout de la página
def layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Button("Cambiar gráfico", id="cambiar-grafico-btn", className="btn-cambiar-grafico"),
                    dcc.Graph(id="grafico-barras", figure=fig_penetracion_internet)
                ], className="graph-container")  # Contenedor de la tarjeta
            ], width=12)
        ], style={"padding": "20px"}),

    ], fluid=True, style={"background-color": "#1e1e2f"})

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
