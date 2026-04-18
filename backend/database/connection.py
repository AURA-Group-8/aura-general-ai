import mysql.connector
from mysql.connector import Error
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_connection():
    """Cria conexão com MySQL"""
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            autocommit=True
        )
        logger.info("✅ Conectado ao MySQL")
        return conn
    except Error as e:
        logger.error(f"❌ Erro ao conectar MySQL: {e}")
        raise

def execute_query(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """Executa query e retorna resultado como lista de dicts"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchall()
        logger.debug(f"Query executada: {len(result)} linhas retornadas")
        return result
    
    except Error as e:
        logger.error(f"❌ Erro executando query: {e}")
        return []
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
