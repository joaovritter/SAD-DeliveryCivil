"""
Extractor de dados de compras
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PurchasesExtractor:
    """Extrator de dados de compras de CSV"""
    
    def from_csv(self, file_path: str) -> pd.DataFrame:
        """
        Extrai dados de compras de arquivo CSV
        
        Formato esperado:
        data,produto_id,fornecedor,quantidade,custo_total
        """
        try:
            df = pd.read_csv(
                file_path,
                encoding='utf-8',
                parse_dates=['data'],
                dtype={
                    'produto_id': 'int64',
                    'fornecedor': 'string',
                    'quantidade': 'int64',
                    'custo_total': 'float64'
                }
            )
            
            # Validar colunas obrigatórias
            required_columns = ['data', 'produto_id', 'fornecedor', 'quantidade', 'custo_total']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Colunas obrigatórias faltando: {missing}")
            
            # Calcular custo unitário
            df['custo_unitario'] = df['custo_total'] / df['quantidade']
            
            # Validar dados
            if df.empty:
                raise ValueError("Arquivo CSV vazio")
            
            if df['quantidade'].min() <= 0:
                raise ValueError("Quantidade deve ser maior que zero")
            
            if df['custo_total'].min() <= 0:
                raise ValueError("Custo total deve ser maior que zero")
            
            logger.info(f"✅ Extraídos {len(df)} registros de compras")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados de compras: {str(e)}")
            raise

