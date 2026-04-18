import json

def build_prompt(db_summary: dict, user_focus: str = None, observations: str = None) -> str:
    """Constrói prompt para Gemini baseado nos dados da clínica"""
    
    services = db_summary.get("services", [])
    clients = db_summary.get("clients", [])
    costs = db_summary.get("costs", [])
    monthly = db_summary.get("monthly_summary", [])
    
    services_info = "\n".join([
        f"- {s.get('service_name')}: R$ {s.get('service_value')}, {s.get('total_appointments')} agendamentos, Receita: R$ {s.get('total_revenue')}"
        for s in services[:10]
    ])
    
    clients_info = "\n".join([
        f"- {c.get('client_name')}: {c.get('total_appointments')} visitas, Última: {c.get('days_since_last')} dias, Gastou: R$ {c.get('total_spent')}"
        for c in clients[:10]
    ])
    
    costs_info = "\n".join([
        f"- {c.get('description')} ({c.get('category')}): R$ {c.get('value')}"
        for c in costs[:15]
    ])
    
    monthly_info = "\n".join([
        f"- {m.get('month')}/{m.get('year')}: Receita R$ {m.get('revenue')}, Custos R$ {m.get('costs')}"
        for m in monthly[:12]
    ])
    
    base_prompt = f"""Você é um consultor de negócios para clínica de estética. Analise os dados abaixo e gere insights acionáveis.

SERVIÇOS E RECEITA:
{services_info}

CLIENTES:
{clients_info}

CUSTOS (Materiais, Aluguel, Etc):
{costs_info}

RESUMO MENSAL (Receita vs Custos):
{monthly_info}
"""

    if user_focus:
        base_prompt += f"\nFOCO DO USUÁRIO: {user_focus}\n"
    
    if observations:
        base_prompt += f"OBSERVAÇÕES ADICIONAIS: {observations}\n"
    
    base_prompt += """
INSTRUÇÕES OBRIGATÓRIAS:
1. Retorne APENAS JSON válido, sem texto adicional
2. Gere entre 5 e 10 insights
3. Insights devem ser acionáveis e específicos
4. Textos máximo 300 caracteres
5. Categorias: finance, clients, marketing, retention, operations
6. Prioridades: low, medium, high
7. Linguagem clara e simples

FORMATO JSON:
[
  {
    "title": "string",
    "text": "string",
    "category": "finance | clients | marketing | retention | operations",
    "priority": "low | medium | high"
  }
]
"""
    
    return base_prompt
