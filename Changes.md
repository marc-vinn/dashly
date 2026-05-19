# Registro de Alterações (Changes.md) - Versão 2.0

## [1.2.0] - 2026-05-01

### 🏗️ Arquitetura e Navegação do Sistema
* **Novo Fluxo de Entrada:** O botão "Iniciar Análise" na Landing Page agora integra o seletor de arquivos (`.csv` ou planilha). O redirecionamento após o upload é automático para a aba de Dashboard com o processamento imediato dos dados.
* **Extinção da Sidebar:** A barra lateral de navegação foi removida.
* **Novo Header de Navegação:** Implementação de menu no topo à esquerda. As páginas são apresentadas em formato de botões, seguindo o padrão visual da Landing Page.
    * **Páginas:** Dashboard, Análises, Dados e Nova Análise.
    * **Lógica de Estado (Active State):** * Botão Selecionado: Fundo `#2b2b2b` e texto Branco.
        * Botão Não Selecionado: Fundo Branco e texto `#2b2b2b`.
* **Ajuste de Layout:** Inclusão de espaçamento de "respiro" entre o menu superior e o início do bloco de gráficos para evitar sobreposição visual.

### 📊 Atualizações Visuais e Dashboard
* **Identidade Visual (Cores):**
    * Substituição do tom Verde pela cor **Roxa (Tema do Projeto)** em todos os elementos.
    * Mantidas as cores auxiliares Pretas e Cinza Claro.
    * **Histogramas:** Cor definida especificamente como `#732dd3`.
    * **Legendas:** Todos os textos de legendas de gráficos agora utilizam a cor `#2b2b2b`.
* **Gráficos de Pizza:** Exibição obrigatória das porcentagens visíveis tanto no corpo do gráfico quanto à frente dos itens na legenda.
* **Simplificação de Filtros:**
    * Reestilização dos filtros para o padrão visual de botões do projeto.
    * Remoção da necessidade de filtrar respostas; agora apenas o filtro de pergunta é utilizado para atualizar o gráfico específico correspondente.

### 📤 Exportação e Compartilhamento
* **Compartilhamento Global:** Adicionado botão redondo com ícone de compartilhamento no topo à direita (cor `#2b2b2b`).
    * **Função PDF:** Gera um arquivo contendo exclusivamente a logo da empresa (superior esquerdo) e os gráficos, garantindo que não seja um print da tela, mas um layout limpo para apresentação.
* **Exportação de Blocos:** Inclusão de menu de "três pontinhos" em cada bloco de gráfico para permitir o download individual daquele elemento em formato `.png`.

### 🗑️ Limpeza de Componentes
* **Página "Visão Geral":** Oficialmente descontinuada e removida do roteamento do sistema.

Ao clicar no botão de iniciar analise no landing page, o usuario ja deve ser capaz de escolher a planilha ou o csv que ele utilizará para fazer a analise dos graficos. Ao carregar, ele ja será direcionado para a aba de dashboard com toda a analise sendo possivel.



A side bar será removida e as paginas agora ficarão no topo da pagina, a esquerda, Em formatos que sigam o padrão do botao da landing page. As novas paginas seráo: Dashboard, Analises, Dados e por ultimo Nova analise, que permite o usuario carregar um novo csv e assim fazer outra analise. A pagina selecionada deve ter o botao preenchido na cor 2b2b2b e o texto em branco, enquanto as nao selecionadas seráo o inverso.



Na pagina de dashboard será quase tudo mantido como está. As unicas alterações nessa aba é que nos graficos de pizza as porcentagens devem ser visiveis na frente da legenda e no grafico. As legendas tambem de todos os graficos devem ficar na cor 2b2b2b e a cor verde dos graficos devem ser substituidadas pela cor tema do projeto, roxa(mantendo as cores pretas e o cinza claro) . Os graficos de histograma devem na cor 732dd3



No topo da pagina a direita será adicionado um botão redondo com o icone de compartilhamento. tambem na cor 2b2b2b. Ao ser clicado, todo o dashboard deve ser compartilhado em pdf, mantendo a logo da empresa no canto superior esquerdo e os graficos com o estilo atual (é muito importante que não seja apenas um print da tela e sim um arquivo que contenha apenas a logo e os graficos). Além disso, no bloco de cada grafico será adicionado os 3 pontinhos que ao clicado permitam salvar em png apenas aquele bloco especifico de gráfico



por conta dos botões no topo, todo o bloco de graficos deve ser movido pra baixo, deixando um espaço de respiro entre os botóes e o inicio do dashboard.



Os filtros tambem devem ser reestilizados para combinarem como estilo de botões. E nao mais é necessario filtrar as respostas, apenas o filtro de pergunta ja é capaz de filtrar apenas o grafico especifico que seja referente a pergunta