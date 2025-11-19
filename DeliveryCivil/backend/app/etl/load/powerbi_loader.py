"""
Loader para Power BI
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import logging
import json

from app.config import settings

logger = logging.getLogger(__name__)

class PowerBILoader:
    """Loader para salvar dados processados para Power BI"""
    
    def save_for_powerbi(self, df: pd.DataFrame, table_name: str) -> dict:
        """
        Salva DataFrame em formatos compatíveis com Power BI
        
        Args:
            df: DataFrame para salvar
            table_name: Nome da tabela
            
        Returns:
            Dict com caminhos dos arquivos salvos
        """
        try:
            output_dir = Path(settings.DATA_OUTPUT_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            saved_files = {}
            
            # Salvar como CSV (compatível com Power BI)
            csv_path = output_dir / f"{table_name}_{timestamp}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            saved_files['csv'] = str(csv_path)
            
            # Salvar como JSON (alternativa)
            json_path = output_dir / f"{table_name}_{timestamp}.json"
            df.to_json(json_path, orient='records', date_format='iso', indent=2)
            saved_files['json'] = str(json_path)
            
            # Salvar metadados
            metadata = {
                'table_name': table_name,
                'timestamp': timestamp,
                'rows': len(df),
                'columns': list(df.columns),
                'file_paths': saved_files
            }
            
            metadata_path = output_dir / f"{table_name}_{timestamp}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Dados salvos para Power BI: {table_name} ({len(df)} registros)")
            
            return saved_files
            
        except Exception as e:
            logger.error(f"Erro ao salvar dados para Power BI: {str(e)}")
            raise

