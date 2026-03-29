# 📦 Delivery Analytics

Sistema web simples para registro e análise de entregas, desenvolvido com Flask + SQLite.

## 🚀 Objetivo

Criar uma ferramenta prática para acompanhar entregas de delivery, analisando dados como faturamento, horários, bairros e desempenho ao longo do tempo.

---

## ⚙️ Funcionalidades

### 📝 Registro de Entregas
- Cadastro de pedidos com valor, bairro, data e hora
- Cálculo automático de taxas de entrega

### 📊 Dashboard (Página Inicial)
- Entregas do dia;
- Gráfico de entregas por horário;
- Ranking de bairros.

### 📈 Métricas
- KPIs:
  - Total de produtos
  - Total de taxas
  - Faturamento total
  - Ticket médio
- Gráfico de entregas por dia
- Filtro por período:
  - Hoje
  - Últimos 7 dias
  - Últimos 30 dias

### 📂 Histórico
- Consulta de entregas por data

---

## 🛠️ Tecnologias

- Python
- Flask
- SQLite
- HTML / CSS
- JavaScript
- Chart.js

---

## ▶️ Como rodar o projeto

```bash
# Clonar o repositório
git clone https://github.com/pauloalfradique98/delivery-analytics.git

# Entrar na pasta
cd delivery-analytics

# Instalar dependências (se necessário)
pip install flask

# Rodar o projeto
python app.py