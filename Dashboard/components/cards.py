from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import textwrap

# Paleta tema roxo
COR_PRIMARIA    = '#9858f1'   # barras principais, pizza 1º lugar
COR_HISTOGRAMA  = '#732dd3'   # histogramas
COR_ESCURA      = '#1A1D21'   # textos e 2º lugar pizza
COR_CINZA       = '#EBECEF'   # barras secundárias / 3º lugar pizza
COR_LEGENDA     = '#2b2b2b'   # todas as legendas

PALETA_PIZZA_BASE = [COR_PRIMARIA, COR_ESCURA, COR_CINZA]


def _paleta_pizza(n):
    paleta = []
    for i in range(n):
        if i < 3:
            paleta.append(PALETA_PIZZA_BASE[i])
        else:
            paleta.append('#717680')
    return paleta


def criar_bloco_pergunta(df, coluna, info, largura, tipo_grafico):
    # 1. PREPARAÇÃO DE DADOS
    counts = df[coluna].value_counts().reset_index()
    counts.columns = [coluna, 'Quantidade']

    esquema_largo = ['histograma', 'barras', 'barra']
    largura_final = 8 if tipo_grafico in esquema_largo else largura

    counts[coluna] = counts[coluna].apply(
        lambda x: "<br>".join(textwrap.wrap(str(x), width=18))
    )

    layout_base = dict(
        font=dict(family="SF Pro, Inter, sans-serif", size=10, color=COR_LEGENDA),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=30, r=20, t=10, b=100),
        autosize=True,
        legend=dict(font=dict(color=COR_LEGENDA))
    )

    indicadores = [
        html.Small("Moda: ", style={"color": "#717680"}),
        html.Strong(f" {info['moda']}", style={"color": COR_ESCURA, "marginRight": "15px"}),
    ]
    if 'media' in info and info['media'] is not None:
        indicadores.append(html.Small("Média: ", style={"color": "#717680"}))
        indicadores.append(html.Strong(f" {info['media']}", style={"color": COR_PRIMARIA}))

    # 2. GERAÇÃO DOS GRÁFICOS
    if tipo_grafico == 'histograma':
        fig = px.bar(counts, x=coluna, y='Quantidade', template="plotly_white")
        fig.update_traces(
            marker_color=COR_HISTOGRAMA,
            marker_cornerradius=8,
            width=1.0,
            showlegend=False
        )
        fig.update_layout(
            **layout_base, bargap=0,
            xaxis={'type': 'category', 'tickangle': -45, 'automargin': True,
                   'title': None, 'tickfont': {'color': COR_LEGENDA}},
            yaxis={'showgrid': False, 'visible': False}
        )

    elif tipo_grafico == 'pizza':
        fig = px.pie(
            counts, values='Quantidade', names=coluna,
            hole=.75,
            color_discrete_sequence=_paleta_pizza(len(counts))
        )
        layout_pizza = layout_base.copy()
        layout_pizza['margin'] = dict(l=10, r=10, t=10, b=50)
        layout_pizza['showlegend'] = True
        layout_pizza['legend'] = dict(
            orientation="h", y=-0.2, x=0.5, xanchor="center",
            font=dict(color=COR_LEGENDA)
        )
        fig.update_traces(
            textinfo='percent',
            textfont_color=COR_LEGENDA,
            textfont_size=11,
        )
        fig.update_layout(**layout_pizza)

    else:  # BARRAS
        fig = px.bar(counts, x=coluna, y='Quantidade', template="plotly_white")
        fig.update_traces(
            marker_color=COR_PRIMARIA,
            marker_cornerradius=8,
            width=0.4,
            showlegend=False
        )
        fig.update_layout(
            **layout_base, bargap=0.3,
            xaxis={'type': 'category', 'tickangle': -45, 'automargin': True,
                   'title': None, 'tickfont': {'color': COR_LEGENDA}},
            yaxis={'showgrid': True, 'gridcolor': 'rgba(0,0,0,0.05)',
                   'title': None, 'tickfont': {'color': COR_LEGENDA}}
        )

    # ID único para exportação PNG individual
    graph_id = f"graph-{coluna[:20].replace(' ', '-')}"

    # 3. RETORNO (Liquid Glass Card)
    return dbc.Col([
        dbc.Card([
            dbc.CardHeader([
                html.Span(coluna, style={"fontWeight": "600", "color": COR_ESCURA, "fontSize": "14px"}),
                # Menu de opções
                html.Div([
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Baixar como PNG", id={"type": "btn-download-png", "index": graph_id}, className="dropdown-item-download")
                        ],
                        label="⋯",
                        toggle_style={
                            "background": "transparent",
                            "border": "none",
                            "color": "#717680",
                            "fontSize": "20px",
                            "padding": "2px 8px",
                            "lineHeight": "1",
                            "boxShadow": "none",
                        },
                        toggle_class_name="btn-three-dots-toggle",
                        align_end=True,
                        color="link",
                    )
                ], className="card-actions")
            ], className="border-0 bg-transparent pt-4 d-flex justify-content-between align-items-center"),
            dbc.CardBody([
                html.Div(indicadores, className="mb-2 px-1"),
                dcc.Graph(
                    id=graph_id,
                    figure=fig,
                    config={
                        'displayModeBar': False,
                        'responsive': True,
                        'toImageButtonOptions': {
                            'format': 'png', 'filename': coluna, 'scale': 2
                        }
                    },
                    style={"height": "350px", "width": "100%"}
                )
            ], className="d-flex flex-column pt-0")
        ], className="glass-card h-100 w-100")
    ], lg=largura_final, md=12, xs=12, className="mb-4 d-flex align-items-stretch")


def criar_card_kpi(titulo, valor, icone, cor_texto):
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(titulo, className="text-muted mb-1",
                            style={"fontSize": "12px", "color": "#717680"}),
                    html.H3(valor, className="fw-bold",
                            style={"margin": "0", "fontSize": "24px", "color": COR_ESCURA})
                ], width=9),
                dbc.Col([
                    html.I(className=f"{icone} fa-xl",
                           style={"color": COR_PRIMARIA, "opacity": "0.8"})
                ], width=3, className="d-flex align-items-center justify-content-end")
            ])
        ])
    ], className="glass-card")