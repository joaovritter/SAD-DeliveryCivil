"""
Modelo de Venda
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal

class Sale(BaseModel):
    """Modelo de venda"""
    id: Optional[int] = None
    data: datetime
    produto_id: int = Field(..., description="ID do produto")
    produto_nome: str = Field(..., description="Nome do produto")
    quantidade: int = Field(..., gt=0, description="Quantidade vendida")
    valor_total: Decimal = Field(..., gt=0, description="Valor total da venda")
    valor_unitario: Optional[Decimal] = None
    cliente_id: Optional[int] = None
    
    class Config:
        json_encoders = {
            Decimal: str,
            datetime: lambda v: v.isoformat()
        }

