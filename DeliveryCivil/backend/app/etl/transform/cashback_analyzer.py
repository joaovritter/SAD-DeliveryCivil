"""
Analisador de produtos para cashback
"""
import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class CashbackAnalyzer:
    """Analisa produtos para identificar oportunidades de cashback"""
    
    def analyze(self, sales_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisa produtos e identifica os melhores candidatos para cashback
        
        Critérios:
        - Alta margem de lucro
        - Alta frequência de compra
        - Produtos estratégicos
        """
        try:
            # Calcular métricas de vendas por produto
            sales_metrics = sales_df.groupby('produto_id').agg({
                'quantidade': ['sum', 'count'],
                'valor_total': 'sum',
                'valor_unitario': 'mean',
                'cliente_id': 'nunique'
            }).reset_index()
            
            sales_metrics.columns = [
                'produto_id',
                'total_vendido',
                'frequencia_vendas',
                'receita_total',
                'preco_medio',
                'clientes_unicos'
            ]
            
            # Calcular margem de lucro
            analysis = stock_df.merge(
                sales_metrics,
                on='produto_id',
                how='left'
            )
            
            analysis['margem_lucro'] = (
                (analysis['preco_medio'] - analysis['custo_unitario']) / 
                analysis['custo_unitario'] * 100
            )
            
            # Calcular ticket médio do produto
            analysis['ticket_medio'] = (
                analysis['receita_total'] / 
                (analysis['frequencia_vendas'] + 0.001)
            )
            
            # Calcular ROI potencial do cashback
            # Assumindo cashback de 5% e aumento de 20% nas vendas
            cashback_rate = 0.05
            sales_increase = 0.20
            analysis['roi_cashback'] = (
                (analysis['margem_lucro'] * (1 + sales_increase)) - 
                (cashback_rate * 100)
            )
            
            # Preencher valores NaN de produtos sem vendas
            analysis['total_vendido'] = analysis['total_vendido'].fillna(0)
            analysis['frequencia_vendas'] = analysis['frequencia_vendas'].fillna(0)
            analysis['receita_total'] = analysis['receita_total'].fillna(0)
            analysis['preco_medio'] = analysis['preco_medio'].fillna(analysis['custo_unitario'] * 1.5)
            analysis['clientes_unicos'] = analysis['clientes_unicos'].fillna(0)
            analysis['margem_lucro'] = analysis['margem_lucro'].fillna(0)
            analysis['roi_cashback'] = analysis['roi_cashback'].fillna(0)
            
            # Normalizar métricas para score com proteção contra divisão por zero
            max_margem = analysis['margem_lucro'].max()
            max_freq = analysis['frequencia_vendas'].max()
            max_clientes = analysis['clientes_unicos'].max()
            max_roi = analysis['roi_cashback'].max()
            
            if max_margem > 0:
                analysis['margem_normalizada'] = analysis['margem_lucro'] / max_margem
            else:
                analysis['margem_normalizada'] = 0
            
            if max_freq > 0:
                analysis['frequencia_normalizada'] = analysis['frequencia_vendas'] / max_freq
            else:
                analysis['frequencia_normalizada'] = 0
            
            if max_clientes > 0:
                analysis['clientes_normalizado'] = analysis['clientes_unicos'] / max_clientes
            else:
                analysis['clientes_normalizado'] = 0
            
            if max_roi > 0:
                analysis['roi_normalizado'] = analysis['roi_cashback'] / max_roi
            else:
                analysis['roi_normalizado'] = 0
            
            # Calcular score de cashback
            # Score = (margem * 0.4) + (frequência * 0.3) + (clientes * 0.2) + (ROI * 0.1)
            analysis['score_cashback'] = (
                (analysis['margem_normalizada'] * 0.4) +
                (analysis['frequencia_normalizada'] * 0.3) +
                (analysis['clientes_normalizado'] * 0.2) +
                (analysis['roi_normalizado'] * 0.1)
            )
            
            # Adicionar recomendações
            analysis['recomendacao_cashback'] = analysis['score_cashback'].apply(
                lambda x: 'Alta' if x > 0.7 else 'Média' if x > 0.4 else 'Baixa'
            )
            
            # Sugerir percentual de cashback baseado no score
            analysis['cashback_sugerido'] = analysis['score_cashback'].apply(
                lambda x: 10 if x > 0.7 else 5 if x > 0.4 else 2
            )
            
            # Ordenar por score
            analysis = analysis.sort_values('score_cashback', ascending=False)
            
            # Selecionar colunas relevantes
            result = analysis[[
                'produto_id',
                'produto_nome',
                'margem_lucro',
                'frequencia_vendas',
                'clientes_unicos',
                'ticket_medio',
                'preco_medio',
                'roi_cashback',
                'score_cashback',
                'recomendacao_cashback',
                'cashback_sugerido'
            ]]
            
            logger.info(f"✅ Análise de cashback concluída: {len(result)} produtos analisados")
            
            return result.fillna(0)
            
        except Exception as e:
            logger.error(f"Erro na análise de cashback: {str(e)}")
            raise

