from database.queries import get_clinic_data_summary
from services.prompt_builder import build_prompt
from services.gemini_service import generate_insights
from models.insight_model import Insight, InsightResponse
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Cache simples em memória
_insights_cache = {}
_cache_ttl = timedelta(hours=1)

def get_insights_with_pagination(
    page: int = 1,
    page_size: int = 5,
    focus: str = None,
    observations: str = None
) -> InsightResponse:
    """
    Orquestra todo o fluxo:
    1. Busca dados MySQL
    2. Constrói prompt com personalização
    3. Chama Gemini (1 vez)
    4. Validações
    5. Cache
    6. Paginação
    """
    try:
        cache_key = f"{focus}_{observations}"
        
        # Verifica cache
        if cache_key in _insights_cache:
            cached_data = _insights_cache[cache_key]
            if datetime.now() < cached_data["expires_at"]:
                logger.info("Retornando insights do cache")
                insights = cached_data["insights"]
            else:
                # Cache expirou
                del _insights_cache[cache_key]
                insights = None
        else:
            insights = None
        
        # Se não tem cache, gera
        if insights is None:
            logger.info("Gerando novos insights...")
            
            # 1. Buscar dados
            db_summary = get_clinic_data_summary(focus=focus)
            
            # 2. Construir prompt
            prompt = build_prompt(db_summary, user_focus=focus, observations=observations)
            
            # 3. Chamar Gemini
            insights = generate_insights(prompt)
            
            # 4. Guardar em cache
            _insights_cache[cache_key] = {
                "insights": insights,
                "expires_at": datetime.now() + _cache_ttl
            }
            
            logger.info(f"Gerados {len(insights)} insights")
        
        # 5. Paginar
        total = len(insights)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        paginated_items = insights[start_idx:end_idx]
        
        return InsightResponse(
            page=page,
            page_size=page_size,
            total=total,
            items=paginated_items
        )
    
    except Exception as e:
        logger.error(f"Erro no serviço de insights: {e}")
        return InsightResponse(
            page=page,
            page_size=page_size,
            total=0,
            items=[]
        )

def clear_cache():
    """Limpa cache"""
    global _insights_cache
    _insights_cache.clear()
    logger.info("Cache limpo")
