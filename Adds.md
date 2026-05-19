# Adds - Planejamento da Página de Análises (Dashly)

Este documento detalha o desenvolvimento da página de **Análises Automáticas** do projeto Dashly. O objetivo é fornecer insights imediatos ao usuário assim que o arquivo CSV for carregado, utilizando uma combinação de análise estatística clássica e inteligência artificial.

---

## 1. Visão Geral da Página
A página de análises será dividida em três seções principais:
1.  **Quick Insights (Heurísticas):** Cards com estatísticas automáticas geradas por algoritmos de correlação e associação.
2.  **AI Assistant (Perguntas e Respostas):** Um chat ou campo de busca onde o usuário pode perguntar "Qual a tendência de vendas no feriado?" e receber uma resposta baseada nos dados.
3.  **Discovery Cards:** Insights narrativos (ex: "73,3% dos usuários que fizeram X, fazem Y e Z").

---

## 2. Estratégia de Implementação de Insights

### A. Abordagem Estatística (Recomendado para Performance)
Para gerar frases como *"X% dos usuários que fazem A também fazem B"*, utilizaremos o algoritmo de **Regras de Associação (Apriori ou FP-Growth)**.
- **Ferramenta:** `mlxtend` ou `pandas`.
- **Lógica:** O sistema identifica padrões frequentes nos dados categóricos e gera métricas de *Confidence* e *Lift*.
- **Vantagem:** É extremamente rápido, gratuito e não depende de API externa para cálculos matemáticos.

### B. Abordagem com IA (Generative BI)
Para transformar os dados brutos em narrativas humanas ou permitir perguntas livres.
- **Fluxo:** 1. O Python extrai o cabeçalho e um resumo estatístico (`df.describe()`, `df.info()`, `df.corr()`).
    2. Esse resumo é enviado via Prompt para uma LLM.
    3. A IA devolve 3 a 5 insights escritos de forma amigável.

---

## 5. Roadmap de Desenvolvimento
- [ ] Implementar script de pré-processamento de dados para identificar colunas categóricas e numéricas.
- [ ] Integrar biblioteca `mlxtend` para geração de regras de associação.
- [ ] Criar interface de chat estilizada no Dash (usando `dbc.Input` e `html.Div` para as mensagens).
- [ ] Configurar a conexão com a API do Groq/Gemini para o "AI Insight Generator".

---

Ia utilizada: Deepseek V4 Flash free :
Api key: Configurada via variável de ambiente OPENROUTER_API_KEY (ver .env.example)

### 3. Layout e Interface do Usuário (UI/UX)

#### A. Barra de Busca Superior (LLM Style)
- Componente de input proeminente no topo da página.
- Placeholder: "Faça alguma pergunta sobre seus dados...".
- Efeito Glassmorphism total (backdrop-filter: blur) sobre o fundo

#### B. Grid de Insights Estatísticos (Camada 1)
- Cards menores organizados logo abaixo da busca.
#### C. Stream de Respostas DeepSeek (Camada 2)
- Uma seção dinâmica que começa oculta ou vazia.
- Cada pergunta do usuário gera um novo card que se empilha nesta área.
- As respostas da IA devem usar Markdown integrado para destacar termos importantes na cor roxa padrao do design do sistema



---
# Especificação Técnica: Guardrails de Contexto e Otimização de Tokens (Dashly)
Este documento define as regras de negócio, arquitetura e engenharia de prompt para a implementação da barra de buscas por IA na página de Análises do projeto Dashly. O objetivo principal é blindar a API contra uso indevido (perguntas fora de escopo) e reduzir drasticamente o consumo desnecessário de tokens de saída (output tokens).  1. Visão Geral do Fluxo (Pipeline de Dados)Para garantir máxima eficiência, o sistema opera em uma Arquitetura Híbrida de Duas Camadas:  Camada Estatística (Local): Processa o CSV via Pandas e gera um dicionário JSON enxuto contendo apenas metadados e sumários estatísticos (get_data_summary).  Camada de IA (DeepSeek API): Recebe o JSON estruturado + a pergunta do usuário dentro de um ambiente controlado por Guardrails baseados em regras estritas.  2. O que é o Guardrail e Regras de EscopoO Guardrail é uma barreira comportamental aplicada no nível do System Prompt. Ele força o modelo a atuar primeiro como um classificador de relevância e, somente se passar na validação, atuar como um analista de dados.  Regras Estritas de Escopo:Perguntas Válidas: Consultas diretas sobre as colunas, correlações, distribuições, anomalias ou insights de negócios derivados do resumo estatístico fornecido.  Perguntas Inválidas (Fora de Escopo): Saudações sem contexto, piadas, pedidos de código (ex: "Como programar em Java?"), receitas, histórias ou qualquer assunto não contido no JSON.  Resposta de Bloqueio Obrigatória: Caso a pergunta seja inválida, a IA DEVE retornar exatamente a string: "Faça perguntas relacionadas aos dados". Sem pontuações adicionais, sem explicações, sem cortesias.  3. Arquitetura para Máxima Eficiência de TokensA otimização de custos segue três etapas obrigatórias:Passo 1: Minimização do Input (Contexto Enxuto)Ação: Nunca envie o arquivo CSV bruto para a API.  Implementação: Use a função get_data_summary(df) para converter tabelas de qualquer tamanho em um JSON de metadados com menos de 2KB. Isto reduz o custo fixo de Input Tokens a frações de centavos por requisição.  Passo 2: Interrupção Antecipada no Output (Early Exit)Ação: Forçar o modelo a falhar rápido e de forma barata.  Implementação: Ao exigir uma resposta de apenas 5 palavras ("Faça perguntas relacionadas aos dados") para inputs inválidos, bloqueamos o comportamento natural das LLMs de gerar parágrafos explicando o motivo de não poderem responder, economizando 99% dos Output Tokens em interações erradas.  Passo 3: Controle de Estado na UI (Dash Callback)Ação: Evitar requisições duplicadas ou vazias.Implementação: Desabilitar o campo de input ou disparar o dcc.Loading imediatamente após o envio, impedindo múltiplos cliques acidentais que gerariam chamadas redundantes à API.  

