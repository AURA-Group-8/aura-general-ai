from database.connection import execute_query
import json
from datetime import datetime, timedelta

def get_services_data():
    """Busca dados de serviços e receitas da tabela dados_aplicacao"""
    query = """
    SELECT 
        job_id,
        name as service_name,
        current_price as service_value,
        COUNT(DISTINCT schedule_id) as total_appointments,
        SUM(total_price) as total_revenue,
        AVG(duracao) as avg_duration
    FROM dados_aplicacao
    WHERE canceled = 0 AND status != 'canceled'
    GROUP BY job_id, name, current_price
    ORDER BY total_revenue DESC
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando serviços: {e}")
        return []

def get_clients_data():
    """Busca dados de clientes/usuários e frequência"""
    query = """
    SELECT 
        user_id,
        username as client_name,
        COUNT(DISTINCT schedule_id) as total_appointments,
        MAX(start_datetime) as last_appointment,
        SUM(total_price) as total_spent,
        DATEDIFF(CURDATE(), MAX(start_datetime)) as days_since_last
    FROM dados_aplicacao
    WHERE canceled = 0 AND status != 'canceled'
    GROUP BY user_id, username
    ORDER BY total_spent DESC
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
        schedule_id,
        username as client_name,
        name as service_name,
        total_price as value,
        start_datetime as appointment_date,
        end_datetime,
        status,
        canceled,
        duracao,
        MONTH(start_datetime) as month,
        YEAR(start_datetime) as year
    FROM dados_aplicacao
    ORDER BY start_datetime DESC
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
        data_compra,
        fornecedor,
        nome_material,
        marca,
        data_validade,
        quantidade_comprada,
        unidade_medida,
        valor_total,
        observacoes,
        MONTH(data_compra) as month,
        YEAR(data_compra) as year
    FROM costs
    ORDER BY data_compra DESC
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
        MONTH(start_datetime) as month,
        YEAR(start_datetime) as year,
        SUM(total_price) as revenue,
        COUNT(DISTINCT schedule_id) as total_appointments
    FROM dados_aplicacao
    WHERE canceled = 0 AND status != 'canceled'
    GROUP BY YEAR(start_datetime), MONTH(start_datetime)
    ORDER BY YEAR(start_datetime) DESC, MONTH(start_datetime) DESC
    LIMIT 24
    """
    try:
        result = execute_query(query)
        # Adicionar custos para cada mês
        costs_query = """
        SELECT 
            MONTH(data_compra) as month, 
            YEAR(data_compra) as year, 
            SUM(valor_total) as costs 
        FROM costs 
        GROUP BY YEAR(data_compra), MONTH(data_compra)
        """
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


def get_cancelled_appointments():
    """Busca agendamentos cancelados para análise"""
    query = """
    SELECT 
        schedule_id,
        username as client_name,
        name as service_name,
        start_datetime,
        status,
        canceled,
        total_price
    FROM dados_aplicacao
    WHERE canceled = 1 OR status = 'canceled'
    ORDER BY start_datetime DESC
    LIMIT 50
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando agendamentos cancelados: {e}")
        return []


def get_user_stats(user_id: int):
    """Busca estatísticas de um usuário/cliente específico"""
    query = """
    SELECT 
        user_id,
        username,
        COUNT(DISTINCT schedule_id) as total_appointments,
        SUM(CASE WHEN canceled = 0 THEN 1 ELSE 0 END) as completed_appointments,
        SUM(CASE WHEN canceled = 1 THEN 1 ELSE 0 END) as cancelled_appointments,
        SUM(total_price) as total_spent,
        AVG(total_price) as avg_spent,
        MIN(start_datetime) as first_appointment,
        MAX(start_datetime) as last_appointment
    FROM dados_aplicacao
    WHERE user_id = %s
    GROUP BY user_id, username
    """
    try:
        result = execute_query(query, (user_id,))
        return result[0] if result else None
    except Exception as e:
        print(f"Erro buscando estatísticas do usuário: {e}")
        return None


def get_costs_by_supplier():
    """Busca custos agrupados por fornecedor"""
    query = """
    SELECT 
        fornecedor,
        COUNT(*) as num_compras,
        SUM(valor_total) as total_gasto,
        AVG(valor_total) as media_compra,
        MAX(data_compra) as ultima_compra
    FROM costs
    GROUP BY fornecedor
    ORDER BY total_gasto DESC
    """
    try:
        result = execute_query(query)
        return result if result else []
    except Exception as e:
        print(f"Erro buscando custos por fornecedor: {e}")
        return []
