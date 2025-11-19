"""
Extractor de dados de vendas
"""
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SalesExtractor:
    """Extrator de dados de vendas de CSV"""
    
    def from_csv(self, file_path: str) -> pd.DataFrame:
        """
        Extrai dados de vendas de arquivo CSV
        
        Formato esperado:
        data,produto_id,produto_nome,quantidade,valor_total,cliente_id
        """
        try:
            df = pd.read_csv(
                file_path,
                encoding='utf-8',
                parse_dates=['data'],
                dtype={
                    'produto_id': 'int64',
                    'produto_nome': 'string',
                    'quantidade': 'int64',
                    'valor_total': 'float64',
                    'cliente_id': 'Int64'  # Nullable
                }
            )
            
            # Validar colunas obrigatórias
            required_columns = ['data', 'produto_id', 'produto_nome', 'quantidade', 'valor_total']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Colunas obrigatórias faltando: {missing}")
            
            # Calcular valor unitário
            df['valor_unitario'] = df['valor_total'] / df['quantidade']
            
            # Validar dados
            if df.empty:
                raise ValueError("Arquivo CSV vazio")
            
            if df['quantidade'].min() <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
            
            if df['valor_total'].min() <= 0:
                raise ValueError("Valor total deve ser maior que zero")
            
            logger.info(f"✅ Extraídos {len(df)} registros de vendas")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados de vendas: {str(e)}")
            raise

