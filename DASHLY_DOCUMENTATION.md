# 📚 Documentação Completa – **Dashly**  
*Dashboard Inteligente de Dados*  

---  

## 1️⃣ Propósito do Projeto  
| Item | Descrição |
|------|-----------|
| **Objetivo geral** | Prover um **painel web interativo** que converte planilhas (CSV, XLS/XLSX) em visualizações, métricas e insights automatizados, com suporte a consultas por IA. |
| **Público‑Alvo** | Analistas de negócios, gestores de produto e usuários que precisam analisar dados rapidamente sem codificação. |
| **Valor de negócio** | • Reduz o tempo de geração de relatórios de **dias → minutos**.<br>• Detecta padrões ocultos usando **Apriori**.<br>• Permite perguntas livres ao dataset via **LLM** com **guardrails** de segurança. |
| **Visão de futuro** | Suporte multi‑tenant, integração com APIs externas, theming avançado (dark / light) e exportação automática de dashboards completos. |

---  

## 2️⃣ Funcionalidades Principais  

| Área | Funcionalidade | Detalhes Técnicos | Benefício ao Usuário |
|------|----------------|-------------------|----------------------|
| **Upload & Parsing** | Recebimento de arquivos CSV/XLS/XLSX, validação de extensão, codificação UTF‑8, fallback para outros encodings. | `FileService.parse_uploaded_file` (validação por extensão, tratamento de erros, proteção contra arquivos mal‑formados). | Upload simples, feedback imediato de erros, garantia de dados limpos. |
| **Cache Seguro** | Armazenamento temporário de DataFrames em disco com TTL de 24 h, thread‑safe. | `DataService` + `diskcache` (diretório `cache_data/`). | Performance rápida, evita recarregamento desnecessário, mantém sessão isolada. |
| **Filtros Dinâmicos** | Dropdowns que listam colunas (excluindo timestamps) e valores únicos. | `DataService.get_filters_options`. | Usuário filtra rapidamente o conjunto de dados sem recarregar a página. |
| **Renderização de Relatórios** | Geração de KPIs, gráficos (histograma, barra, pizza) e cards responsivos. | `components/cards.py` – uso de Plotly, paleta de cores premium, design **Liquid Glass**. | Visualização clara, estética premium, fácil interpretação. |
| **Quick Insights** | Algoritmo Apriori (mlxtend) gera até 6 insights estatísticos com títulos e descrições formatadas em Markdown. | `InsightService.generate_quick_insights`. | Usuário recebe insights acionáveis em segundos. |
| **AI Assistant** | Chat LLM (DeepSeek V4 Flash) recebe resumo dos dados e pergunta do usuário, devolve até 3 respostas curtas, com **guardrails** estritas. | `AIService.get_ai_insights` (variável de ambiente `OPENROUTER_API_KEY`, validação de chave, mensagens de erro claras). | Consulta livre, respostas contextualizadas, custo de tokens otimizado. |
| **Exportação** | Exportação do dashboard inteiro em PDF (via `exportDashboardToPDF` client‑side) e exportação individual de gráficos como PNG. | JavaScript `export.js`, callbacks client‑side, `toImageButtonOptions` de Plotly. | Usuário gera relatórios prontos para apresentação ou auditoria. |
| **Navegação** | Top Header com barra de pesquisa, navegação via URL (`/`, `/analises`, `/dados`, `/dashboard`). | `callbacks.register_callbacks` → roteador principal, estado ativo dos botões de navegação. | Experiência fluida, URLs compartilháveis. |
| **Responsividade** | Layout baseado em **Bootstrap 5** + **Dash Bootstrap Components**, colunas adaptativas (`lg`, `md`, `xs`). | `layout_*.py` e `cards.py` definem breakpoints. | Funciona em desktop, tablet e mobile. |
| **Segurança** | - **Chave de API** nunca hard‑coded, carregada via `os.environ.get`. <br>- **`.gitignore`** protege `.env`, arquivos de cache e dados sensíveis. <br>- **Guardrails** de IA (rejeição de perguntas fora de escopo). <br>- **Validação de uploads** (extensão, codificação, tamanho). | Implementado em `ai_service.py`, `Adds.md`, `.gitignore`, e nas funções de parsing. | Reduz risco de vazamento de credenciais, impede uso indevido da IA, elimina dados sensíveis do repositório. |
| **Testes Automatizados** | Testes unitários com `pytest` cobrindo serviços, callbacks e componentes. | Diretório `tests/`, mocks de `diskcache` e chamadas HTTP. | Garantia de qualidade, prevenção de regressões. |

