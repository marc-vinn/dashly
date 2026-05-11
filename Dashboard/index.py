from dash import html
import dash_bootstrap_components as dbc
from components.top_header import render_top_header


def get_dashboard_layout(page_content_layout):
    return html.Div([
        # Header fixo no topo
        render_top_header(),

        # Alertas de upload
        html.Div(id='mensagem-feedback', style={"padding": "0 2rem"}),

        # Conteúdo da página com respiro abaixo do header
        html.Div(
            page_content_layout,
            id='page-content',
            style={"padding": "2rem", "paddingTop": "1rem"}
        )
    ])