from dash import dcc, html
import dash_bootstrap_components as dbc


def layout_graficos():
    return html.Div([
        # Uma única linha para KPI + Filtros
        dbc.Row([
            # Aqui entrará o seu card de "Total de Respostas" (largura 3)
            # O ID fica aqui para o callback injetar o conteúdo
            dbc.Col(id='kpi-header', lg=3, md=4, xs=12),

            # Espaço vazio para separar (opcional)
            dbc.Col(lg=5, md=2, className="d-none d-md-block"),

            # Filtros menores ao lado (largura 2 cada)
            dbc.Col([
                html.Label("Filtrar Pergunta:", className="text-muted small fw-bold"),
                dcc.Dropdown(id='filtro-pergunta', placeholder="Selecione...", style={"fontSize": "13px"}),
            ], lg=2, md=3, xs=6),

            dbc.Col([
                html.Label("Filtrar Resposta:", className="text-muted small fw-bold"),
                dcc.Dropdown(id='filtro-valor', placeholder="Selecione...", style={"fontSize": "13px"}),
            ], lg=2, md=3, xs=6),

        ], className="mb-4 align-items-center g-3"),

        # Grid de Gráficos logo abaixo
        dbc.Row(id='grid-de-cards', className="g-4 d-flex flex-wrap")
    ], className="p-4")