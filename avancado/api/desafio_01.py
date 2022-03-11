"""
API Google Sheets
https://developers.google.com/sheets/api/quickstart/python
"""

from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Se modificar esta linha, delete o token.json
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# O ID e o Range da planilha, ambos são obrigatórios
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = 'Sheet1!A1:G1'

creds = None

# O arquivo token.json guarda as tokens de acesso do usuário
# É criado automaticamente quando o fluxo de autorização é completado pela primeira vez.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Se não houverem credenciais (válidas) disponíveis, fará o usuário logar
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('gsheet.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Salva as credenciais para a próxima execução
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('sheets', 'v4', credentials=creds)

    # Chama a Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('Nenhum Dado Encontrado.')
    else:
        print('Conexão Bem Sucedida')

except HttpError as err:
    print(err)

# A partir daqui você pode editar a planilha
planilha_id = ''
planilha_range = 'Sheet1!A:F'

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=planilha_id, range=planilha_range).execute()

# 1 lista com 1 lista por linha. [[linha 1], [linha 2], ..., [linha n]]
values = result.get('values', [])
print(values)

# Escrever valores
# valueInputOption: RAW (equivale a r'') ou USER_ENTERED (usar quando inserir fórmulas)
values = [["Atualizado via API"]]
body = {'values': values}

result = service.spreadsheets().values().update(spreadsheetId=planilha_id,
                                                range="Sheet1!A1",
                                                valueInputOption="RAW",
                                                body=body).execute()
print('{0} células atualizadas'.format(result.get('updatedCells')))

# Escrever no FINAL da planilha
values = [["Daniel", "danielsantarita@gmail.com", "Append via API"]]
body = {'values': values}

result = service.spreadsheets().values().append(spreadsheetId=planilha_id,
                                                range="Sheet1!A1:G2",
                                                valueInputOption="RAW",
                                                body=body).execute()
print('{0} células atualizadas'.format(result.get('updates').get('updatedCells')))

# Desafio planilha ComprasProblema

planilha_id = ''
planilha_range = 'Sheet1!A1:D9'

sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=planilha_id, range=planilha_range).execute()

# 1 - Ler o intervalo:
values = result.get('values', [])

# 2 - Verificar se Status está preenchido:
# 3 - Se o Status estiver vazio, verificar o problema:
# 4 - Enviar mensagem e registrar novo status:


def atualizar_status(status: str, indice: int) -> None:
    indice += 1
    servico = build('sheets', 'v4', credentials=creds)
    valores = [[f"{status}"]]
    corpo = {'values': valores}

    servico.spreadsheets().values().update(
        spreadsheetId='',
        range=f"Sheet1!D{indice}",
        valueInputOption="RAW",
        body=corpo)\
        .execute()
    return


for i, lista in enumerate(values):
    if len(lista) < 4:
        if lista[2] == 'Comprou':
            atualizar_status("Compra Finalizada", i)
        if lista[2] == 'Boleto Gerado':
            atualizar_status("Mensagem Boleto Enviada", i)
        elif lista[2] == 'Sem Saldo':
            atualizar_status("Mensagem Sem Saldo Enviada", i)
print('Status atualizados.')
