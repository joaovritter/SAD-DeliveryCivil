"""
Extractor de dados de estoque
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class StockExtractor:
    """Extrator de dados de estoque de CSV"""
    
    def from_csv(self, file_path: str) -> pd.DataFrame:
        """
        Extrai dados de estoque de arquivo CSV
        
        Formato esperado:
        produto_id,produto_nome,quantidade_atual,quantidade_minima,custo_unitario
        """
        try:
            df = pd.read_csv(
                file_path,
                encoding='utf-8',
                dtype={
                    'produto_id': 'int64',
                    'produto_nome': 'string',
                    'quantidade_atual': 'int64',
                    'quantidade_minima': 'int64',
                    'custo_unitario': 'float64'
                }
            )
            
            # Validar colunas obrigatórias
            required_columns = ['produto_id', 'produto_nome', 'quantidade_atual', 'quantidade_minima', 'custo_unitario']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Colunas obrigatórias faltando: {missing}")
            
            # Calcular valor total do estoque
            df['valor_total_estoque'] = df['quantidade_atual'] * df['custo_unitario']
            
            # Validar dados
            if df.empty:
                raise ValueError("Arquivo CSV vazio")
            
            if df['quantidade_atual'].min() < 0:
                raise ValueError("Quantidade atual não pode ser negativa")
            
            if df['quantidade_minima'].min() < 0:
                raise ValueError("Quantidade mínima não pode ser negativa")
            
            if df['custo_unitario'].min() <= 0:
                raise ValueError("Custo unitário deve ser maior que zero")
            
            logger.info(f"✅ Extraídos {len(df)} registros de estoque")
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados de estoque: {str(e)}")
            raise

