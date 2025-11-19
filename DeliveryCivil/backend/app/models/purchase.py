"""
Modelo de Compra
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Purchase(BaseModel):
    """Modelo de compra"""
    id: Optional[int] = None
    data: datetime
    produto_id: int = Field(..., description="ID do produto")
    fornecedor: str = Field(..., description="Nome do fornecedor")
    quantidade: int = Field(..., gt=0, description="Quantidade comprada")
    custo_total: Decimal = Field(..., gt=0, description="Custo total da compra")
    custo_unitario: Optional[Decimal] = None
    
    class Config:
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }

