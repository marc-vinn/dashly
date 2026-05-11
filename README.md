# Dashboard de Relatórios

Este repositório contém a aplicação de Dashboard interativo. Ele foi refatorado focando em **Arquitetura Limpa (Clean Architecture)**, **Isolamento de Lógica** e **Segurança**.

## 📁 Estrutura do Projeto (Proposta)
- `core/` (ou `domain/`): Modelos de dados e lógica pura, independente do Dash.
- `services/`: Serviços que conectam os dados às lógicas, validam uploads e armazenam seguramente os dados no backend.
- `Dashboard/`: A camada de apresentação, que contém componentes e callbacks do Dash que apenas interagem com a camada de `services`.
- `tests/`: Onde todos os testes do pytest residem.

## 🚀 Como iniciar
(Em desenvolvimento)
