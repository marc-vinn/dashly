from dash import html, dcc


def layout_landing():
    return html.Div([
        # Canvas para o fundo de partículas
        html.Canvas(id="particleCanvas"),

        # Conteúdo central
        html.Div([
            html.H1([
                "Entenda seus dados como nunca e tome as melhores decisões com ",
                html.Span("Dashly", className="dashly-highlight")
            ], className="landing-h1"),

            html.P("Clique no botão para carregar seu arquivo!", className="landing-subtitle"),

            # Botão de upload integrado com efeito Liquid Glass
            # O redirect é feito via Output('url', 'pathname') no callback — sem Location duplicado
            dcc.Upload(
                id='upload-landing',
                accept='.csv, .xls, .xlsx',
                children=html.Div([
                    html.Div(className="glass-filter"),
                    html.Div(className="glass-overlay"),
                    html.Div(className="glass-specular"),
                    html.Div(
                        html.Span("Iniciar Análise"),
                        className="glass-content"
                    )
                ], className="glass-button"),
                multiple=False,
                style={"textDecoration": "none", "cursor": "pointer"}
            ),

        ], className="landing-content")
    ])