---  

## 3️⃣ Tecnologias Utilizadas  

| Camada | Tecnologia | Motivo da escolha |
|--------|------------|-------------------|
| **Frontend** | **Dash** + **Plotly** + **Dash Bootstrap Components** | Criação rápida de UI react‑like, visualizações avançadas e integração com Bootstrap responsivo. |
| **Design** | **Liquid Glass** (backdrop‑filter, transparência, gradientes) | Estética premium, sensação de profundidade “Apple‑style”. |
| **Backend / Lógica** | **Python 3.11**, **Pandas**, **mlxtend** (Apriori), **diskcache** | Processamento de dados eficiente, algoritmos de associação, cache thread‑safe. |
| **IA** | **OpenRouter** → *DeepSeek V4 Flash* | Modelo LLM de alta performance, custos baixos, fácil integração via API. |
| **Gerenciamento de dependências** | `requirements.txt` (pip) | Simplicidade e compatibilidade com ambientes virtuais. |
| **Versionamento** | **Git** (GitHub remote) | Controle de histórico, colaboração e CI/CD. |
| **Env vars** | **python‑dotenv** (implícito) | Mantém segredos fora do código. |
| **Teste** | **pytest** | TDD obrigatório, cobertura de lógica crítica. |

---  

## 4️⃣ Arquitetura do Projeto  

```text
Dashboard/
├── app.py                     # Entrypoint – inicia o servidor Dash
├── index.py                   # Layout global e função get_dashboard_layout()
├── assets/
│   ├── style.css              # CSS custom (Glassmorphism, cores)
│   ├── dashly.png             # Logo oficial
│   └── export.js              # Funções client‑side para PDF/PNG
├── components/
│   ├── top_header.py          # Header com logo, barra de busca
│   └── cards.py               # Cards KPI, gráficos, menus de download
├── pages/
│   ├── landing.py             # Tela inicial – upload via landing
│   ├── dashboard.py           # Layout principal do dashboard
│   ├── dados.py               # Página de visualização de dados brutos
│   └── analises.py            # Página “Análises” – quick insights & IA
├── logic/
│   └── callbacks.py           # Registro de todos os callbacks Dash
├── services/
│   ├── file_service.py        # Parsing e validação de uploads
│   ├── data_service.py        # Cache de DataFrames, filtros
│   ├── insight_service.py     # Algoritmo Apriori + formatação
│   └── ai_service.py          # Integração OpenRouter, guardrails, validações
├── tests/                     # Testes unitários (pytest)
├── requirements.txt           # Dependências Python
└── README.md                  # Overview geral
```

### 4.1 Camada de **Apresentação**  
- **Dash** renderiza componentes React‑like.  
- **Liquid Glass** implementado via CSS (`backdrop-filter: blur(12px);`, `background: rgba(255,255,255,0.15)`), bordas translúcidas e sombras suaves.  
- **Bootstrap** fornece grid responsiva (`lg`, `md`, `xs`).  

### 4.2 Camada de **Lógica de Negócio**  
- **Callbacks** centralizados em `logic/callbacks.py`. Cada callback tem responsabilidade única (upload, filtro, renderização, insights, IA).  
- **Service Layer** (`services/`) isola I/O (arquivo, cache, API) da UI, facilitando testes unitários e reutilização.  

### 4.3 Camada de **Persistência Temporária**  
- **diskcache** cria um diretório `cache_data/` fora do workspace git, com TTL 24 h.  
- Cache ID (UUID) passado entre callbacks via `dcc.Store('store-data')`.  

### 4.4 Camada de **IA**  
- **AIService** recebe resumo de dados (`get_data_summary`) e pergunta do usuário.  
- **Guardrails** (arquivo `Adds.md`) definem regras estritas: abortar se a pergunta não for sobre o dataset, resposta fixa "`Faça perguntas relacionadas aos dados`".  
- Token **max_tokens = 500**, **temperature = 0.3** → respostas concisas e consistentes.  

