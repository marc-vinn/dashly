from dash import html
import dash_bootstrap_components as dbc

def layout_visao_geral():
    return html.Div([
        html.H3("Resumo Estrutural do CSV", className="mb-4 text-secondary"),
        # O callback 'exibir_auditoria_tecnica' vai preencher este ID
        html.Div(id='output-data-upload')
    ])