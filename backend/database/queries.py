from database.connection import execute_query
import json
from datetime import datetime, timedelta

def get_services_data():
    """Busca dados de serviços e receitas"""
    query = """
    SELECT 
        s.id,
        s.name as service_name,
        s.value as service_value,
        COUNT(a.id) as total_appointments,
        SUM(a.value) as total_revenue
    FROM services s
    LEFT JOIN appointments a ON s.id = a.service_id
    GROUP BY s.id, s.name, s.value
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando serviços: {e}")
        return []

def get_clients_data():
    """Busca dados de clientes e frequência"""
    query = """
    SELECT 
        c.id,
        c.name as client_name,
        COUNT(a.id) as total_appointments,
        MAX(a.appointment_date) as last_appointment,
        SUM(a.value) as total_spent,
        DATEDIFF(CURDATE(), MAX(a.appointment_date)) as days_since_last
    FROM clients c
    LEFT JOIN appointments a ON c.id = a.client_id
    GROUP BY c.id, c.name
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando clientes: {e}")
        return []

def get_appointments_data():
    """Busca dados de agendamentos recentes"""
    query = """
    SELECT 
        a.id,
        c.name as client_name,
        s.name as service_name,
        a.value,
        a.appointment_date,
        MONTH(a.appointment_date) as month,
        YEAR(a.appointment_date) as year
    FROM appointments a
    JOIN clients c ON a.client_id = c.id
    JOIN services s ON a.service_id = s.id
    ORDER BY a.appointment_date DESC
    LIMIT 100
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando agendamentos: {e}")
        return []

def get_costs_data():
    """Busca dados de custos gerais da planilha"""
    query = """
    SELECT 
        id,
        category,
        description,
        value,
        purchase_date,
        MONTH(purchase_date) as month,
        YEAR(purchase_date) as year
    FROM costs
    ORDER BY purchase_date DESC
    LIMIT 100
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando custos: {e}")
        return []

def get_monthly_summary():
    """Resumo mensal de receita vs custos"""
    query = """
    SELECT 
        MONTH(appointment_date) as month,
        YEAR(appointment_date) as year,
        SUM(value) as revenue
    FROM appointments
    GROUP BY YEAR(appointment_date), MONTH(appointment_date)
    ORDER BY YEAR(appointment_date) DESC, MONTH(appointment_date) DESC
    LIMIT 24
    """
    try:
        result = execute_query(query)
        # Adicionar custos para cada mês
        costs_query = "SELECT MONTH(purchase_date) as month, YEAR(purchase_date) as year, SUM(value) as costs FROM costs GROUP BY YEAR(purchase_date), MONTH(purchase_date)"
        costs = execute_query(costs_query)
        costs_map = {(c['month'], c['year']): c['costs'] for c in costs}
        
        for row in result:
            row['costs'] = costs_map.get((row['month'], row['year']), 0)
        
        return result if result else []
    except Exception as e:
        print(f"Erro buscando resumo mensal: {e}")
        return []

def get_clinic_data_summary(focus: str = None):
    """Retorna resumo compilado de todos os dados da clínica"""
    summary = {
        "services": get_services_data(),
        "clients": get_clients_data(),
        "appointments": get_appointments_data(),
        "costs": get_costs_data(),
        "monthly_summary": get_monthly_summary(),
        "user_focus": focus,
        "generated_at": datetime.now().isoformat()
    }
    return summary
