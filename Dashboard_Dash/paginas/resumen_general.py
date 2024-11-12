import dash
from dash import html

# layout de la página de resumen general
def layout():
    return html.Div([  # El contenido que ya tenías en app.py
        # Presentación en la parte superior
        html.Div([
            html.H2("Análisis de Conectividad en Argentina", style={"text-align": "center", "margin-bottom": "10px"}),
            html.P(
                "Este dashboard presenta un análisis sobre el sector de telecomunicaciones en Argentina. "
                "A continuación, encontrarás un resumen de los principales KPIs que miden el progreso en el acceso a internet, "
                "la cobertura de tecnologías avanzadas y el crecimiento de líneas pospago.",
                style={"text-align": "center", "margin-bottom": "30px"}
            ),
        ]),

        # Contenedor para centrar las tarjetas
        html.Div([
            # Tarjeta KPI 1 - Acceso a Internet
            html.Div([
                html.Div([
                    html.Img(src="/assets/wifi-router.png", className="card-icon-small"),
                    html.H3("Acceso a Internet", className="card-title"),
                    html.H1("2%"),  # Valor de ejemplo
                    html.P("Proyección trimestral"),
                    html.Img(src="/assets/wifi-router.png", className="card-icon"),
                    html.Div([html.Div(className="progress-slider")], className="progress-bar")
                ], className="card card-acceso-internet", id='card-acceso-internet')
            ], style={"flex": "1", "margin": "10px"}),

            # Tarjeta KPI 2 - Cobertura de Fibra Óptica
            html.Div([
                html.Div([
                    html.Img(src="/assets/Infraestructure.png", className="card-icon-small"),
                    html.H3("Cobertura de Fibra Óptica", className="card-title"),
                    html.H1("10%"),  # Valor de ejemplo
                    html.P("Proyección trimestral"),
                    html.Img(src="/assets/Infraestructure.png", className="card-icon"),
                    html.Div([html.Div(className="progress-slider")], className="progress-bar")
                ], className="card card-cobertura-fibra", id='card-cobertura-fibra')
            ], style={"flex": "1", "margin": "10px"}),

            # Tarjeta KPI 3 - Aumento en Planes Pospago
            html.Div([
                html.Div([
                    html.Img(src="/assets/mobile.png", className="card-icon-small"),
                    html.H3("Aumento en Planes Pospago", className="card-title"),
                    html.H1("5%"),  # Valor de ejemplo
                    html.P("Proyección trimestral"),
                    html.Img(src="/assets/mobile.png", className="card-icon"),
                    html.Div([html.Div(className="progress-slider")], className="progress-bar")
                ], className="card card-planes-pospago", id='card-planes-pospago')
            ], style={"flex": "1", "margin": "10px"}),
        ], style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"})
    ])
