import React, { useState } from 'react';
import { ArrowLeft, ExternalLink, Maximize2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';

// ============================================
// CONFIGURE O LINK DO SEU RELATÓRIO POWER BI
// ============================================
const POWER_BI_URL = "https://app.powerbi.com/view?r=eyJrIjoiMWYzNjU5MjUtNWJkYy00M2FlLWJkNDAtZWZiNzk0ZmM5ODhjIiwidCI6ImU1YTJkNTdmLTgyZTMtNDNkYS1hZjFjLTFhMmNjMWI0MjMzMCJ9";

interface PowerBiDashboardProps {
  reportId?: string;
  datasetId?: string;
  onFilterChange?: (filters: any[]) => void;
}

const PowerBiDashboard: React.FC<PowerBiDashboardProps> = () => {
  const navigate = useNavigate();
  const [showExternal, setShowExternal] = useState(false);
  const [iframeError, setIframeError] = useState(false);

  // Abrir Power BI em nova aba
  const handleOpenPowerBI = () => {
    if (POWER_BI_URL && POWER_BI_URL.trim() !== "") {
      window.open(POWER_BI_URL, '_blank', 'noopener,noreferrer');
    }
  };

  // Detectar erro no iframe
  const handleIframeError = () => {
    setIframeError(true);
  };

  // Se houver erro ou preferir modo externo, mostrar botão
  if (showExternal || iframeError) {
    return (
      <div className="p-4 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold">Relatório Power BI</h2>
            <p className="text-sm text-muted-foreground">
              Clique no botão abaixo para acessar o relatório
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => setShowExternal(false)}>
              Tentar Incorporar
            </Button>
            <Button variant="outline" onClick={() => navigate('/reports')}>
              <ArrowLeft size={16} className="mr-2" />
              Voltar
            </Button>
          </div>
        </div>

        <div className="flex justify-center items-center min-h-[400px]">
          <Button 
            onClick={handleOpenPowerBI}
            size="lg"
            className="text-lg px-8 py-6"
          >
            <ExternalLink size={24} className="mr-3" />
            Abrir Relatório Power BI
          </Button>
        </div>
      </div>
    );
  }

  // Tentar mostrar em iframe
  return (
    <div className="flex flex-col h-[calc(100vh-120px)]">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-background">
        <div>
          <h2 className="text-xl font-bold">Relatório Power BI</h2>
          <p className="text-sm text-muted-foreground">
            Visualização incorporada
          </p>
        </div>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            size="sm"
            onClick={handleOpenPowerBI}
            title="Abrir em nova aba"
          >
            <Maximize2 size={16} className="mr-2" />
            Abrir Externo
          </Button>
          <Button variant="outline" size="sm" onClick={() => navigate('/reports')}>
            <ArrowLeft size={16} className="mr-2" />
            Voltar
          </Button>
        </div>
      </div>

      {/* Iframe do Power BI */}
      <div className="flex-1 relative">
        <iframe
          src={POWER_BI_URL}
          title="Power BI Dashboard"
          className="w-full h-full border-0"
          allowFullScreen
          onError={handleIframeError}
          sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
        />
      </div>
    </div>
  );
};

export default PowerBiDashboard;
