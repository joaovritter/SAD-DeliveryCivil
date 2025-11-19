"""
Serviço de integração com Power BI
"""
import os
import logging
from typing import Dict, Optional
from msal import ConfidentialClientApplication
import requests

from app.config import settings

logger = logging.getLogger(__name__)

class PowerBIService:
    """Serviço para autenticação e geração de embed tokens do Power BI"""
    
    def __init__(self):
        self.tenant_id = settings.AZURE_TENANT_ID or ""
        self.client_id = settings.AZURE_CLIENT_ID or ""
        self.client_secret = settings.AZURE_CLIENT_SECRET or ""
        self.workspace_id = settings.POWER_BI_WORKSPACE_ID or ""
        self.report_id = settings.POWER_BI_REPORT_ID or ""
        self.dataset_id = settings.POWER_BI_DATASET_ID or ""
        self.api_url = settings.POWER_BI_API_URL
        
        # Cache de access token
        self._access_token: Optional[str] = None
    
    def is_configured(self) -> bool:
        """
        Verifica se o Power BI está configurado
        
        Returns:
            True se todas as credenciais obrigatórias estão configuradas
        """
        return bool(
            self.tenant_id and 
            self.client_id and 
            self.client_secret and
            self.workspace_id and
            self.report_id
        )
    
    def get_missing_credentials(self) -> list:
        """
        Retorna lista de credenciais faltando
        
        Returns:
            Lista de nomes das credenciais que estão faltando
        """
        missing = []
        if not self.tenant_id:
            missing.append("AZURE_TENANT_ID")
        if not self.client_id:
            missing.append("AZURE_CLIENT_ID")
        if not self.client_secret:
            missing.append("AZURE_CLIENT_SECRET")
        if not self.workspace_id:
            missing.append("POWER_BI_WORKSPACE_ID")
        if not self.report_id:
            missing.append("POWER_BI_REPORT_ID")
        return missing
    
    def get_access_token(self) -> str:
        """
        Obtém access token do Azure AD usando Service Principal
        
        Returns:
            Access token para Power BI API
        """
        # Verificar se está configurado
        if not self.is_configured():
            missing = self.get_missing_credentials()
            raise ValueError(
                f"Power BI não configurado. Credenciais faltando: {', '.join(missing)}. "
                f"Configure no arquivo backend/.env"
            )
        
        try:
            # Se já temos token válido, retornar
            if self._access_token:
                return self._access_token
            
            # Criar aplicação MSAL
            app = ConfidentialClientApplication(
                client_id=self.client_id,
                client_credential=self.client_secret,
                authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )
            
            # Obter token
            result = app.acquire_token_for_client(
                scopes=["https://analysis.windows.net/powerbi/api/.default"]
            )
            
            if "access_token" in result:
                self._access_token = result["access_token"]
                logger.info("✅ Access token obtido com sucesso")
                return self._access_token
            else:
                error = result.get("error_description", result.get("error", "Erro desconhecido"))
                error_code = result.get("error_codes", [])
                logger.error(f"Erro ao obter access token: {error} (códigos: {error_code})")
                raise Exception(f"Falha na autenticação Azure AD: {error}")
                
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Erro ao obter access token: {str(e)}")
            raise
    
    def generate_embed_token(self, report_id: Optional[str] = None, dataset_id: Optional[str] = None) -> Dict:
        """
        Gera embed token para relatório Power BI
        
        Args:
            report_id: ID do relatório (opcional, usa padrão se não fornecido)
            dataset_id: ID do dataset (opcional, usa padrão se não fornecido)
            
        Returns:
            Dict com embedToken, embedUrl, reportId, etc.
        """
        try:
            access_token = self.get_access_token()
            
            # Usar IDs fornecidos ou padrão
            target_report_id = report_id or self.report_id
            target_dataset_id = dataset_id or self.dataset_id
            
            if not target_report_id:
                raise ValueError("report_id é obrigatório")
            
            # URL da API
            url = f"{self.api_url}/groups/{self.workspace_id}/reports/{target_report_id}/GenerateToken"
            
            # Payload para embed token
            payload = {
                "accessLevel": "View",
                "allowSaveAs": False
            }
            
            if target_dataset_id:
                payload["datasets"] = [{"id": target_dataset_id}]
            
            # Headers
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # Fazer requisição
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Obter embed URL
            embed_url = f"https://app.powerbi.com/reportEmbed?reportId={target_report_id}&groupId={self.workspace_id}"
            
            result = {
                "embedToken": token_data.get("token"),
                "embedUrl": embed_url,
                "reportId": target_report_id,
                "workspaceId": self.workspace_id,
                "tokenId": token_data.get("tokenId"),
                "expiration": token_data.get("expiration")
            }
            
            logger.info(f"✅ Embed token gerado para relatório {target_report_id}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao gerar embed token: {str(e)}")
            raise
    
    def get_report_info(self, report_id: Optional[str] = None) -> Dict:
        """
        Obtém informações de um relatório Power BI
        
        Args:
            report_id: ID do relatório (opcional, usa padrão se não fornecido)
            
        Returns:
            Dict com informações do relatório
        """
        try:
            access_token = self.get_access_token()
            target_report_id = report_id or self.report_id
            
            if not target_report_id:
                raise ValueError("report_id é obrigatório")
            
            url = f"{self.api_url}/groups/{self.workspace_id}/reports/{target_report_id}"
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            report_info = response.json()
            
            return {
                "id": report_info.get("id"),
                "name": report_info.get("name"),
                "webUrl": report_info.get("webUrl"),
                "embedUrl": report_info.get("embedUrl"),
                "description": report_info.get("description")
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter informações do relatório: {str(e)}")
            raise

