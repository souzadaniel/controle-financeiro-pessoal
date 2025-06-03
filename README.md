# 💸 Controle Financeiro Pessoal

Este projeto foi desenvolvido com o objetivo de organizar e acompanhar as finanças pessoais de forma estruturada, utilizando Python e MySQL. Os dados são registrados diretamente no banco e poderão futuramente ser visualizados via dashboards no Power BI.

## 🛠 Tecnologias utilizadas

- Python 3
- MySQL Workbench
- Pandas
- Power BI (em breve)

## 📂 Funcionalidades

- Inserir lançamentos (único, fixo e parcelado)
- Editar lançamentos existentes
- Excluir lançamentos
- Consultar lançamentos (com Pandas)
- Registro de:
  - Descrição
  - Valor
  - Data
  - Categoria
  - Conta
  - Natureza
  - Tipo do lançamento

## 📁 Estrutura

```bash
├── inserir_lancamento.py
├── editar_lancamento.py
├── excluir_lancamento.py
├── consultar_lancamento.py
├── conexao.py
├── validador.py
