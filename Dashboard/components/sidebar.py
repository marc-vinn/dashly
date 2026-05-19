from dash import html, dcc
import dash_bootstrap_components as dbc


def render_sidebar():
    return html.Div(
        className="sidebar-custom",
        style={
            "position": "fixed", "top": 0, "left": 0, "bottom": 0,
            "width": "18rem", "padding": "2rem 1.5rem"
        },
        children=[
            # Logo
            html.Img(src="/assets/dashly.png", style={"width": "100%", "marginBottom": "25px"}),

            # Texto de Instrução
            html.P("Carregue sua planilha para começar",
                   className="text-center fw-bold mb-2",
                   style={"fontSize": "11px"}),

            # Botão Upload (Aqui geralmente mora o erro de parêntese)
            dcc.Upload(
                id='upload-data',
                className="upload-box",
                children=html.Div('Arraste ou Clique'),
                multiple=False
            ),  # <-- Certifique-se que este fecha o dcc.Upload

            html.Hr(style={"margin": "30px 0", "color": "#e9ecef"}),

            # Navegação
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(className="fa-solid fa-table-list"), html.Span("Visão Geral")],
                        href="/", active="exact", className="nav-link-custom"
                    ),
                    dbc.NavLink(
                        [html.I(className="fa-solid fa-chart-pie"), html.Span("Gráficos")],
                        href="/graficos", active="exact", className="nav-link-custom"
                    ),
                ],
                vertical=True,
                pills=True
            ),
        ]
    )