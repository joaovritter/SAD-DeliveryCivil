"""
Endpoints para upload e processamento de datasets
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

from app.config import settings
from app.etl.extract.sales_extractor import SalesExtractor
from app.etl.extract.stock_extractor import StockExtractor
from app.etl.extract.purchases_extractor import PurchasesExtractor

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/datasets/upload/sales")
async def upload_sales_dataset(file: UploadFile = File(...)):
    """
    Upload de dataset de vendas (CSV)
    
    Formato esperado:
    data,produto_id,produto_nome,quantidade,valor_total,cliente_id
    """
    try:
        logger.info(f"📥 Recebendo arquivo de vendas: {file.filename}")
        
        # Validar extensão
        if not file.filename or not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
        
        # Salvar arquivo temporariamente
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = Path(settings.DATA_RAW_DIR) / f"vendas_{timestamp}.csv"
        
        # Garantir que o diretório existe
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        logger.info(f"📦 Arquivo recebido: {len(content)} bytes")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"💾 Arquivo salvo em: {file_path}")
        
        # Extrair e validar dados
        extractor = SalesExtractor()
        df = extractor.from_csv(str(file_path))
        
        # Processar dados
        records = df.to_dict("records")
        
        logger.info(f"✅ Dataset de vendas processado: {len(records)} registros")
        
        return {
            "message": "Dataset de vendas processado com sucesso",
            "records_count": len(records),
            "file_path": str(file_path),
            "sample": records[:5] if len(records) > 0 else []
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao processar dataset de vendas: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo: {str(e)}")

@router.post("/datasets/upload/stock")
async def upload_stock_dataset(file: UploadFile = File(...)):
    """
    Upload de dataset de estoque (CSV)
    
    Formato esperado:
    produto_id,produto_nome,quantidade_atual,quantidade_minima,custo_unitario
    """
    try:
        logger.info(f"📥 Recebendo arquivo de estoque: {file.filename}")
        
        if not file.filename or not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = Path(settings.DATA_RAW_DIR) / f"estoque_{timestamp}.csv"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        logger.info(f"📦 Arquivo recebido: {len(content)} bytes")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"💾 Arquivo salvo em: {file_path}")
        
        extractor = StockExtractor()
        df = extractor.from_csv(str(file_path))
        
        records = df.to_dict("records")
        
        logger.info(f"✅ Dataset de estoque processado: {len(records)} registros")
        
        return {
            "message": "Dataset de estoque processado com sucesso",
            "records_count": len(records),
            "file_path": str(file_path),
            "sample": records[:5] if len(records) > 0 else []
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao processar dataset de estoque: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo: {str(e)}")

@router.post("/datasets/upload/purchases")
async def upload_purchases_dataset(file: UploadFile = File(...)):
    """
    Upload de dataset de compras (CSV)
    
    Formato esperado:
    data,produto_id,fornecedor,quantidade,custo_total
    """
    try:
        logger.info(f"📥 Recebendo arquivo de compras: {file.filename}")
        
        if not file.filename or not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = Path(settings.DATA_RAW_DIR) / f"compras_{timestamp}.csv"
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = await file.read()
        logger.info(f"📦 Arquivo recebido: {len(content)} bytes")
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"💾 Arquivo salvo em: {file_path}")
        
        extractor = PurchasesExtractor()
        df = extractor.from_csv(str(file_path))
        
        records = df.to_dict("records")
        
        logger.info(f"✅ Dataset de compras processado: {len(records)} registros")
        
        return {
            "message": "Dataset de compras processado com sucesso",
            "records_count": len(records),
            "file_path": str(file_path),
            "sample": records[:5] if len(records) > 0 else []
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erro ao processar dataset de compras: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Erro ao processar arquivo: {str(e)}")

@router.get("/datasets/list")
async def list_datasets():
    """Lista todos os datasets processados"""
    raw_dir = Path(settings.DATA_RAW_DIR)
    files = []
    
    for file_path in raw_dir.glob("*.csv"):
        files.append({
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        })
    
    return {
        "datasets": files,
        "count": len(files)
    }

