from dash import dcc, html
import dash_bootstrap_components as dbc


def layout_dashboard():
    return html.Div([
        # Linha de KPI
        dbc.Row([
            dbc.Col(id='kpi-header', lg=4, md=6, xs=12),
        ], className="mb-3 g-3"),

        # Painel de Filtros e Segmentação (Glass Card)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            # 1. Filtro de Exibição
                            dbc.Col([
                                html.Div([
                                    html.I(className="fa-solid fa-chart-simple me-2", style={"color": "#9858f1"}),
                                    html.Label("Exibir Gráficos das Perguntas:", className="text-muted small fw-bold mb-1"),
                                ], className="d-flex align-items-center mb-1"),
                                dcc.Dropdown(
                                    id='filtro-pergunta',
                                    placeholder="Todos os gráficos ativos. Selecione para isolar...",
                                    className="custom-dropdown",
                                    clearable=True,
                                    multi=True
                                ),
                            ], lg=6, md=12, xs=12, className="pe-lg-4 filter-col-divider mb-3 mb-lg-0"),

                            # 2. Filtro de Segmentação (Cross-filtering)
                            dbc.Col([
                                html.Div([
                                    html.I(className="fa-solid fa-filter me-2", style={"color": "#9858f1"}),
                                    html.Label("Segmentar Público por Resposta (Cohort):", className="text-muted small fw-bold mb-1"),
                                ], className="d-flex align-items-center mb-1"),
                                dbc.Row([
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='filtro-segmento-pergunta',
                                            placeholder="Selecione a Pergunta...",
                                            className="custom-dropdown",
                                            clearable=True
                                        ),
                                    ], md=6, xs=12, className="mb-2 mb-md-0"),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='filtro-segmento-resposta',
                                            placeholder="Selecione a Resposta...",
                                            className="custom-dropdown",
                                            clearable=True,
                                            disabled=True
                                        ),
                                    ], md=6, xs=12)
                                ])
                            ], lg=6, md=12, xs=12, className="ps-lg-4"),
                        ])
                    ], className="p-4", style={"overflow": "visible"})
                ], className="glass-card mb-4", style={"overflow": "visible"})
            ], width=12)
        ]),

        # Grid de Gráficos
        dbc.Row(id='grid-de-cards', className="g-4 d-flex flex-wrap justify-content-center")
    ], style={"paddingTop": "1.5rem"})



def layout_dados():
    return html.Div([
        html.H4("Dados Brutos", className="mb-4", style={"color": "#1A1D21"}),
        html.Div(id='tabela-dados-brutos', className="mt-2")
    ], style={"paddingTop": "1.5rem"})