---  

## 5️⃣ Segurança Aplicada  

| Vetor | Medida | Como foi implementada |
|-------|--------|-----------------------|
| **Credenciais** | Chave API em **variável de ambiente** (`OPENROUTER_API_KEY`). | `ai_service.py` lê com `os.environ.get`. `.env.example` fornece template. |
| **Exposição de segredos** | `.gitignore` bloqueia `.env`, `cache_data/`, arquivos CSV/Excel sensíveis. | Adicionado `!.env.example` para permitir versionamento do template. |
| **Cache** | Não versionado, armazenado localmente, TTL curta. | `git rm --cached Dashboard/cache_data/*`. |
| **Upload** | Validação por extensão, tamanho, codificação, tratamento de exceções. | `FileService.parse_uploaded_file`. |
| **IA Guardrails** | Prompt contém regras estritas, aborta fora de escopo, resposta fixa. | Documentado em `Adds.md` e implementado em `AIService.get_ai_insights`. |
| **Rate‑limiting & Timeout** | `requests.post(..., timeout=20)`. | Evita hanging da API. |
| **Sanitização de Inputs** | Apenas valores esperados chegam ao LLM (resumo de dataset, não arquivo bruto). | `AIService.get_data_summary` gera JSON resumido. |
| **Exportação** | Funções client‑side não acessam o filesystem do usuário. | `exportDashboardToPDF` usa `html2canvas` + `jsPDF`. |
| **Testes de Segurança** | Testes unitários cobrem cenários de upload inválido, chave ausente, respostas fora de escopo. | `tests/` inclui mocks de `requests` e `diskcache`. |

---  

## 6️⃣ Boas Práticas Adoptadas  

1. **Clean Architecture** – separação clara entre *Presentation* (`pages/`, `components/`), *Domain* (`services/`, `logic/`) e *Infrastructure* (`diskcache`, `requests`).  
2. **Single Responsibility Principle** – cada função / callback faz **uma única coisa** (ex.: `upload_pela_landing`, `exibir_quick_insights`).  
3. **Defense‑in‑Depth** – validações em múltiplas camadas (frontend, service, IA).  
4. **TDD** – todos os novos módulos têm testes unitários antes de serem mesclados.  
5. **Versionamento Semântico** – mensagens de commit claras (`security: …`, `style: …`).  
6. **Documentação de Código** – docstrings detalhadas, comentários de arquitetura.  
7. **Design System** – paleta de cores, tipografia (`Inter` via Google Fonts) e componentes reutilizáveis (`glass-card`).  
8. **CI‑Ready** – `requirements.txt` travado, testes automatizados podem ser integrados a GitHub Actions.  

---  

## 7️⃣ Estrutura de Diretórios – Visão Detalhada  

```text
Dashboard/
│
├─ app.py                         # dash.Dash() + server initialization
│
├─ index.py                       # get_dashboard_layout() – wrapper que aplica header/footer
│
├─ assets/
│   ├─ style.css                  # CSS custom (Glassmorphism, animações de hover, fontes)
│   ├─ dashly.png                 # Logo oficial
│   └─ export.js                  # Client‑side export (PDF/PNG) + PDF generation logic
│
├─ components/
│   ├─ top_header.py              # Header com logo, buscar LLM, botão de exportação
│   └─ cards.py                   # Cards KPI, gráficos, menus de download, paleta de cores
│
├─ pages/
│   ├─ landing.py                 # Tela inicial (upload via landing)
│   ├─ dashboard.py               # Layout principal do dashboard (KPIs + grids)
│   ├─ dados.py                   # Tabela de dados brutos (responsive)
│   └─ analises.py                # Aba “Análises”: quick insights + AI chat
│
├─ logic/
│   └─ callbacks.py               # Registro de todos os callbacks (router, upload, filtros, insights, AI, export)
│
├─ services/
│   ├─ file_service.py            # Parsing de arquivos, validações de extensão/encoding
│   ├─ data_service.py            # Cache (diskcache), filtro de opções
│   ├─ insight_service.py         # Algoritmo Apriori + formatação de regras
│   └─ ai_service.py              # Integração com OpenRouter, guardrails, validação de chave
│
├─ tests/                         # pytest suite (unitários + integração)
│
├─ .gitignore                     # Ignora .env, caches, dados sensíveis, virtualenvs
├─ .env.example                   # Template de variáveis de ambiente (sem valores reais)
├─ README.md                      # Overview
├─ Adds.md                        # Spec de IA e guardrails (não contém chaves)
└─ requirements.txt               # Dependências fixas
```

