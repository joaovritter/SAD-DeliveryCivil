# DeliveryCivil - Sistema de Apoio à Decisão (SAD)

Sistema completo para análise de vendas, estoque e geração de recomendações de negócio com integração Power BI.

## 🚀 Funcionalidades

- ✅ Upload de datasets (vendas, estoque, compras)
- ✅ Análise de produtos para promoção
- ✅ Análise de estoque para reposição
- ✅ Análise de produtos para cashback
- ✅ Integração com Power BI Embedded
- ✅ Dashboard interativo com análises em tempo real

## 📋 Pré-requisitos

- Node.js 18+ e npm/yarn
- Python 3.11+
- Conta Azure com Power BI (opcional, para visualização)

## 🛠️ Instalação

### Backend (Python)

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp backend/.env.example backend/.env
# Editar backend/.env com suas credenciais

# Executar servidor
cd backend
python run.py
# Ou: uvicorn app.main:app --reload
```

### Frontend (React)

```bash
# Instalar dependências
npm install

# Configurar variável de ambiente (opcional)
# Criar .env.local com:
# VITE_API_BASE_URL=http://localhost:8000

# Executar servidor de desenvolvimento
npm run dev
```

## 📊 Formato dos Datasets

### Vendas (sales.csv)
```csv
data,produto_id,produto_nome,quantidade,valor_total,cliente_id
2024-01-15,1,Cimento CP-II 50kg,10,249.00,123
```

### Estoque (stock.csv)
```csv
produto_id,produto_nome,quantidade_atual,quantidade_minima,custo_unitario
1,Cimento CP-II 50kg,150,50,20.00
```

### Compras (purchases.csv)
```csv
data,produto_id,fornecedor,quantidade,custo_total
2024-01-10,1,Fornecedor A,200,4000.00
```

## 🔧 Estrutura do Projeto

```
DeliveryCivil/
├── backend/              # API FastAPI
│   ├── app/
│   │   ├── main.py      # Aplicação principal
│   │   ├── api/         # Endpoints
│   │   ├── etl/         # Pipeline ETL
│   │   ├── models/      # Modelos Pydantic
│   │   └── services/    # Serviços (Power BI)
│   └── data/            # Dados processados
├── src/                  # Frontend React
│   ├── pages/           # Páginas
│   ├── components/      # Componentes
│   └── services/        # Serviços API
└── requirements.txt     # Dependências Python
```

## 📡 Endpoints da API

### Upload
- `POST /api/datasets/upload/sales` - Upload vendas
- `POST /api/datasets/upload/stock` - Upload estoque
- `POST /api/datasets/upload/purchases` - Upload compras

### Análises
- `GET /api/analytics/promotion` - Análise de promoção
- `GET /api/analytics/stock` - Análise de estoque
- `GET /api/analytics/cashback` - Análise de cashback
- `GET /api/analytics/summary` - Resumo geral

### Power BI
- `GET /api/reports/embed-token` - Token para Power BI
- `GET /api/reports/info` - Info do relatório

## 🎯 Como Usar

1. **Upload de dados**: Acesse `/upload` e faça upload dos datasets
2. **Visualizar análises**: Acesse `/reports` para ver as análises
3. **Power BI**: Configure credenciais no `.env` e acesse a aba Power BI

## 📝 Licença

Este projeto é privado.
