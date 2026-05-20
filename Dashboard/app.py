import sys
import os

# Garantir que o diretório do app está no Python path (necessário para Vercel)
# Quando a Vercel importa "Dashboard/app.py", o CWD pode ser a raiz do repo,
# não o diretório Dashboard/, quebrando imports como "from logic.callbacks import..."
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from logic.callbacks import register_callbacks

app = dash.Dash(
    __name__,
    assets_folder=os.path.join(APP_DIR, "assets"),
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap"
    ],
    external_scripts=[
        # html2canvas para captura de elementos
        "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js",
        # jsPDF para geração de PDF
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
    ],
    suppress_callback_exceptions=True
)

# Expor o servidor WSGI (Flask) para Vercel/Gunicorn
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='store-data', storage_type='session'),
    html.Div(id='root-content')
])

# Injeção do SVG Filter para o botão Liquid Glass
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Dashly</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <svg style="display: none">
          <filter id="glass-distortion">
            <feTurbulence type="turbulence" baseFrequency="0.008" numOctaves="2" result="noise" />
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="77" />
          </filter>
        </svg>

        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

register_callbacks()

if __name__ == '__main__':
    # Modo desenvolvimento local — o Dash roda seu servidor interno
    server.run(debug=True)

# Em produção (Vercel/Gunicorn), a variável "app" precisa ser o WSGI callable (Flask)
# A Vercel importa este módulo e procura por "app" como ponto de entrada
app = server