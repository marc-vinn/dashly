from dash import dcc, html
import dash_bootstrap_components as dbc

def layout_analises():
    return html.Div([
        # 1. Armazenamento local do Histórico do Chat na sessão
        dcc.Store(id="store-chat-history", data=[]),
        
        # 2. Grid de Insights Estatísticos (Camada 1)
        html.Div([
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
        ], className="mb-4"),

        # 3. Área Principal do Assistente de IA (Chat Stream)
        html.Div([
            html.H5(html.B("AI Assistant"), className="mb-3 text-secondary"),
            dcc.Loading(
                id="loading-ai",
                type="dot",
                color="#732dd3",
                children=html.Div([
                    # ESTADO INICIAL (Empty State) - será substituído pelas mensagens quando houver histórico
                    html.Div([
                        html.Div(
                            html.I(className="fa-solid fa-wand-magic-sparkles"),
                            className="chat-empty-icon"
                        ),
                        html.H3("Assistente de IA Dashly", className="chat-empty-title"),
                        html.P(
                            "Faça perguntas sobre seus dados, descubra correlações ocultas, "
                            "identifique anomalias ou solicite análises preditivas completas.",
                            className="chat-empty-subtitle"
                        ),
                        # Prompts Rápidos Sugeridos
                        html.Div([
                            html.Div([
                                html.Div("Resumo Geral", className="chat-prompt-title"),
                                html.Div("Faça um resumo estatístico das variáveis e principais padrões.", className="chat-prompt-desc")
                            ], className="chat-prompt-card", id={"type": "quick-prompt", "index": 0}, n_clicks=0),
                            
                            html.Div([
                                html.Div("Buscar Correlações", className="chat-prompt-title"),
                                html.Div("Identifique quais variáveis possuem maior relação mútua.", className="chat-prompt-desc")
                            ], className="chat-prompt-card", id={"type": "quick-prompt", "index": 1}, n_clicks=0),
                            
                            html.Div([
                                html.Div("Detectar Anomalias", className="chat-prompt-title"),
                                html.Div("Encontre outliers, valores atípicos ou inconsistências.", className="chat-prompt-desc")
                            ], className="chat-prompt-card", id={"type": "quick-prompt", "index": 2}, n_clicks=0),
                            
                            html.Div([
                                html.Div("Conselhos Estratégicos", className="chat-prompt-title"),
                                html.Div("Obtenha insights e recomendações práticas de negócios.", className="chat-prompt-desc")
                            ], className="chat-prompt-card", id={"type": "quick-prompt", "index": 3}, n_clicks=0),
                        ], className="chat-quick-prompts")
                    ], className="chat-empty-state", id="chat-welcome-state")
                ], id="ai-chat-output", className="d-flex flex-column")
            )
        ], style={"flex": "1", "display": "flex", "flexDirection": "column"}),

        # 4. Barra de Input Flutuante/Fixa na Parte Inferior (Estilo Liquid Glass)
        html.Div([
            dbc.InputGroup([
                dbc.Input(
                    id="ai-chat-input", 
                    placeholder="Faça alguma pergunta sobre seus dados...", 
                    type="text",
                    autocomplete="off",
                    style={
                        "borderRadius": "12px 0 0 12px", 
                        "borderRight": "none",
                        "backgroundColor": "rgba(255, 255, 255, 0.7)",
                        "backdropFilter": "blur(10px)",
                        "fontSize": "15px",
                        "padding": "12px 18px"
                    }
                ),
                dbc.Button(
                    html.I(className="fa-solid fa-paper-plane"), 
                    id="ai-chat-btn", 
                    style={
                        "borderRadius": "0 12px 12px 0", 
                        "backgroundColor": "#732dd3", 
                        "borderColor": "#732dd3",
                        "color": "white",
                        "padding": "12px 24px"
                    }
                )
            ])
        ], className="chat-input-sticky")
    ], className="chat-container")
