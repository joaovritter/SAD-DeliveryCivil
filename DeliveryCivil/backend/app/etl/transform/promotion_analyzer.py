"""
Analisador de produtos para promoção
"""
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PromotionAnalyzer:
    """Analisa produtos para identificar oportunidades de promoção"""
    
    def analyze(self, sales_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisa produtos e identifica os melhores candidatos para promoção
        
        Regras de Negócio:
        - RF-02: Produtos "encalhados" (pouca ou nenhuma venda nos últimos 90 dias)
        - SE (vendas_30d < 5) E (estoque > 20) ENTÃO Sugerir_Promoção(desconto=15%)
        - Produtos com estoque excedente
        """
        try:
            # Data atual (usar a data mais recente das vendas)
            data_atual = sales_df['data'].max() if not sales_df.empty else datetime.now()
            data_30d_atras = data_atual - timedelta(days=30)
            data_90d_atras = data_atual - timedelta(days=90)
            
            # Filtrar vendas dos últimos 30 e 90 dias
            vendas_30d = sales_df[sales_df['data'] >= data_30d_atras]
            vendas_90d = sales_df[sales_df['data'] >= data_90d_atras]
            
            # Calcular métricas de vendas por produto (todos os tempos)
            sales_metrics_all = sales_df.groupby('produto_id').agg({
                'quantidade': ['sum', 'mean', 'count'],
                'valor_total': 'sum',
                'valor_unitario': 'mean'
            }).reset_index()
            
            sales_metrics_all.columns = [
                'produto_id',
                'total_vendido',
                'media_vendida',
                'frequencia_vendas',
                'receita_total',
                'preco_medio'
            ]
            
            # Calcular vendas dos últimos 30 dias
            vendas_30d_metrics = vendas_30d.groupby('produto_id').agg({
                'quantidade': 'sum',
                'valor_total': 'sum'
            }).reset_index()
            vendas_30d_metrics.columns = ['produto_id', 'vendas_30d_quantidade', 'vendas_30d_receita']
            
            # Calcular vendas dos últimos 90 dias
            vendas_90d_metrics = vendas_90d.groupby('produto_id').agg({
                'quantidade': 'sum',
                'valor_total': 'sum'
            }).reset_index()
            vendas_90d_metrics.columns = ['produto_id', 'vendas_90d_quantidade', 'vendas_90d_receita']
            
            # Contar número de vendas (transações) nos últimos 30 dias
            vendas_30d_count = vendas_30d.groupby('produto_id').size().reset_index(name='vendas_30d')
            
            # Merge de todas as métricas
            sales_metrics = sales_metrics_all.merge(
                vendas_30d_metrics,
                on='produto_id',
                how='left'
            ).merge(
                vendas_90d_metrics,
                on='produto_id',
                how='left'
            ).merge(
                vendas_30d_count,
                on='produto_id',
                how='left'
            )
            
            # Merge de dados primeiro
            analysis = stock_df.merge(
                sales_metrics,
                on='produto_id',
                how='left'
            )
            
            # Preencher valores NaN de produtos sem vendas
            analysis['total_vendido'] = analysis['total_vendido'].fillna(0)
            analysis['media_vendida'] = analysis['media_vendida'].fillna(0)
            analysis['frequencia_vendas'] = analysis['frequencia_vendas'].fillna(0)
            analysis['receita_total'] = analysis['receita_total'].fillna(0)
            analysis['preco_medio'] = analysis['preco_medio'].fillna(analysis['custo_unitario'] * 1.5)
            analysis['vendas_30d_quantidade'] = analysis['vendas_30d_quantidade'].fillna(0)
            analysis['vendas_30d_receita'] = analysis['vendas_30d_receita'].fillna(0)
            analysis['vendas_30d'] = analysis['vendas_30d'].fillna(0)
            analysis['vendas_90d_quantidade'] = analysis['vendas_90d_quantidade'].fillna(0)
            analysis['vendas_90d_receita'] = analysis['vendas_90d_receita'].fillna(0)
            
            # Calcular métricas de estoque
            analysis['dias_estoque'] = (
                analysis['quantidade_atual'] / 
                (analysis['media_vendida'] + 0.001)
            )
            analysis['margem_lucro'] = (
                (analysis['preco_medio'] - analysis['custo_unitario']) / 
                (analysis['custo_unitario'] + 0.001) * 100
            )
            
            # Aplicar regras de negócio
            # RF-02: Produtos "encalhados" (pouca ou nenhuma venda nos últimos 90 dias)
            analysis['encalhado'] = analysis['vendas_90d_quantidade'] <= 0
            
            # Regra: SE (vendas_30d < 5) E (estoque > 20) ENTÃO Sugerir_Promoção(desconto=15%)
            analysis['atende_regra_promocao'] = (
                (analysis['vendas_30d'] < 5) & 
                (analysis['quantidade_atual'] > 20)
            )
            
            # Produtos com estoque excedente (estoque muito acima do necessário)
            # Considerar excedente se estoque > 3x a média de vendas mensais
            vendas_mensais_estimadas = analysis['vendas_30d_quantidade']
            analysis['estoque_excedente'] = analysis['quantidade_atual'] > (vendas_mensais_estimadas * 3)
            
            # Calcular desconto sugerido baseado nas regras
            analysis['desconto_sugerido'] = 0.0
            analysis.loc[analysis['atende_regra_promocao'], 'desconto_sugerido'] = 15.0
            analysis.loc[analysis['encalhado'], 'desconto_sugerido'] = 20.0  # Desconto maior para encalhados
            analysis.loc[
                (analysis['estoque_excedente']) & (analysis['desconto_sugerido'] == 0),
                'desconto_sugerido'
            ] = 10.0
            
            # Calcular score de promoção
            # Score = (dias_estoque * 0.4) + (margem_lucro * 0.3) + (baixa_frequencia * 0.3)
            max_freq = analysis['frequencia_vendas'].max()
            max_dias = analysis['dias_estoque'].max()
            max_margem = analysis['margem_lucro'].max()
            
            # Normalizar com proteção contra divisão por zero
            if max_freq > 0:
                analysis['frequencia_normalizada'] = 1 - (analysis['frequencia_vendas'] / max_freq)
            else:
                analysis['frequencia_normalizada'] = 1.0  # Todos têm baixa frequência
            
            if max_dias > 0 and max_margem > 0:
                analysis['score_promocao'] = (
                    (analysis['dias_estoque'] / max_dias * 0.4) +
                    (analysis['margem_lucro'] / max_margem * 0.3) +
                    (analysis['frequencia_normalizada'] * 0.3)
                )
            elif max_dias > 0:
                analysis['score_promocao'] = (
                    (analysis['dias_estoque'] / max_dias * 0.5) +
                    (analysis['frequencia_normalizada'] * 0.5)
                )
            elif max_margem > 0:
                analysis['score_promocao'] = (
                    (analysis['margem_lucro'] / max_margem * 0.5) +
                    (analysis['frequencia_normalizada'] * 0.5)
                )
            else:
                # Se não há dados suficientes, usar apenas frequência
                analysis['score_promocao'] = analysis['frequencia_normalizada']
            
            # Adicionar recomendações baseadas nas regras de negócio
            def classificar_recomendacao(row):
                if row['encalhado']:
                    return 'Alta'  # Produtos encalhados têm alta prioridade
                elif row['atende_regra_promocao']:
                    return 'Alta'  # Atende regra específica
                elif row['estoque_excedente']:
                    return 'Média'
                elif row['score_promocao'] > 0.7:
                    return 'Alta'
                elif row['score_promocao'] > 0.4:
                    return 'Média'
                else:
                    return 'Baixa'
            
            analysis['recomendacao_promocao'] = analysis.apply(classificar_recomendacao, axis=1)
            
            # Adicionar motivo da recomendação
            def motivo_recomendacao(row):
                motivos = []
                if row['encalhado']:
                    motivos.append('Encalhado (sem vendas em 90 dias)')
                if row['atende_regra_promocao']:
                    motivos.append(f'Poucas vendas (30d: {int(row["vendas_30d"])}) e estoque alto ({int(row["quantidade_atual"])})')
                if row['estoque_excedente']:
                    motivos.append('Estoque excedente')
                if not motivos:
                    motivos.append('Score alto de promoção')
                return ' | '.join(motivos)
            
            analysis['motivo_recomendacao'] = analysis.apply(motivo_recomendacao, axis=1)
            
            # Ordenar: primeiro encalhados, depois por score
            analysis['prioridade'] = analysis.apply(
                lambda x: 3 if x['encalhado'] else (2 if x['atende_regra_promocao'] else (1 if x['estoque_excedente'] else 0)),
                axis=1
            )
            analysis = analysis.sort_values(['prioridade', 'score_promocao'], ascending=[False, False])
            
            # Selecionar colunas relevantes
            result = analysis[[
                'produto_id',
                'produto_nome',
                'quantidade_atual',
                'dias_estoque',
                'margem_lucro',
                'preco_medio',
                'custo_unitario',
                'frequencia_vendas',
                'vendas_30d',
                'vendas_30d_quantidade',
                'vendas_90d_quantidade',
                'encalhado',
                'estoque_excedente',
                'desconto_sugerido',
                'score_promocao',
                'recomendacao_promocao',
                'motivo_recomendacao'
            ]]
            
            logger.info(f"✅ Análise de promoção concluída: {len(result)} produtos analisados")
            
            return result.fillna(0)
            
        except Exception as e:
            logger.error(f"Erro na análise de promoção: {str(e)}")
            raise

