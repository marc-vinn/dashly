# Dashboard de Relatórios (Clean Architecture)

Este repositório contém a aplicação de Dashboard interativo. Ele foi refatorado focando em **Arquitetura Limpa (Clean Architecture)**, **Isolamento de Lógica** e **Segurança**.

## 🛡️ Segurança e Padrões (GITTY e Coder)
- Nenhum dado bruto é enviado ao frontend.
- O `.gitignore` bloqueia o upload de arquivos CSV/Excel sensíveis.
- O código segue o **Single Responsibility Principle (SRP)**.
- Todas as features são orientadas por **Test-Driven Development (TDD)**.

## 📁 Estrutura do Projeto (Proposta)
- `core/` (ou `domain/`): Modelos de dados e lógica pura, independente do Dash.
- `services/`: Serviços que conectam os dados às lógicas, validam uploads e armazenam seguramente os dados no backend.
- `Dashboard/`: A camada de apresentação, que contém componentes e callbacks do Dash que apenas interagem com a camada de `services`.
- `tests/`: Onde todos os testes do pytest residem.

## 🚀 Como iniciar
(Em desenvolvimento)
