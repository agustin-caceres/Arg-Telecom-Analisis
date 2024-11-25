import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from data_loader import cargar_datos_accesos_movil
from visualization import graficar_evolucion_accesos_pospago, graficar_proyeccion_accesos_pospago, graficar_distribucion_accesos

# Carga de los datos
df_accesos_movil = cargar_datos_accesos_movil()

# Generar los gráficos iniciales
fig_evolucion_accesos = graficar_evolucion_accesos_pospago(df_accesos_movil)
fig_proyeccion = graficar_proyeccion_accesos_pospago(df_accesos_movil)
fig_torta = graficar_distribucion_accesos(df_accesos_movil)


# Layout principal
def layout():
    return html.Div([
        # Gráfico principal de barras horizontales (mitad superior)
        html.Div([
            dcc.Graph(
                id='evolucion-accesos-pospago',
                figure=fig_evolucion_accesos
            )
        ], className="bar-graph-container", style={"width": "100%", "border-radius": "4px", "height": "50vh"}),

        # Contenedor de gráficos en la mitad inferior
        html.Div([
            # Gráfico de líneas (izquierda)
            html.Div([
                dcc.Graph(
                    id="grafico-lineas",
                    figure=fig_proyeccion,
                    style={"height": "100%"}
                )
            ], className="line-graph-kpi3-container", style={"flex": "1"}),  # Ocupa la mitad izquierda

            # Gráfico de torta (derecha)
            html.Div([
                dcc.Graph(
                    id="grafico-torta",
                    figure=fig_torta,  # Aquí debes pasar tu figura de gráfico de torta
                    style={"height": "100%"}
                )
            ], className="line-graph-kpi3-container", style={"flex": "1"})  # Ocupa la mitad derecha
        ], style={"display": "flex", "gap": "20px", "height": "50vh"})  # Distribución en la mitad inferior
    ], style={"background-color": "#09090e", "padding": "20px"})