REGRAS ESTRITAS DE GUARDRAIL (DEFESA DE ESCOPO):
1. Avalie se a pergunta do usuário é estritamente sobre os dados fornecidos no contexto ou sobre análises de negócios diretamente aplicáveis a eles.
2. Se a pergunta for sobre qualquer outro assunto (exemplos: programação, saudações informais longas, culinária, história, piadas, ferramentas externas) ou se não puder ser respondida com as informações do JSON, você DEVE abortar a análise imediatamente.
3. Em caso de aborto por escopo, sua resposta DEVE ser EXATAMENTE a frase abaixo, sem adicionar caracteres, saudações, desculpas ou pontos finais extras:

Faça perguntas relacionadas aos dados

# Diretrizes de Geração de Insights Analíticos (DeepSeek V4 Flash)

**Nota:** Este documento deve ser seguido rigorosamente para garantir que as respostas da IA sejam precisas, úteis e consistentes com o escopo do projeto Dashly. As regras de "Output Conciso" e "Ausência de Metadados" são críticas para a experiência do usuário e otimização de custos.

---

## 1. Regras Gerais e Comportamento

- **Persona:** Atue como um Consultor de Dados experiente e analista de BI.
- **Linguagem:** Português (pt-br).
- ** Tom:** Profissional, objetivo e direto ao ponto.
- **Contexto:** Baseie todas as análises estritamente nos dados estruturados (metadados e estatísticas) fornecidos.

## 2. Regra de Otimização de Output (Anti-Excess)

Para evitar desperdício de tokens e garantir velocidade, siga estas diretrizes:

- **Limite de Insights:** Gere no máximo **3 insights por requisição**.
- **Comprimento de Cada Insight:** Cada insight deve ter entre **15 e 30 palavras**.
- **Estrutura da Frase:**
    - Evite introduções como "Com base nos dados...". Vá direto ao ponto.
    - Foque em apresentar a relação, correlação ou anomalia de forma clara.
    - **Exemplo Ruim:** "Com base na análise das informações, foi possível observar que existe uma correlação negativa significativa entre a coluna X e a coluna Y."
    - **Exemplo Bom:** "As colunas X e Y apresentam forte correlação negativa: quando X aumenta, Y tende a cair drasticamente."

## 3. Regra de Formatação de Saída (Markdown)

Utilize **Markdown** para facilitar a leitura e organização visual dos insights.

- **Listas:** Sempre use listas ordenadas ou não ordenadas.
- **Negrito:** Destaque com **negrito** os termos técnicos, nomes de colunas, percentuais ou valores numéricos importantes.
- **Itálico:** Use itálico para termos de ênfase ou explicações secundárias.
- **Links/Gráficos:** NÃO gere códigos HTML, URLs ou referências a imagens. Gere apenas a descrição textual do insight.

## 4. Regra de Apresentação de Dados (Obrigatória)

- **Não inclua estatísticas brutas na resposta:**
    - Exemplo: Evite listar o número exato de linhas ou porcentagens exatas se isso não for essencial para o entendimento do insight.
    - O usuário já viu os números na tabela `get_data_summary`. Foque na interpretação (o "e daí?").
    - Se precisar citar um número, redonde-o para facilitar a leitura (ex: "quase 80%").

---

## 5. Exemplos de Respostas Válidas

### Cenário 1: Dados de Vendas
**Resumo fornecido:** "Loja A teve queda de 45% nas vendas em Abril. Março teve pico."

**Resposta Válida:**
1.  **Queda Sazonal Observada:** As vendas na Loja A registraram queda brusca de **45%** em Abril, contrastando com o pico de movimento registrado em Março.
2.  **Foco Geográfico:** O desempenho da Loja A impactou significativamente a média geral de vendas da região Sul, que apresentou retração de **12%** no período.
3.  **Anomalia Regional:** Enquanto a região Sul desacelera, a região Sudeste mantém estabilidade, indicando que o problema pode ser localizado.

### Cenário 2: Dados de Satisfação (NPS)
**Resumo fornecido:** "NPS: 25 (Baixo). 30% Promotores, 50% Neutros, 20% Detratores."

**Resposta Válida:**
1.  **Baixa Lealdade do Cliente:** O Net Promoter Score (NPS) de **25** indica um nível crítico de insatisfação entre a base de usuários.
2.  **Risco de Churn:** Com **50%** de clientes Neutros e **20%** de Detratores, há um risco iminente de alta rotatividade (churn) nos próximos trimestres.
3.  **Oportunidade de Conversão:** A estratégia deve focar em converter os clientes Neutros em Promotores, oferecendo incentivos ou melhorando o atendimento reportado.

### Cenário 3: Dados de E-commerce (Taxa de Conversão)
**Resumo fornecido:** "Taxa de conversão 1.2%. Google Ads (R$ 500 investidos), Orgânico (R$ 0 investidos)."

**Resposta Válida:**
1.  **Baixa Eficiência do Funil:** A taxa de conversão geral de **1.2%** é baixa, indicando gargalos no processo de compra desde a visita inicial até a finalização.
2.  **Inef