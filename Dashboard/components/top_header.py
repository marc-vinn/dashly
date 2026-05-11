from dash import html, dcc
import dash_bootstrap_components as dbc


def render_top_header():
    nav_pages = [
        {"label": "Dashboard", "href": "/dashboard", "id": "nav-dashboard"},
        {"label": "Análises",  "href": "/analises",  "id": "nav-analises"},
        {"label": "Dados",     "href": "/dados",      "id": "nav-dados"},
    ]

    nav_buttons = [
        dcc.Link(
            p["label"],
            href=p["href"],
            id=p["id"],
            className="nav-top-btn"
        )
        for p in nav_pages
    ]

    # Botão "Nova Análise" embrulhado em dcc.Upload
    nova_analise_btn = dcc.Upload(
        id='upload-data',
        children=html.Div("Nova Análise", className="nav-top-btn nav-top-btn-nova"),
        multiple=False,
        style={"display": "inline-block"}
    )

    share_btn = html.Button(
        html.I(className="fa-solid fa-share-nodes"),
        id="btn-share-pdf",
        className="share-btn",
        title="Exportar PDF"
    )

    return html.Div([
        # Lado esquerdo: logo + navegação
        html.Div([
            dcc.Link(
                html.Img(src="/assets/logo.png", className="header-logo"),
                href="/",
                style={"textDecoration": "none"}
            ),
            html.Div(nav_buttons + [nova_analise_btn], className="nav-top-group"),
        ], className="header-left"),

        # Lado direito: botão share
        html.Div([
            share_btn,
        ], className="header-right"),

    ], className="top-header", id="top-header")
