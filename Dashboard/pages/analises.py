from dash import dcc, html
import dash_bootstrap_components as dbc

def layout_analises():
    return html.Div([
        # 1. Barra de Busca Superior (LLM Style)
        html.Div([
            dbc.InputGroup([
                dbc.Input(
                    id="ai-chat-input", 
                    placeholder="Faça alguma pergunta sobre seus dados...", 
                    style={
                        "borderRadius": "12px 0 0 12px", 
                        "borderRight": "none",
                        "backgroundColor": "rgba(255, 255, 255, 0.6)",
                        "backdropFilter": "blur(10px)"
                    }
                ),
                dbc.Button(
                    html.I(className="fa-solid fa-paper-plane"), 
                    id="ai-chat-btn", 
                    style={
                        "borderRadius": "0 12px 12px 0", 
                        "backgroundColor": "#732dd3", 
                        "borderColor": "#732dd3",
                        "color": "white"
                    }
                )
            ], style={"boxShadow": "0 4px 15px rgba(0, 0, 0, 0.05)"})
        ], className="mb-4 p-4", style={
            "borderRadius": "16px",
            "backgroundColor": "rgba(255, 255, 255, 0.25)",
            "backdropFilter": "blur(12px)",
            "border": "1px solid rgba(255, 255, 255, 0.3)",
            "boxShadow": "0 8px 32px 0 rgba(31, 38, 135, 0.07)"
        }),

        # 2. Grid de Insights Estatísticos (Camada 1)
        html.Div([
            html.H5(html.B("Quick Insights"), className="mb-0 text-secondary"),
            dbc.Button(
                html.I(className="fa-solid fa-arrows-rotate"), 
                id="btn-refresh-insights", 
                color="light", 
                size="sm", 
                className="ms-3 rounded-circle shadow-sm",
                style={"width": "35px", "height": "35px", "color": "#732dd3"}
            )
        ], className="d-flex align-items-center mb-3"),
        dcc.Loading(
            type="circle",
            color="#732dd3",
            children=html.Div(id='quick-insights-container')
        ),

        # 3. Stream de Respostas DeepSeek (Camada 2)
        html.H5(html.B("AI Assistant"), className="mb-3 text-secondary"),
        dcc.Loading(
            id="loading-ai",
            type="dot",
            color="#732dd3",
            children=html.Div(id="ai-chat-output", className="mt-2")
        )
    ], style={"paddingTop": "1.5rem"})
