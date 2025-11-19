import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 segundos
});

// Interceptor para tratamento de erros
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erro na API:', error);
    return Promise.reject(error);
  }
);

// Interfaces removidas - Power BI agora usa iframe público

export interface AnalyticsResponse {
  message: string;
  total_products: number;
  products: any[];
  critical_products?: number;
  high_urgency_products?: number;
  medium_urgency_products?: number;
}

export interface AnalyticsSummary {
  summary: {
    total_products: number;
    total_sales: number;
    total_revenue?: number;  // Receita total (opcional para compatibilidade)
    promotion_opportunities: number;
    stock_critical: number;
    cashback_high: number;
  };
  top_promotion: any[];
  top_stock: any[];
  top_cashback: any[];
}

// Power BI agora usa iframe público - não precisa de API
export const reportsApi = {
  // Endpoint mantido apenas para compatibilidade
  checkHealth: async () => {
    const response = await apiClient.get('/api/reports/health');
    return response.data;
  },
};

export const datasetsApi = {
  /**
   * Upload de dataset de vendas
   */
  uploadSales: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    
    // Não definir Content-Type manualmente - deixar o axios detectar automaticamente
    const response = await apiClient.post('/api/datasets/upload/sales', formData, {
      timeout: 60000, // 60 segundos para uploads grandes
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      },
    });
    return response.data;
  },

  /**
   * Upload de dataset de estoque
   */
  uploadStock: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/api/datasets/upload/stock', formData, {
      timeout: 60000,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      },
    });
    return response.data;
  },

  /**
   * Upload de dataset de compras
   */
  uploadPurchases: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/api/datasets/upload/purchases', formData, {
      timeout: 60000,
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      },
    });
    return response.data;
  },

  /**
   * Lista todos os datasets
   */
  listDatasets: async (): Promise<any> => {
    const response = await apiClient.get('/api/datasets/list');
    return response.data;
  },
};

export const analyticsApi = {
  /**
   * Análise de produtos para promoção
   */
  getPromotionAnalysis: async (saveToPowerBI: boolean = false): Promise<AnalyticsResponse> => {
    const response = await apiClient.get<AnalyticsResponse>(
      `/api/analytics/promotion?save_to_powerbi=${saveToPowerBI}`
    );
    return response.data;
  },

  /**
   * Análise de estoque para reposição
   */
  getStockAnalysis: async (saveToPowerBI: boolean = false): Promise<AnalyticsResponse> => {
    const response = await apiClient.get<AnalyticsResponse>(
      `/api/analytics/stock?save_to_powerbi=${saveToPowerBI}`
    );
    return response.data;
  },

  /**
   * Análise de produtos para cashback
   */
  getCashbackAnalysis: async (saveToPowerBI: boolean = false): Promise<AnalyticsResponse> => {
    const response = await apiClient.get<AnalyticsResponse>(
      `/api/analytics/cashback?save_to_powerbi=${saveToPowerBI}`
    );
    return response.data;
  },

  /**
   * Resumo de todas as análises
   */
  getSummary: async (): Promise<AnalyticsSummary> => {
    const response = await apiClient.get<AnalyticsSummary>('/api/analytics/summary');
    return response.data;
  },
};

