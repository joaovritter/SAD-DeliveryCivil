"""
Modelo de Estoque
"""
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class Stock(BaseModel):
    """Modelo de estoque"""
    produto_id: int = Field(..., description="ID do produto")
    produto_nome: str = Field(..., description="Nome do produto")
    quantidade_atual: int = Field(..., ge=0, description="Quantidade atual em estoque")
    quantidade_minima: int = Field(..., ge=0, description="Quantidade mínima de estoque")
    custo_unitario: Decimal = Field(..., gt=0, description="Custo unitário")
    valor_total_estoque: Optional[Decimal] = None
    
    class Config:
        json_encoders = {
            Decimal: str
        }

