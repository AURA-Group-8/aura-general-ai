from fastapi import APIRouter, Query, Body
from models.insight_model import InsightRequest, InsightResponse, Insight
from services.insight_service import get_insights_with_pagination, clear_cache
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["insights"])

@router.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "ok",
        "service": "Aura Insights API",
        "version": "1.0.0"
    }

@router.get("/insights", response_model=InsightResponse)
async def get_insights(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=20),
    focus: str = Query(None),
    observations: str = Query(None)
):
    """
    Retorna insights paginados.
    
    - **page**: Página (padrão 1)
    - **page_size**: Itens por página (padrão 5, máx 20)
    - **focus**: Foco customizado (ex: financeiro, retenção)
    - **observations**: Observações adicionais do usuário
    """
    return get_insights_with_pagination(
        page=page,
        page_size=page_size,
        focus=focus,
        observations=observations
    )

@router.post("/insights", response_model=InsightResponse)
async def post_insights(
    request: InsightRequest,
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=20)
):
    """
    Retorna insights paginados com body request (foco e observações).
    """
    return get_insights_with_pagination(
        page=page,
        page_size=page_size,
        focus=request.focus,
        observations=request.observations
    )

@router.get("/insights/categories")
async def get_categories():
    """Lista categorias disponíveis de insights"""
    return {
        "categories": ["finance", "clients", "marketing", "retention", "operations"],
        "priorities": ["low", "medium", "high"]
    }

@router.delete("/cache", tags=["admin"])
async def clear_insights_cache():
    """Limpa cache de insights"""
    clear_cache()
    return {"message": "Cache limpo com sucesso"}
