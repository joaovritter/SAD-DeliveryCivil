"""
Endpoints para relatórios Power BI (simplificado - usando iframe público)
"""
from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/reports/health")
async def check_powerbi_config():
    """
    Endpoint de health check para Power BI
    Agora usando iframe público, não precisa de autenticação
    """
    return {
        "configured": True,
        "method": "iframe_public",
        "message": "Power BI usando iframe público - configure a URL no front-end"
    }

