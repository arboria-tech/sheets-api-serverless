import json
import logging
import gspread
from google.oauth2.service_account import Credentials
from typing import Any, Dict, List, Optional

# Configura o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Função para obter as credenciais do Google Sheets
def get_google_sheets_credentials() -> Credentials:
    # Carregando as credenciais do arquivo credentials.json
    try:
        creds = Credentials.from_service_account_file(
            'client_secret.json',
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        return creds
    except Exception as e:
        logger.error(f"Error loading credentials: {str(e)}")
        raise

# Função para obter todos os registros de uma planilha
def get_all_records(spreadsheet_id: str, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        # Cria um cliente gspread usando as credenciais
        credentials = get_google_sheets_credentials()
        client = gspread.authorize(credentials)

        # Abre a planilha pelo ID
        logger.info(f"Opening spreadsheet with ID: {spreadsheet_id}")
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Seleciona a aba apropriada
        sheet = spreadsheet.worksheet(sheet_name) if sheet_name else spreadsheet.sheet1
        
        # Obtém todos os dados da aba
        data = sheet.get_all_records()
        
        logger.info(f"Retrieved {len(data)} records from spreadsheet.")
        return data

    except gspread.SpreadsheetNotFound:
        logger.error(f"Spreadsheet with ID {spreadsheet_id} not found.")
        raise Exception(f"Spreadsheet not found with ID {spreadsheet_id}.")
    except gspread.WorksheetNotFound:
        logger.error(f"Worksheet with name {sheet_name} not found.")
        raise Exception(f"Worksheet not found with name {sheet_name}.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

# Função principal da Lambda
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Extrai o corpo da requisição POST
        body = json.loads(event.get('body', '{}'))

        # Valida os parâmetros esperados
        if 'spreadsheet_id' not in body:
            raise ValueError("Missing required field: spreadsheet_id")

        # Pega os parâmetros do corpo da requisição
        spreadsheet_id = body['spreadsheet_id']
        sheet_name = body.get('sheet_name')  # Opcional

        logger.info(f"Request received to fetch records for spreadsheet_id={spreadsheet_id}, sheet_name={sheet_name}")

        # Busca todos os registros da planilha
        records = get_all_records(spreadsheet_id, sheet_name)

        # Retorna os registros em formato JSON
        return {
            'statusCode': 200,
            'body': json.dumps(records),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(ve)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
