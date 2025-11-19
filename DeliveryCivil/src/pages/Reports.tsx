import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, TrendingUp, Package, Gift, BarChart3 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import BottomNavigation from '@/components/BottomNavigation';
import PowerBiDashboard from '@/components/PowerBiDashboard';
import { analyticsApi, AnalyticsSummary, AnalyticsResponse } from '@/services/api';

const Reports: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('summary');
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [promotionData, setPromotionData] = useState<AnalyticsResponse | null>(null);
  const [stockData, setStockData] = useState<AnalyticsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingPromotion, setLoadingPromotion] = useState(false);
  const [loadingStock, setLoadingStock] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSummary();
  }, []);

  useEffect(() => {
    if (activeTab === 'promotion' && !promotionData) {
      loadPromotionAnalysis();
    }
  }, [activeTab]);

  useEffect(() => {
    if (activeTab === 'stock' && !stockData) {
      loadStockAnalysis();
    }
  }, [activeTab]);

  const loadSummary = async () => {
    try {
      setLoading(true);
      const data = await analyticsApi.getSummary();
      setSummary(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar análises');
    } finally {
      setLoading(false);
    }
  };

  const loadPromotionAnalysis = async () => {
    try {
      setLoadingPromotion(true);
      const data = await analyticsApi.getPromotionAnalysis();
      setPromotionData(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar análise de promoção');
    } finally {
      setLoadingPromotion(false);
    }
  };

  const loadStockAnalysis = async () => {
    try {
      setLoadingStock(true);
      const data = await analyticsApi.getStockAnalysis();
      setStockData(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao carregar análise de estoque');
    } finally {
      setLoadingStock(false);
    }
  };

  if (loading) {
    return (
      <div className="click-obra-container">
        <header className="sticky top-0 z-50 bg-background border-b p-4">
          <div className="flex items-center gap-4">
            <button onClick={() => navigate("/")} className="p-2 -ml-2">
              <ArrowLeft size={24} />
            </button>
            <h1 className="text-xl font-bold">Relatórios e Análises</h1>
          </div>
        </header>
        <main className="pb-32 p-4">
          <div className="text-center py-8">Carregando análises...</div>
        </main>
        <BottomNavigation />
      </div>
    );
  }

  return (
    <div className="click-obra-container">
      <header className="sticky top-0 z-50 bg-background border-b">
        <div className="flex items-center justify-between p-4">
          <div className="flex items-center gap-4">
            <button onClick={() => navigate("/")} className="p-2 -ml-2">
              <ArrowLeft size={24} />
            </button>
            <h1 className="text-xl font-bold">Relatórios e Análises</h1>
          </div>
        </div>
      </header>

      <main className="pb-32 p-4">
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="summary">Resumo</TabsTrigger>
            <TabsTrigger value="promotion">Promoção</TabsTrigger>
            <TabsTrigger value="stock">Estoque</TabsTrigger>
            <TabsTrigger value="powerbi">Power BI</TabsTrigger>
          </TabsList>

          <TabsContent value="summary" className="space-y-4">
            {summary && (
              <>
                <div className="grid grid-cols-2 gap-4">
                  <Card>
                    <CardHeader className="pb-2">
                      <CardDescription>Total de Produtos</CardDescription>
                      <CardTitle className="text-2xl">{summary.summary.total_products.toLocaleString('pt-BR')}</CardTitle>
                    </CardHeader>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardDescription>Total de Vendas</CardDescription>
                      <CardTitle className="text-2xl">{summary.summary.total_sales.toLocaleString('pt-BR')}</CardTitle>
                    </CardHeader>
                  </Card>
                  {summary.summary.total_revenue !== undefined && (
                    <Card>
                      <CardHeader className="pb-2">
                        <CardDescription>Receita Total</CardDescription>
                        <CardTitle className="text-2xl">
                          R$ {summary.summary.total_revenue.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </CardTitle>
                      </CardHeader>
                    </Card>
                  )}
                  <Card>
                    <CardHeader className="pb-2">
                      <CardDescription>Oportunidades de Promoção</CardDescription>
                      <CardTitle className="text-2xl">{summary.summary.promotion_opportunities.toLocaleString('pt-BR')}</CardTitle>
                    </CardHeader>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardDescription>Estoque Crítico</CardDescription>
                      <CardTitle className="text-2xl text-destructive">{summary.summary.stock_critical.toLocaleString('pt-BR')}</CardTitle>
                    </CardHeader>
                  </Card>
                  <Card>
                    <CardHeader className="pb-2">
                      <CardDescription>Cashback Alto</CardDescription>
                      <CardTitle className="text-2xl">{summary.summary.cashback_high.toLocaleString('pt-BR')}</CardTitle>
                    </CardHeader>
                  </Card>
                </div>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Top Produtos para Promoção
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {summary.top_promotion.map((product, idx) => (
                        <div key={idx} className="flex justify-between items-center p-2 border rounded">
                          <div>
                            <div className="font-semibold">{product.produto_nome}</div>
                            <div className="text-sm text-muted-foreground">
                              Score: {product.score_promocao?.toFixed(2)} | 
                              Recomendação: {product.recomendacao_promocao}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Package className="h-5 w-5" />
                      Produtos com Estoque Crítico
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {summary.top_stock.map((product, idx) => (
                        <div key={idx} className="flex justify-between items-center p-2 border rounded">
                          <div>
                            <div className="font-semibold">{product.produto_nome}</div>
                            <div className="text-sm text-muted-foreground">
                              Estoque: {product.quantidade_atual} | 
                              Mínimo: {product.quantidade_minima} | 
                              Urgência: {product.urgencia_reposicao}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Gift className="h-5 w-5" />
                      Top Produtos para Cashback
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      {summary.top_cashback.map((product, idx) => (
                        <div key={idx} className="flex justify-between items-center p-2 border rounded">
                          <div>
                            <div className="font-semibold">{product.produto_nome}</div>
                            <div className="text-sm text-muted-foreground">
                              Score: {product.score_cashback?.toFixed(2)} | 
                              Cashback Sugerido: {product.cashback_sugerido}%
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </>
            )}
          </TabsContent>

          <TabsContent value="promotion" className="space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold">Análise de Promoção</h2>
                <p className="text-sm text-muted-foreground">
                  Produtos recomendados para promoção baseado em estoque parado, margem de lucro e frequência de vendas
                </p>
              </div>
              <Button onClick={loadPromotionAnalysis} disabled={loadingPromotion}>
                <BarChart3 className="h-4 w-4 mr-2" />
                {loadingPromotion ? 'Carregando...' : 'Atualizar'}
              </Button>
            </div>

            {loadingPromotion ? (
              <Card>
                <CardContent className="py-8 text-center">
                  <div className="text-muted-foreground">Carregando análise de promoção...</div>
                </CardContent>
              </Card>
            ) : promotionData ? (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Resumo</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <div className="text-sm text-muted-foreground">Total de Produtos Analisados</div>
                        <div className="text-2xl font-bold">{promotionData.total_products}</div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Produtos Recomendados</div>
                        <div className="text-2xl font-bold text-primary">
                          {promotionData.products.filter((p: any) => p.recomendacao_promocao === 'Alta').length}
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

            <Card>
              <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Produtos Recomendados para Promoção
                    </CardTitle>
                    <CardDescription>
                      Ordenados por score de promoção (maior score = maior prioridade)
                    </CardDescription>
              </CardHeader>
              <CardContent>
                    <div className="space-y-3">
                      {promotionData.products.length === 0 ? (
                        <div className="text-center py-4 text-muted-foreground">
                          Nenhum produto encontrado
                        </div>
                      ) : (
                        promotionData.products.map((product: any, idx: number) => (
                          <div key={idx} className="p-4 border rounded-lg hover:bg-accent/50 transition-colors">
                            <div className="flex justify-between items-start mb-2">
                              <div className="flex-1">
                                <div className="font-semibold text-lg">{product.produto_nome}</div>
                                <div className="text-sm text-muted-foreground mt-1">
                                  ID: {product.produto_id}
                                </div>
                              </div>
                              <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                product.recomendacao_promocao === 'Alta' ? 'bg-red-100 text-red-800' :
                                product.recomendacao_promocao === 'Média' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {product.recomendacao_promocao}
                              </div>
                            </div>
                            {product.motivo_recomendacao && (
                              <div className="mb-3 p-2 bg-blue-50 dark:bg-blue-950 rounded text-sm">
                                <div className="font-semibold text-blue-900 dark:text-blue-100">💡 Motivo:</div>
                                <div className="text-blue-800 dark:text-blue-200">{product.motivo_recomendacao}</div>
                              </div>
                            )}
                            {product.desconto_sugerido > 0 && (
                              <div className="mb-3 p-3 bg-green-50 dark:bg-green-950 rounded-lg border border-green-200 dark:border-green-800">
                                <div className="flex items-center gap-2">
                                  <span className="text-2xl font-bold text-green-600 dark:text-green-400">
                                    {product.desconto_sugerido}%
                                  </span>
                                  <span className="text-sm text-green-700 dark:text-green-300">Desconto Sugerido</span>
                                </div>
                              </div>
                            )}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-3 text-sm">
                              <div>
                                <div className="text-muted-foreground">Score</div>
                                <div className="font-semibold">{(product.score_promocao || 0).toFixed(2)}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Estoque Atual</div>
                                <div className="font-semibold">{product.quantidade_atual || 0}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Vendas (30 dias)</div>
                                <div className="font-semibold">{product.vendas_30d || 0}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Vendas (90 dias)</div>
                                <div className="font-semibold">{product.vendas_90d_quantidade || 0}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Dias de Estoque</div>
                                <div className="font-semibold">{(product.dias_estoque || 0).toFixed(1)}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Margem de Lucro</div>
                                <div className="font-semibold">{(product.margem_lucro || 0).toFixed(1)}%</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Preço Médio</div>
                                <div className="font-semibold">R$ {(product.preco_medio || 0).toFixed(2)}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Custo Unitário</div>
                                <div className="font-semibold">R$ {(product.custo_unitario || 0).toFixed(2)}</div>
                              </div>
                            </div>
                            {product.encalhado && (
                              <div className="mt-2 p-2 bg-red-50 dark:bg-red-950 rounded text-xs text-red-800 dark:text-red-200">
                                ⚠️ Produto encalhado: Sem vendas nos últimos 90 dias
                              </div>
                            )}
                          </div>
                        ))
                      )}
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card>
                <CardContent className="py-8 text-center">
                  <div className="text-muted-foreground">Clique em "Atualizar" para carregar a análise</div>
              </CardContent>
            </Card>
            )}
          </TabsContent>

          <TabsContent value="stock" className="space-y-4 pb-8">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold">Análise de Estoque</h2>
                <p className="text-sm text-muted-foreground">
                  Produtos que precisam ser repostos baseado em estoque atual vs mínimo e velocidade de venda
                </p>
              </div>
              <Button onClick={loadStockAnalysis} disabled={loadingStock}>
                <BarChart3 className="h-4 w-4 mr-2" />
                {loadingStock ? 'Carregando...' : 'Atualizar'}
              </Button>
            </div>

            {loadingStock ? (
              <Card>
                <CardContent className="py-8 text-center">
                  <div className="text-muted-foreground">Carregando análise de estoque...</div>
                </CardContent>
              </Card>
            ) : stockData ? (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Resumo</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <div className="text-sm text-muted-foreground">Total de Produtos</div>
                        <div className="text-2xl font-bold">{stockData.total_products}</div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Críticos</div>
                        <div className="text-2xl font-bold text-red-600">{stockData.critical_products || 0}</div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Alta Urgência</div>
                        <div className="text-2xl font-bold text-orange-600">{stockData.high_urgency_products || 0}</div>
                      </div>
                      <div>
                        <div className="text-sm text-muted-foreground">Média Urgência</div>
                        <div className="text-2xl font-bold text-yellow-600">{stockData.medium_urgency_products || 0}</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Package className="h-5 w-5" />
                      Produtos que Precisam Atenção
                    </CardTitle>
                    <CardDescription>
                      Mostrando produtos com urgência Crítica, Alta e Média. Ordenados por urgência.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="pb-8">
                    <div className="space-y-3">
                      {stockData.products.length === 0 ? (
                        <div className="text-center py-4 text-muted-foreground">
                          Nenhum produto encontrado
                        </div>
                      ) : (
                        stockData.products
                          .filter((p: any) => p.urgencia_reposicao !== 'Baixa') // Mostrar apenas Crítica, Alta e Média
                          .map((product: any, idx: number) => (
                          <div key={idx} className="p-4 border rounded-lg hover:bg-accent/50 transition-colors">
                            <div className="flex justify-between items-start mb-2">
                              <div className="flex-1">
                                <div className="font-semibold text-lg">{product.produto_nome}</div>
                                <div className="text-sm text-muted-foreground mt-1">
                                  ID: {product.produto_id}
                                </div>
                              </div>
                              <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                product.urgencia_reposicao === 'Crítica' ? 'bg-red-100 text-red-800' :
                                product.urgencia_reposicao === 'Alta' ? 'bg-orange-100 text-orange-800' :
                                product.urgencia_reposicao === 'Média' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {product.urgencia_reposicao}
                              </div>
                            </div>
                            {product.alerta_oportunidade && (
                              <div className="mb-3 p-3 bg-yellow-50 dark:bg-yellow-950 rounded-lg border border-yellow-200 dark:border-yellow-800">
                                <div className="font-semibold text-yellow-900 dark:text-yellow-100 mb-1">📢 Alerta de Oportunidade:</div>
                                <div className="text-sm text-yellow-800 dark:text-yellow-200">{product.alerta_oportunidade}</div>
                              </div>
                            )}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-3 text-sm">
                              <div>
                                <div className="text-muted-foreground">Estoque Atual</div>
                                <div className={`font-semibold ${
                                  product.quantidade_atual < product.quantidade_minima ? 'text-red-600' : ''
                                }`}>
                                  {product.quantidade_atual || 0}
                                </div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Estoque Mínimo</div>
                                <div className="font-semibold">{product.quantidade_minima || 0}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Vendas (7 dias)</div>
                                <div className="font-semibold text-primary">{product.vendas_7d || 0}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Qtd Vendida (7d)</div>
                                <div className="font-semibold">{product.vendas_7d_quantidade || 0}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Dias até Ruptura</div>
                                <div className="font-semibold">{(product.dias_ate_ruptura || 0).toFixed(1)}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Vendas Média Diária</div>
                                <div className="font-semibold">{(product.vendas_media_diaria || 0).toFixed(1)}</div>
                              </div>
                              {product.quantidade_sugerida > 0 && (
                                <>
                                  <div>
                                    <div className="text-muted-foreground">Quantidade Sugerida</div>
                                    <div className="font-semibold text-primary">{Math.round(product.quantidade_sugerida || 0)}</div>
                                  </div>
                                  <div>
                                    <div className="text-muted-foreground">Custo de Reposição</div>
                                    <div className="font-semibold">
                                      R$ {(product.custo_reposicao || 0).toFixed(2)}
                                    </div>
                                  </div>
                                </>
                              )}
                              <div>
                                <div className="text-muted-foreground">Custo Unitário</div>
                                <div className="font-semibold">R$ {(product.custo_unitario || 0).toFixed(2)}</div>
                              </div>
                              <div>
                                <div className="text-muted-foreground">Score de Reposição</div>
                                <div className="font-semibold">{(product.score_reposicao || 0).toFixed(2)}</div>
                              </div>
                            </div>
                          </div>
                        ))
                      )}
                    </div>
                  </CardContent>
                </Card>
                <div className="h-12"></div> {/* Espaço extra no final para evitar corte */}
              </>
            ) : (
              <Card>
                <CardContent className="py-8 text-center">
                  <div className="text-muted-foreground">Clique em "Atualizar" para carregar a análise</div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="powerbi">
            <PowerBiDashboard />
          </TabsContent>
        </Tabs>
      </main>

      <BottomNavigation />
    </div>
  );
};

export default Reports;

