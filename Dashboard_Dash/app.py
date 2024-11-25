import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from paginas import resumen_general, kpi_1, kpi_2, kpi_3

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Definir la estructura básica
app.layout = html.Div([
    # Componente Location para manejar la URL activa
    dcc.Location(id='url', refresh=False),

    # Contenido principal de la página
    html.Div(id='page-content'),

    # Barra de navegación en la parte inferior
    html.Div([
        dcc.Link('Resumen', href='/', className='nav-link', id='link-resumen'),
        dcc.Link('Acceso a Internet', href='/acceso-a-internet', className='nav-link', id='link-acceso-internet'),
        dcc.Link('Cobertura de Fibra Óptica', href='/cobertura-fibra', className='nav-link', id='link-cobertura-fibra'),
        dcc.Link('Aumento en Planes Pospago', href='/planes-pospago', className='nav-link', id='link-planes-pospago'),
        dcc.Link('Conclusiones', href='/conclusiones', className='nav-link', id='link-conclusiones'),
    ], className='nav-bar-bottom')
])

# Lógica para actualizar el contenido según la URL activa
@app.callback(
    [Output('page-content', 'children'),
     Output('link-resumen', 'className'),
     Output('link-acceso-internet', 'className'),
     Output('link-cobertura-fibra', 'className'),
     Output('link-planes-pospago', 'className'),
     Output('link-conclusiones', 'className')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    # Establecer la clase activa dependiendo de la URL
    active_link = 'nav-link active-link'
    normal_link = 'nav-link'

    if pathname == '/':
        return resumen_general.layout(), active_link, normal_link, normal_link, normal_link, normal_link
    elif pathname == '/acceso-a-internet':
        return kpi_1.layout(), normal_link, active_link, normal_link, normal_link, normal_link
    elif pathname == '/cobertura-fibra':
        return kpi_2.layout(), normal_link, normal_link, active_link, normal_link, normal_link
    elif pathname == '/planes-pospago':
        return kpi_3.layout(), normal_link, normal_link, normal_link, active_link, normal_link
    elif pathname == '/conclusiones':
        return html.Div([html.H3('Conclusiones')]), normal_link, normal_link, normal_link, normal_link, active_link
    else:
        return html.Div([html.H3('Página no encontrada')]), normal_link, normal_link, normal_link, normal_link, normal_link

if __name__ == '__main__':
    app.run_server(debug=False)