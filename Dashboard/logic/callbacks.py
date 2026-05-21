from dash import html, callback, Input, Output, State, clientside_callback, no_update
import dash_bootstrap_components as dbc

from services.file_service import FileService
from services.data_service import DataService
from logic.processador import auditoria_dados, processar_estatisticas
from components.cards import criar_bloco_pergunta, criar_card_kpi
from pages.dashboard import layout_dashboard, layout_dados
from pages.analises import layout_analises
from pages.landing import layout_landing
from index import get_dashboard_layout


def register_callbacks():

    # ─── CALLBACK 1: ROTEADOR PRINCIPAL ────────────────────────────────────────
    @callback(
        Output('root-content', 'children'),
        Input('url', 'pathname')
    )
    def roteador_principal(pathname):
        if pathname is None or pathname == '/' or pathname == '':
            return layout_landing()
        elif pathname == '/analises':
            return get_dashboard_layout(layout_analises())
        elif pathname == '/dados':
            return get_dashboard_layout(layout_dados())
        else:
            # /dashboard e qualquer outra rota
            return get_dashboard_layout(layout_dashboard())

    # ─── CALLBACK 2A: UPLOAD PELA LANDING PAGE ─────────────────────────────────
    @callback(
        Output('store-data', 'data', allow_duplicate=True),
        Output('url', 'pathname', allow_duplicate=True),
        Input('upload-landing', 'contents'),
        State('upload-landing', 'filename'),
        prevent_initial_call=True
    )
    def upload_pela_landing(contents, filename):
        if not contents:
            return no_update, no_update

        df, erro = FileService.parse_uploaded_file(contents, filename)
        if erro:
            return no_update, no_update

        cache_id = DataService.store_data(df)
        return cache_id, '/dashboard'

    # ─── CALLBACK 2B: UPLOAD PELO HEADER (Nova Análise) ────────────────────────
    @callback(
        Output('store-data', 'data', allow_duplicate=True),
        Output('mensagem-feedback', 'children', allow_duplicate=True),
        Input('upload-data', 'contents'),
        State('upload-data', 'filename'),
        prevent_initial_call=True
    )
    def processar_e_confirmar(contents, filename):
        if contents is None:
            return no_update, no_update

        df, erro = FileService.parse_uploaded_file(contents, filename)
        if erro:
            return no_update, dbc.Alert(f"Erro: {erro}", color="danger", dismissable=True)

        cache_id = DataService.store_data(df)
        return cache_id, dbc.Alert("✓ Planilha carregada com sucesso!", color="success", dismissable=True, duration=3000)

    # ─── CALLBACK 3: FILTROS (apenas pergunta) ─────────────────────────────────
    @callback(
        Output('filtro-pergunta', 'options'),
        Input('store-data', 'data'),
    )
    def atualizar_filtros(cache_id):
        if not cache_id:
            return []

        opcoes, _ = DataService.get_filters_options(cache_id, None)
        return opcoes

    # ─── CALLBACK 4: GRID DINÂMICO ──────────────────────────────────────────────
    @callback(
        Output('grid-de-cards', 'children'),
        Output('kpi-header', 'children'),
        Input('store-data', 'data'),
        Input('filtro-pergunta', 'value'),
    )
    def renderizar_relatorio_final(cache_id, col_filtro):
        if not cache_id:
            return html.Div("Aguardando upload...", className="p-4 text-muted"), []

        df = DataService.get_data(cache_id)
        if df is None:
            return html.Div("Sessão expirada. Faça upload novamente.", className="p-4 text-warning"), []

        total_respostas = len(df)
        kpis = [criar_card_kpi("Total de Respostas", f"{total_respostas}", "fa-solid fa-users", "text-primary")]

        colunas_analise = [c for c in df.columns if "carimbo" not in c.casefold() and "timestamp" not in c.casefold()]

        # Se filtro ativo, renderiza apenas o bloco daquela pergunta
        if col_filtro and col_filtro in colunas_analise:
            colunas_analise = [col_filtro]

        blocos = []
        for col in colunas_analise:
            info = processar_estatisticas(df, col)
            if info.get('tipo') == 'numerico':
                tipo = 'histograma'
                largura = 8
            elif df[col].nunique() <= 3:
                tipo = 'pizza'
                largura = 4
            else:
                tipo = 'barra'
                largura = 8
            blocos.append(criar_bloco_pergunta(df, col, info, largura, tipo))

        return blocos, kpis

    # ─── CALLBACK 5A: GERAÇÃO DE QUICK INSIGHTS (aba Análises) ───────────────────
    from services.insight_service import InsightService
    from dash import dcc
    
    @callback(
        Output('quick-insights-container', 'children'),
        Input('store-data', 'data'),
        Input('btn-refresh-insights', 'n_clicks')
    )
    def exibir_quick_insights(cache_id, n_clicks):
        if not cache_id:
            return dbc.Row(dbc.Col(html.Div("Faça upload de um arquivo para ver os insights estatísticos.", className="text-muted p-3")))

        df = DataService.get_data(cache_id)
        if df is None:
            return dbc.Row(dbc.Col(html.Div("Sessão expirada. Faça upload novamente.", className="text-warning")))

        # Gerar 6 insights e randomizá-los
        regras = InsightService.generate_quick_insights(df, max_rules=6)
        
        cards = []
        for i, regra in enumerate(regras):
            card = dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H6(regra["title"], className="card-title", style={"color": "#732dd3", "fontWeight": "bold"}),
                        dcc.Markdown(regra["description"], className="card-text m-0", style={"fontSize": "15px", "lineHeight": "1.5"})
                    ], className="p-4") # Padding maior para o card ficar mais espesso
                ], style={"borderLeft": "5px solid #732dd3", "borderRadius": "12px", "boxShadow": "0 4px 15px rgba(0,0,0,0.05)"}),
                md=12, lg=4, # 3 cards por linha (layout maior)
                key=f"insight-card-{i}-{n_clicks}" # Key dinâmica ajuda o React a renderizar sem falhas
            )
            cards.append(card)
            
        return dbc.Row(cards, className="g-3 mb-5")

    # ─── CALLBACK 5A: PREENCHER PROMPTS RÁPIDOS ─────────────────────────────────
    from dash import ALL, callback_context, dcc
    import json

    @callback(
        Output('ai-chat-input', 'value', allow_duplicate=True),
        Input({'type': 'quick-prompt', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def preencher_prompt_rapido(n_clicks_list):
        if not any(n_clicks_list):
            return no_update
            
        ctx = callback_context
        if not ctx.triggered:
            return no_update
            
        triggered = ctx.triggered[0]
        prop_id_str = triggered['prop_id'].split('.')[0]
        try:
            prop_id_dict = json.loads(prop_id_str)
            index = prop_id_dict['index']
            prompts = [
                "Faça um resumo geral dos meus dados e aponte as principais métricas.",
                "Quais variáveis possuem as maiores correlações ou dependências mútuas?",
                "Identifique possíveis anomalias, valores atípicos (outliers) ou desvios nos dados.",
                "Quais insights estratégicos ou recomendações de ação você propõe?"
            ]
            return prompts[index]
        except Exception:
            return no_update

    # ─── CALLBACK 5B: AI CHAT ASSISTANT (aba Análises com Histórico e Enter Key) ────
    from services.ai_service import AIService

    def render_chat_history_layout(chat_history):
        if not chat_history:
            return html.Div([
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
            
        bubbles = []
        for i, msg in enumerate(chat_history):
            role = msg.get("role")
            text = msg.get("text", "")
            
            if role == "user":
                bubble = html.Div(
                    text,
                    className="chat-bubble-user animate__animated animate__fadeInUp",
                    key=f"msg-user-{i}"
                )
                bubbles.append(bubble)
            elif role == "assistant":
                bubble = html.Div([
                    html.Div([
                        html.I(className="fa-solid fa-robot me-2", style={"color": "#732dd3"}),
                        html.Span("Dashly AI", style={"fontWeight": "bold", "color": "#732dd3"})
                    ], className="mb-2 d-flex align-items-center", style={"fontSize": "13px"}),
                    dcc.Markdown(text, style={"color": "#1A1D21", "lineHeight": "1.6"})
                ], className="chat-bubble-ai animate__animated animate__fadeInUp", key=f"msg-ai-{i}")
                bubbles.append(bubble)
            elif role == "system_error":
                bubble = dbc.Alert(
                    text,
                    color="warning" if "upload" in text.lower() or "expirada" in text.lower() else "danger",
                    className="mb-3 w-75 align-self-center animate__animated animate__fadeIn"
                )
                bubbles.append(bubble)
                
        return bubbles

    @callback(
        Output('store-chat-history', 'data'),
        Output('ai-chat-output', 'children'),
        Output('ai-chat-input', 'value', allow_duplicate=True),
        Input('ai-chat-btn', 'n_clicks'),
        Input('ai-chat-input', 'n_submit'),
        State('ai-chat-input', 'value'),
        State('store-chat-history', 'data'),
        State('store-data', 'data'),
        prevent_initial_call=True
    )
    def processar_pergunta_ai(n_clicks, n_submit, pergunta, chat_history, cache_id):
        if chat_history is None:
            chat_history = []
            
        ctx = callback_context
        if not ctx.triggered:
            return chat_history, render_chat_history_layout(chat_history), no_update
            
        # Evita processar se a pergunta estiver em branco
        if not pergunta or not pergunta.strip():
            return chat_history, render_chat_history_layout(chat_history), no_update
            
        if not cache_id:
            warning_msg = "Faça upload de um arquivo primeiro."
            chat_history.append({"role": "user", "text": pergunta})
            chat_history.append({"role": "system_error", "text": warning_msg})
            return chat_history, render_chat_history_layout(chat_history), ""
            
        df = DataService.get_data(cache_id)
        if df is None:
            warning_msg = "Sessão expirada. Faça upload novamente."
            chat_history.append({"role": "user", "text": pergunta})
            chat_history.append({"role": "system_error", "text": warning_msg})
            return chat_history, render_chat_history_layout(chat_history), ""
            
        try:
            resumo = AIService.get_data_summary(df)
            resposta = AIService.get_ai_insights(resumo, pergunta)
            
            # Acumula a pergunta e resposta no histórico
            chat_history.append({"role": "user", "text": pergunta})
            chat_history.append({"role": "assistant", "text": resposta})
            
            return chat_history, render_chat_history_layout(chat_history), ""
        except Exception as e:
            error_msg = f"Erro ao processar a IA: {str(e)}"
            chat_history.append({"role": "user", "text": pergunta})
            chat_history.append({"role": "system_error", "text": error_msg})
            return chat_history, render_chat_history_layout(chat_history), ""

    # ─── CALLBACK 6: TABELA DE DADOS BRUTOS ─────────────────────────────────────
    @callback(
        Output('tabela-dados-brutos', 'children'),
        Input('store-data', 'data')
    )
    def exibir_dados_brutos(cache_id):
        if not cache_id:
            return html.Div("Nenhum dado carregado.", className="text-muted")

        df = DataService.get_data(cache_id)
        if df is None:
            return html.Div("Sessão expirada.")

        return dbc.Table.from_dataframe(df, striped=True, bordered=True, responsive=True, size="sm")

    # ─── CALLBACK 7: ATIVAR/DESATIVAR NAV BUTTONS ────────────────────────────────
    @callback(
        Output('nav-dashboard', 'className'),
        Output('nav-analises', 'className'),
        Output('nav-dados', 'className'),
        Input('url', 'pathname')
    )
    def atualizar_nav_ativo(pathname):
        base = "nav-top-btn"
        active = "nav-top-btn nav-top-btn-active"
        if pathname == '/analises':
            return base, active, base
        elif pathname == '/dados':
            return base, base, active
        else:
            return active, base, base

    # ─── CALLBACK 8: PDF SHARE (via clientside) ───────────────────────────────────
    clientside_callback(
        """
        function(n_clicks) {
            if (!n_clicks) return window.dash_clientside.no_update;
            window.exportDashboardToPDF && window.exportDashboardToPDF();
            return window.dash_clientside.no_update;
        }
        """,
        Output('btn-share-pdf', 'disabled'),
        Input('btn-share-pdf', 'n_clicks'),
        prevent_initial_call=True
    )