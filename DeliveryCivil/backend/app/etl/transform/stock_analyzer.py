"""
Analisador de estoque para reposição
"""
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class StockAnalyzer:
    """Analisa estoque para identificar necessidade de reposição"""
    
    def analyze(self, sales_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisa estoque e identifica produtos que precisam ser repostos
        
        Critérios:
        - Estoque abaixo do mínimo
        - Velocidade de venda alta
        - Previsão de ruptura
        """
        try:
            # Data atual (usar a data mais recente das vendas)
            sales_df_copy = sales_df.copy()
            sales_df_copy['data'] = pd.to_datetime(sales_df_copy['data'])
            data_atual = sales_df_copy['data'].max() if not sales_df_copy.empty else datetime.now()
            data_7d_atras = data_atual - timedelta(days=7)
            
            # Filtrar vendas dos últimos 7 dias para alertas de oportunidade
            vendas_7d = sales_df_copy[sales_df_copy['data'] >= data_7d_atras]
            
            # Calcular vendas dos últimos 7 dias por produto
            vendas_7d_metrics = vendas_7d.groupby('produto_id').agg({
                'quantidade': 'sum',
                'valor_total': 'sum'
            }).reset_index()
            vendas_7d_metrics.columns = ['produto_id', 'vendas_7d_quantidade', 'vendas_7d_receita']
            
            # Contar número de transações nos últimos 7 dias
            vendas_7d_count = vendas_7d.groupby('produto_id').size().reset_index(name='vendas_7d')
            
            # Calcular velocidade de venda (unidades por dia) - histórico completo
            daily_sales = sales_df_copy.groupby(['produto_id', sales_df_copy['data'].dt.date]).agg({
                'quantidade': 'sum'
            }).reset_index()
            
            # Calcular média diária de vendas
            avg_daily_sales = daily_sales.groupby('produto_id')['quantidade'].mean().reset_index()
            avg_daily_sales.columns = ['produto_id', 'vendas_media_diaria']
            
            # Merge com estoque
            analysis = stock_df.merge(
                avg_daily_sales,
                on='produto_id',
                how='left'
            ).merge(
                vendas_7d_metrics,
                on='produto_id',
                how='left'
            ).merge(
                vendas_7d_count,
                on='produto_id',
                how='left'
            )
            
            # Preencher NaN com 0
            analysis['vendas_media_diaria'] = analysis['vendas_media_diaria'].fillna(0)
            analysis['vendas_7d_quantidade'] = analysis['vendas_7d_quantidade'].fillna(0)
            analysis['vendas_7d_receita'] = analysis['vendas_7d_receita'].fillna(0)
            analysis['vendas_7d'] = analysis['vendas_7d'].fillna(0)
            
            # Calcular dias até ruptura
            analysis['dias_ate_ruptura'] = (
                analysis['quantidade_atual'] / 
                (analysis['vendas_media_diaria'] + 0.001)
            )
            
            # Calcular quantidade sugerida para reposição
            # Sugestão = (vendas_media_diaria * lead_time) + estoque_minimo - estoque_atual
            lead_time = 7  # dias (pode ser configurável)
            analysis['quantidade_sugerida'] = (
                (analysis['vendas_media_diaria'] * lead_time) + 
                analysis['quantidade_minima'] - 
                analysis['quantidade_atual']
            )
            analysis['quantidade_sugerida'] = analysis['quantidade_sugerida'].clip(lower=0)
            
            # Calcular custo de reposição
            analysis['custo_reposicao'] = (
                analysis['quantidade_sugerida'] * 
                analysis['custo_unitario']
            )
            
            # Classificar urgência
            analysis['urgencia_reposicao'] = analysis.apply(
                lambda row: self._classify_urgency(row),
                axis=1
            )
            
            # Calcular score de reposição
            analysis['score_reposicao'] = analysis.apply(
                lambda row: self._calculate_reorder_score(row),
                axis=1
            )
            
            # RF-06: Gerar alertas de oportunidade
            # Ex: "Item X teve 30 compras no período de 7 dias. Considere uma reposição de estoque"
            def gerar_alerta(row):
                alertas = []
                
                # Alerta de alta demanda recente
                if row['vendas_7d'] >= 20:  # 20 ou mais transações em 7 dias
                    alertas.append(
                        f"⚠️ Alta demanda: {int(row['vendas_7d'])} compras nos últimos 7 dias. "
                        f"Considere uma reposição de estoque."
                    )
                elif row['vendas_7d'] >= 10:  # 10-19 transações
                    alertas.append(
                        f"📈 Demanda crescente: {int(row['vendas_7d'])} compras nos últimos 7 dias. "
                        f"Monitore o estoque."
                    )
                
                # Alerta de estoque baixo com alta venda
                if row['quantidade_atual'] < row['quantidade_minima'] and row['vendas_7d_quantidade'] > 0:
                    alertas.append(
                        f"🔴 Estoque crítico: {int(row['quantidade_atual'])} unidades "
                        f"(mínimo: {int(row['quantidade_minima'])}). "
                        f"Reposição urgente recomendada."
                    )
                
                # Alerta de ruptura iminente
                if row['dias_ate_ruptura'] < 7 and row['vendas_media_diaria'] > 0:
                    alertas.append(
                        f"⏰ Ruptura prevista em {row['dias_ate_ruptura']:.1f} dias. "
                        f"Repor {int(row['quantidade_sugerida'])} unidades."
                    )
                
                return ' | '.join(alertas) if alertas else None
            
            analysis['alerta_oportunidade'] = analysis.apply(gerar_alerta, axis=1)
            
            # Adicionar recomendações
            analysis['recomendacao_reposicao'] = analysis.apply(
                lambda x: f"Repor {x['quantidade_sugerida']} unidades" if x['quantidade_sugerida'] > 0 else "Estoque adequado",
                axis=1
            )
            
            # Ordenar por urgência e score
            analysis = analysis.sort_values(
                ['urgencia_reposicao', 'score_reposicao'],
                ascending=[False, False]
            )
            
            # Selecionar colunas relevantes
            result = analysis[[
                'produto_id',
                'produto_nome',
                'quantidade_atual',
                'quantidade_minima',
                'vendas_media_diaria',
                'vendas_7d',
                'vendas_7d_quantidade',
                'vendas_7d_receita',
                'dias_ate_ruptura',
                'quantidade_sugerida',
                'custo_reposicao',
                'custo_unitario',
                'urgencia_reposicao',
                'score_reposicao',
                'recomendacao_reposicao',
                'alerta_oportunidade'
            ]]
            
            logger.info(f"✅ Análise de estoque concluída: {len(result)} produtos analisados")
            
            return result.fillna(0)
            
        except Exception as e:
            logger.error(f"Erro na análise de estoque: {str(e)}")
            raise
    
    def _classify_urgency(self, row) -> str:
        """
        Classifica urgência de reposição baseado em percentual acima do estoque mínimo
        
        Regras:
        - Crítica: abaixo do estoque mínimo
        - Alta: até 10% acima do estoque mínimo
        - Média: até 40% acima do estoque mínimo
        - Baixa: mais de 40% acima do estoque mínimo
        """
        quantidade_atual = row['quantidade_atual']
        quantidade_minima = row['quantidade_minima']
        
        # Calcular percentual acima do mínimo
        if quantidade_atual < quantidade_minima:
            return 'Crítica'
        elif quantidade_atual <= quantidade_minima * 1.1:  # Até 10% acima
            return 'Alta'
        elif quantidade_atual <= quantidade_minima * 1.4:  # Até 40% acima
            return 'Média'
        else:  # Mais de 40% acima
            return 'Baixa'
    
    def _calculate_reorder_score(self, row) -> float:
        """
        Calcula score de reposição (0-1) baseado na urgência
        
        Score reflete a necessidade de reposição:
        - Crítica: 1.0 (máxima urgência)
        - Alta: 0.8
        - Média: 0.5
        - Baixa: 0.2
        """
        quantidade_atual = row['quantidade_atual']
        quantidade_minima = row['quantidade_minima']
        
        if quantidade_atual < quantidade_minima:
            return 1.0  # Crítica
        elif quantidade_atual <= quantidade_minima * 1.1:
            return 0.8  # Alta
        elif quantidade_atual <= quantidade_minima * 1.4:
            return 0.5  # Média
        else:
            return 0.2  # Baixa