---  

## 8️⃣ Cuidados Tomados em Cada Funcionalidade  

| Funcionalidade | Risco Potencial | Mitigação |
|----------------|----------------|-----------|
| **Upload** | Arquivo mal‑formado → crash, injeção de código. | Validação de extensão, fallback de codificação, tratamento de exceções (`UnicodeDecodeError`, `ParserError`). |
| **Cache** | Dados persistidos podem vazar. | TTL 24 h, diretório excluído do git, uso de `diskcache` thread‑safe. |
| **Filtros** | Injeção de nomes de colunas maliciosas. | Lista de colunas filtradas (`carimbo`, `timestamp`) e validação de existência antes de usar. |
| **Gráficos** | XSS via conteúdos de labels. | `textwrap.wrap` + escape de strings ao gerar rótulos; Plotly sanitiza automaticamente. |
| **Quick Insights** | Exposição de dados sensíveis nas regras. | Regra gera apenas **insights agregados** (máximo 3 frases, sem números exatos). |
| **AI Assistant** | Uso indevido da API (spam, perguntas fora de escopo). | Guardrails no prompt (reject out‑of‑scope, resposta fixa), temperatura baixa, limite de tokens, validação de chave. |
| **Exportação PDF/PNG** | Download de arquivos externos. | Funções client‑side utilizam apenas DOM atual; não há download de recursos externos. |
| **Deploy** | Chave hard‑coded no repositório. | Removida, chave passada via `.env`; `.gitignore` assegura que `.env` nunca seja versionado. |
| **Testes** | Código quebrado em futuras alterações. | Cobertura de testes unitários + CI automatizado (pytest). |

---  

## 9️⃣ Como Executar o Projeto  

### Pré‑requisitos  

| Item | Comando |
|------|---------|
| **Python 3.11+** | `python --version` (deve retornar 3.11 ou superior) |
| **Virtualenv** | `python -m venv .venv` <br> `.\.venv\Scripts\activate` (Windows) |
| **Instalação de dependências** | `pip install -r requirements.txt` |
| **Variáveis de ambiente** | Copiar o template: `copy .env.example .env` <br> Editar `.env` → `OPENROUTER_API_KEY= SUA_CHAVE_AQUI` |

### Execução  

```bash
cd Dashboard
python app.py
```

A aplicação estará disponível em **http://localhost:8050**.  

### Testes  

```bash
cd Dashboard
pytest -v
```

### Deploy  

```bash
git push origin main   # já configurado no remoto https://github.com/marc-vinn/dashly
```

> **Importante:** A chave de API deve ser sempre gerenciada via `.env` para proteger as credenciais de vazamentos.

---  

## 🔟 Histórico de Alterações de Segurança e UI

| Commit | Mensagem | Principais Alterações |
|--------|----------|-----------------------|
| `bd03137` | `style: update project logo to new Dashly design` | Substituição de `logo.png` por `dashly.png` em `top_header.py`. |
| `78d00a3` | `security: remove hardcoded API key, untrack cache data, delete legacy files, update README` | • Remoção de chave hard‑coded (`ai_service.py`, `Adds.md`). <br>• `git rm --cached` de `cache_data/*`. <br>• Deleção de arquivos legados (`sidebar.py`, `graficos.py`, etc.). <br>• `.gitignore` atualizado (venv2, whitelist `.env.example`). <br>• `README.md` atualizado. |

---  

## 📣 Conclusão  

O projeto **Dashly** segue padrões modernos de desenvolvimento, garantindo uma arquitetura limpa (Clean Architecture), segurança (secrets gerenciados fora do código e guardrails de IA), design premium (Liquid Glass) e geração instantânea de valor com o uso de algoritmos preditivos e Large Language Models otimizados.
