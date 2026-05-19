# Dashly — Dashboard Inteligente de Dados

Dashboard interativo construído com **Dash + Plotly** que transforma planilhas em insights visuais. Arquitetura limpa com separação de camadas, cache seguro e UI em Liquid Glass.

## ✨ Funcionalidades

- **Upload dinâmico** de arquivos CSV e Excel (XLS/XLSX)
- **Gráficos automáticos** — barras, pizza e histogramas gerados por tipo de dado
- **Quick Insights** — algoritmo Apriori para detecção de correlações estatísticas
- **AI Assistant** — chat com IA (DeepSeek via OpenRouter) com guardrails anti-escopo
- **Exportação** — PDF completo do dashboard e PNG individual de cada gráfico

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


## 🛠️ Stack

| Tecnologia | Uso |
|---|---|
| Dash + Plotly | Framework web + gráficos interativos |
| Dash Bootstrap | Componentes UI responsivos |
| Pandas | Manipulação de dados |
| mlxtend (Apriori) | Análise de associação estatística |
| diskcache | Cache de sessão thread-safe |
| OpenRouter API | Integração com LLM (DeepSeek) |
