"""
FastAPI Application - DeliveryCivil SAD
Sistema de Apoio à Decisão para análise de vendas, estoque e promoções
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from app.api.routes import datasets, analytics, reports
from app.config import settings
from app.utils.logger import setup_logging

# Configurar logging
setup_logging()

# Carregar variáveis de ambiente
load_dotenv()

# Criar aplicação FastAPI
app = FastAPI(
    title="DeliveryCivil SAD API",
    description="API para Sistema de Apoio à Decisão - Análise de Vendas, Estoque e Promoções",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(datasets.router, prefix="/api", tags=["Datasets"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "DeliveryCivil SAD API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global de exceções"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro interno: {str(exc)}"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

