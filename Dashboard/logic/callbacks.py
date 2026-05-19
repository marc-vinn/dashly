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

    # ─── CALLBACK 5B: AI CHAT ASSISTANT (aba Análises) ───────────────────────────
    from services.ai_service import AIService
    
    @callback(
        Output('ai-chat-output', 'children'),
        Output('ai-chat-input', 'value'), # Limpa o input após enviar
        Input('ai-chat-btn', 'n_clicks'),
        State('ai-chat-input', 'value'),
        State('store-data', 'data'),
        prevent_initial_call=True
    )
    def processar_pergunta_ai(n_clicks, pergunta, cache_id):
        if not n_clicks or not pergunta or not pergunta.strip():
            return no_update, no_update
            
        if not cache_id:
            return dbc.Alert("Faça upload de um arquivo primeiro.", color="warning"), ""
            
        df = DataService.get_data(cache_id)
        if df is None:
            return dbc.Alert("Sessão expirada. Faça upload novamente.", color="warning"), ""
            
        try:
            resumo = AIService.get_data_summary(df)
            resposta = AIService.get_ai_insights(resumo, pergunta)
            
            card_resposta = html.Div([
                html.H6(html.B(f"Sua Pergunta: {pergunta}"), className="mb-3 text-secondary"),
                dcc.Markdown(resposta, style={"color": "#1A1D21", "lineHeight": "1.6"})
            ], className="p-4 mb-3", style={
                "backgroundColor": "#f8f9fa", 
                "borderRadius": "12px",
                "borderLeft": "4px solid #732dd3",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"
            })
            
            return card_resposta, ""
        except Exception as e:
            return dbc.Alert(f"Erro ao processar a IA: {str(e)}", color="danger"), ""

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