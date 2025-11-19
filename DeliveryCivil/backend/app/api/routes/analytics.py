"""
Endpoints para análises de negócio
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import pandas as pd
import logging
from pathlib import Path

from app.config import settings
from app.etl.extract.sales_extractor import SalesExtractor
from app.etl.extract.stock_extractor import StockExtractor
from app.etl.transform.promotion_analyzer import PromotionAnalyzer
from app.etl.transform.stock_analyzer import StockAnalyzer
from app.etl.transform.cashback_analyzer import CashbackAnalyzer
from app.etl.load.powerbi_loader import PowerBILoader

logger = logging.getLogger(__name__)
router = APIRouter()

def _load_latest_datasets():
    """Carrega os datasets mais recentes"""
    raw_dir = Path(settings.DATA_RAW_DIR)
    
    # Encontrar arquivos mais recentes
    sales_files = list(raw_dir.glob("vendas_*.csv"))
    stock_files = list(raw_dir.glob("estoque_*.csv"))
    
    if not sales_files:
        raise HTTPException(status_code=404, detail="Dataset de vendas não encontrado")
    if not stock_files:
        raise HTTPException(status_code=404, detail="Dataset de estoque não encontrado")
    
    # Pegar arquivo mais recente
    latest_sales = max(sales_files, key=lambda p: p.stat().st_mtime)
    latest_stock = max(stock_files, key=lambda p: p.stat().st_mtime)
    
    # Carregar dados
    sales_extractor = SalesExtractor()
    stock_extractor = StockExtractor()
    
    sales_df = sales_extractor.from_csv(str(latest_sales))
    stock_df = stock_extractor.from_csv(str(latest_stock))
    
    return sales_df, stock_df

@router.get("/analytics/promotion")
async def analyze_promotion(save_to_powerbi: bool = False):
    """
    Analisa produtos para identificar oportunidades de promoção
    
    Returns:
        Lista de produtos recomendados para promoção
    """
    try:
        sales_df, stock_df = _load_latest_datasets()
        
        analyzer = PromotionAnalyzer()
        result_df = analyzer.analyze(sales_df, stock_df)
        
        # Converter para dict
        result = result_df.to_dict("records")
        
        # Salvar para Power BI se solicitado
        if save_to_powerbi:
            loader = PowerBILoader()
            loader.save_for_powerbi(result_df, "promocao_analise")
        
        return {
            "message": "Análise de promoção concluída",
            "total_products": len(result),
            "products": result[:20]  # Top 20
        }
    except Exception as e:
        logger.error(f"Erro na análise de promoção: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@router.get("/analytics/stock")
async def analyze_stock(save_to_powerbi: bool = False):
    """
    Analisa estoque para identificar necessidade de reposição
    
    Returns:
        Lista de produtos que precisam ser repostos
    """
    try:
        sales_df, stock_df = _load_latest_datasets()
        
        analyzer = StockAnalyzer()
        result_df = analyzer.analyze(sales_df, stock_df)
        
        result = result_df.to_dict("records")
        
        if save_to_powerbi:
            loader = PowerBILoader()
            loader.save_for_powerbi(result_df, "estoque_analise")
        
        # Contar produtos por urgência
        critical = [r for r in result if r['urgencia_reposicao'] == 'Crítica']
        high = [r for r in result if r['urgencia_reposicao'] == 'Alta']
        medium = [r for r in result if r['urgencia_reposicao'] == 'Média']
        
        # Retornar todos os produtos (não apenas críticos) para exibição completa
        # Ordenados por urgência (Crítica → Alta → Média → Baixa)
        return {
            "message": "Análise de estoque concluída",
            "total_products": len(result),
            "critical_products": len(critical),
            "high_urgency_products": len(high),
            "medium_urgency_products": len(medium),
            "products": result  # Todos os produtos ordenados por urgência
        }
    except Exception as e:
        logger.error(f"Erro na análise de estoque: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@router.get("/analytics/cashback")
async def analyze_cashback(save_to_powerbi: bool = False):
    """
    Analisa produtos para identificar oportunidades de cashback
    
    Returns:
        Lista de produtos recomendados para cashback
    """
    try:
        sales_df, stock_df = _load_latest_datasets()
        
        analyzer = CashbackAnalyzer()
        result_df = analyzer.analyze(sales_df, stock_df)
        
        result = result_df.to_dict("records")
        
        if save_to_powerbi:
            loader = PowerBILoader()
            loader.save_for_powerbi(result_df, "cashback_analise")
        
        return {
            "message": "Análise de cashback concluída",
            "total_products": len(result),
            "products": result[:20]  # Top 20
        }
    except Exception as e:
        logger.error(f"Erro na análise de cashback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

@router.get("/analytics/summary")
async def get_analytics_summary():
    """
    Retorna resumo de todas as análises
    """
    try:
        sales_df, stock_df = _load_latest_datasets()
        
        # Análises rápidas
        promotion_analyzer = PromotionAnalyzer()
        stock_analyzer = StockAnalyzer()
        cashback_analyzer = CashbackAnalyzer()
        
        promotion_df = promotion_analyzer.analyze(sales_df, stock_df)
        stock_df_result = stock_analyzer.analyze(sales_df, stock_df)
        cashback_df = cashback_analyzer.analyze(sales_df, stock_df)
        
        # Garantir que as colunas existem e não são NaN antes de filtrar
        promotion_df['recomendacao_promocao'] = promotion_df['recomendacao_promocao'].fillna('Baixa')
        stock_df_result['urgencia_reposicao'] = stock_df_result['urgencia_reposicao'].fillna('Baixa')
        cashback_df['recomendacao_cashback'] = cashback_df['recomendacao_cashback'].fillna('Baixa')
        
        # Calcular métricas com segurança
        promotion_high = promotion_df[promotion_df['recomendacao_promocao'] == 'Alta']
        stock_critical = stock_df_result[stock_df_result['urgencia_reposicao'] == 'Crítica']
        cashback_high = cashback_df[cashback_df['recomendacao_cashback'] == 'Alta']
        
        # Calcular valor total de vendas (soma dos valores)
        total_revenue = float(sales_df['valor_total'].sum()) if 'valor_total' in sales_df.columns else 0.0
        
        # Garantir ordenação correta antes de pegar top 5
        # Promotion já está ordenado por score_promocao (desc)
        # Stock já está ordenado por urgência e score
        # Cashback já está ordenado por score_cashback (desc)
        
        # Converter valores NaN para garantir serialização JSON
        def clean_dict(d):
            """Remove NaN e inf dos valores"""
            import math
            cleaned = {}
            for k, v in d.items():
                if isinstance(v, float):
                    if math.isnan(v) or math.isinf(v):
                        cleaned[k] = 0.0
                    else:
                        cleaned[k] = round(v, 2) if abs(v) < 1e10 else 0.0
                else:
                    cleaned[k] = v
            return cleaned
        
        top_promotion = [clean_dict(r) for r in promotion_df.head(5).to_dict("records")]
        top_stock = [clean_dict(r) for r in stock_df_result[stock_df_result['urgencia_reposicao'].isin(['Crítica', 'Alta'])].head(5).to_dict("records")]
        top_cashback = [clean_dict(r) for r in cashback_df.head(5).to_dict("records")]
        
        return {
            "summary": {
                "total_products": int(len(stock_df)),
                "total_sales": int(len(sales_df)),
                "total_revenue": round(total_revenue, 2),
                "promotion_opportunities": int(len(promotion_high)),
                "stock_critical": int(len(stock_critical)),
                "cashback_high": int(len(cashback_high))
            },
            "top_promotion": top_promotion,
            "top_stock": top_stock,
            "top_cashback": top_cashback
        }
    except Exception as e:
        logger.error(f"Erro no resumo de análises: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro na análise: {str(e)}")

