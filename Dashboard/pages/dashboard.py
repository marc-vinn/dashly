from dash import dcc, html
import dash_bootstrap_components as dbc


def layout_dashboard():
    return html.Div([
        # Linha de KPI + Filtro de Pergunta
        dbc.Row([
            dbc.Col(id='kpi-header', lg=3, md=4, xs=12),
            dbc.Col(lg=5, md=2, className="d-none d-md-block"),
            dbc.Col([
                html.Label("Filtrar por Pergunta:", className="text-muted small fw-bold mb-1"),
                dcc.Dropdown(
                    id='filtro-pergunta',
                    placeholder="Selecione uma pergunta para isolar o gráfico...",
                    className="custom-dropdown",
                    clearable=True
                ),
            ], lg=4, md=6, xs=12),
        ], className="mb-2 align-items-center g-3"),

        # Grid de Gráficos
        dbc.Row(id='grid-de-cards', className="g-4 d-flex flex-wrap")
    ], style={"paddingTop": "1.5rem"})



def layout_dados():
    return html.Div([
        html.H4("Dados Brutos", className="mb-4", style={"color": "#1A1D21"}),
        html.Div(id='tabela-dados-brutos', className="mt-2")
    ], style={"paddingTop": "1.5rem"})
