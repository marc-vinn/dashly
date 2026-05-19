# Dashly — Dashboard Inteligente de Dados

Dashboard interativo construído com **Dash + Plotly** que transforma planilhas em insights visuais. Arquitetura limpa com separação de camadas, cache seguro e UI em Liquid Glass.

## ✨ Funcionalidades

- **Upload dinâmico** de arquivos CSV e Excel (XLS/XLSX)
- **Gráficos automáticos** — barras, pizza e histogramas gerados por tipo de dado
- **Quick Insights** — algoritmo Apriori para detecção de correlações estatísticas
- **AI Assistant** — chat com IA (DeepSeek via OpenRouter) com guardrails anti-escopo
- **Exportação** — PDF completo do dashboard e PNG individual de cada gráfico
- **UI Liquid Glass** — design inspirado no Apple glassmorphism

## 📁 Estrutura do Projeto

```
Dashboard/
├── app.py                  # Ponto de entrada da aplicação Dash
├── index.py                # Layout principal (Top Header + content)
├── assets/                 # CSS, JS e imagens estáticas
├── components/             # Componentes visuais reutilizáveis (cards, header)
├── logic/                  # Processamento de dados e callbacks do Dash
├── pages/                  # Layouts das páginas (landing, dashboard, análises, dados)
├── services/               # Camada de serviços (FileService, DataService, AIService)
├── tests/                  # Testes unitários (pytest)
└── requirements.txt        # Dependências Python
```

## 🚀 Como Executar

### 1. Clonar e configurar ambiente

```bash
git clone https://github.com/marc-vinn/dashly.git
cd dashly/Dashboard
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

```bash
# Copie o template e preencha com sua chave
copy ..\..env.example ..\.env
```

Edite o `.env` na raiz do projeto:
```
OPENROUTER_API_KEY=sua_chave_openrouter_aqui
```

> **Nota:** A chave da OpenRouter é necessária apenas para o AI Assistant na aba "Análises". O dashboard funciona normalmente sem ela.

### 3. Executar

```bash
python app.py
```

Acesse: [http://localhost:8050](http://localhost:8050)

## 🧪 Testes

```bash
cd Dashboard
python -m pytest tests/ -v
```

## 🛡️ Segurança

- Chaves de API via variáveis de ambiente (nunca em código)
- `.gitignore` protege `.env`, dados de usuário (`*.csv`, `*.xlsx`) e cache
- Cache de sessão com TTL de 24h via `diskcache`
- Validação de uploads com Defense in Depth (extensão + encoding + estrutura)
- Guardrails de escopo no prompt da IA

## 🛠️ Stack

| Tecnologia | Uso |
|---|---|
| Dash + Plotly | Framework web + gráficos interativos |
| Dash Bootstrap | Componentes UI responsivos |
| Pandas | Manipulação de dados |
| mlxtend (Apriori) | Análise de associação estatística |
| diskcache | Cache de sessão thread-safe |
| OpenRouter API | Integração com LLM (DeepSeek) |
