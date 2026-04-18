# 🤖 Copilot Instructions — Projeto Python + Gemini (Sugestões de Negócio para Clínica de Estética)

## ⚠️ REGRAS ABSOLUTAS DO PROJETO

1. Este repositório contém APENAS backend Python  
2. NÃO gerar frontend  
3. NÃO gerar docker, terraform ou infraestrutura  
4. NÃO gerar autenticação complexa  
5. NÃO criar telas, HTML ou templates  
6. Focar SOMENTE em: MySQL → processamento → Gemini → API REST  
7. Código deve estar pronto para rodar faltando apenas credenciais MySQL e API KEY Gemini  

---

## 🧠 CONTEXTO DO NEGÓCIO

A IA irá gerar insights de negócio para clínica de estética, incluindo:

- análises financeiras  
- clientes mais frequentes  
- retenção  
- serviços mais lucrativos  
- oportunidades de venda  
- sugestões estratégicas  

O banco já está FLATTENED (desnormalizado). Não criar joins complexos.

---

## 🏗️ ARQUITETURA OBRIGATÓRIA

Estrutura do projeto:

/backend  
 ├── app.py  
 ├── config.py  
 ├── requirements.txt  
 ├── README.md  
 │  
 ├── database/  
 │    ├── connection.py  
 │    └── queries.py  
 │  
 ├── services/  
 │    ├── gemini_service.py  
 │    ├── insight_service.py  
 │    └── prompt_builder.py  
 │  
 ├── models/  
 │    └── insight_model.py  
 │  
 └── api/  
      └── routes.py  

Framework obrigatório: FastAPI

---

## 🗄️ CONSUMO DO MYSQL

Usar mysql-connector-python e variáveis de ambiente.

Tabela base:
clinic_flattened_data

Criar função:
get_clinic_data_summary() -> dict

Função deve:
- buscar dados relevantes  
- transformar em JSON resumido  
- limitar volume de dados  

---

## ✨ USO DA IA GEMINI

Biblioteca obrigatória:
google-generativeai

Arquivo:
services/gemini_service.py

Função principal:
generate_insights(prompt: str) -> list[Insight]

Regra: a IA deve ser chamada UMA única vez por execução.

---

## 🧾 PROMPT BASE (MOCKADO)

Arquivo: prompt_builder.py

Função:
build_prompt(custom_focus: str, db_summary: dict) -> str

A IA deve retornar APENAS JSON:

[
  {
    "title": "string",
    "text": "string",
    "category": "finance | clients | marketing | retention | operations",
    "priority": "low | medium | high"
  }
]

Instruções obrigatórias no prompt:

- respostas serão exibidas como cards  
- textos curtos (máx 300 caracteres)  
- recomendações acionáveis  
- linguagem simples  
- máximo 10 insights por execução  

Incluir no prompt:
Custom focus from user:
{custom_focus}

---

## 🔄 SERVICE DE ORQUESTRAÇÃO

Arquivo: insight_service.py

Fluxo:

1 → Buscar dados MySQL  
2 → Construir prompt com personalização  
3 → Chamar Gemini (uma vez)  
4 → Validar JSON retornado  
5 → Salvar em cache simples em memória  
6 → Disponibilizar via API  

---

## 🌐 API PARA O FRONTEND

Rota FastAPI:

GET /insights?page=1&page_size=5&focus=financeiro

Parâmetros:
- page  
- page_size  
- focus (string opcional)

Retorno obrigatório:

{
  "page": 1,
  "page_size": 5,
  "total": 20,
  "items": [
    {
      "title": "...",
      "text": "...",
      "category": "...",
      "priority": "..."
    }
  ]
}

Paginação em memória.

---

## 📦 REQUIREMENTS.TXT

fastapi  
uvicorn  
mysql-connector-python  
python-dotenv  
google-generativeai  
pydantic  

---

## ▶️ README.md OBRIGATÓRIO

### Setup

python -m venv venv  
source venv/bin/activate  
venv\Scripts\activate  
pip install -r requirements.txt  

### Variáveis de ambiente (.env)

MYSQL_HOST=  
MYSQL_USER=  
MYSQL_PASSWORD=  
MYSQL_DATABASE=  

GEMINI_API_KEY=  

### Rodar servidor

uvicorn app:app --reload  

### Testar endpoint

http://localhost:8000/insights  

---

## 🧼 BOAS PRÁTICAS OBRIGATÓRIAS

- usar Pydantic  
- tipagem completa  
- tratamento de erros  
- logging básico  
- separação de responsabilidades  
- código pronto para produção simples  

---

## 🟡 OBSERVAÇÕES

- MVP de IA de insights  
- Escalabilidade não é prioridade  
- Cache simples em memória  
- Banco já preparado  
- IA deve ser barata → 1 chamada  
- Foco em integração com app mobile  

---

## ✅ DEFINIÇÃO DE PRONTO

✔ sobe com uvicorn  
✔ conecta MySQL  
✔ chama Gemini  
✔ retorna insights paginados  
✔ aceita personalização de foco  
✔ pronto para React Native  