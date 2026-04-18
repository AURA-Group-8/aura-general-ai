ve# Aura Insights API

IA para gerar insights de negócio para clínica de estética usando Python, FastAPI e Google Gemini.

## ⚡ Setup Rápido

**1. Ambiente:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**2. Configuração (.env):**
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=clinic
GEMINI_API_KEY=sua_api_key_gemini
```

**3. Iniciar:**
```bash
uvicorn app:app --reload
```

Acesse: http://localhost:8000/docs

## 📊 Dados Integrados

### Banco de Dados
- **Serviços**: nome, valor, total de agendamentos, receita
- **Clientes**: nome, frequência, última visita, gasto total
- **Agendamentos**: data, serviço, cliente, valor
- **Custos**: materiais, aluguel, categoria, data

### Fluxo
1. Busca dados MySQL (serviços, clientes, agendamentos, custos)
2. Usuário envia **foco** e **observações** (opcional)
3. Constrói prompt customizado
4. Chama Gemini 1 vez
5. Retorna insights paginados em cache

## 🔌 Endpoints

### GET /api/v1/insights
Retorna insights paginados com parâmetros query:
```
?page=1&page_size=5&focus=financeiro&observations=aumentar_margem
```

### POST /api/v1/insights
Body com foco e observações:
```json
{
  "focus": "retenção de clientes frequentes",
  "observations": "temos muita variação no mês"
}
```

### GET /api/v1/insights/categories
Lista categorias disponiveis.

### DELETE /api/v1/cache
Limpa cache de insights.

## 📋 Schema dos Insights

```json
{
  "page": 1,
  "page_size": 5,
  "total": 25,
  "items": [
    {
      "title": "Oportunidade de Upsell",
      "text": "Clientes que fazem limpeza 2x/mês raramente fazem peeling. Oferta cruzada: 15% desc...",
      "category": "marketing",
      "priority": "high"
    }
  ]
}
```

**Categorias**: finance, clients, marketing, retention, operations  
**Prioridades**: low, medium, high

## 🗄️ Estrutura MySQL

Tabelas esperadas:
```sql
-- Serviços
CREATE TABLE services (
  id INT PRIMARY KEY,
  name VARCHAR(255),
  value DECIMAL(10,2)
);

-- Clientes
CREATE TABLE clients (
  id INT PRIMARY KEY,
  name VARCHAR(255)
);

-- Agendamentos
CREATE TABLE appointments (
  id INT PRIMARY KEY,
  client_id INT,
  service_id INT,
  appointment_date DATETIME,
  value DECIMAL(10,2)
);

-- Custos
CREATE TABLE costs (
  id INT PRIMARY KEY,
  category VARCHAR(100),
  description VARCHAR(255),
  value DECIMAL(10,2),
  purchase_date DATETIME
);
```

## ✨ Features

✅ FastAPI + Uvicorn  
✅ MySQL connector  
✅ Google Gemini integrado  
✅ Cache em memória (1 hora)  
✅ Paginação  
✅ Input de usuário (foco + observações)  
✅ Logging  
✅ CORS habilitado  
✅ Auto-documentação Swagger


