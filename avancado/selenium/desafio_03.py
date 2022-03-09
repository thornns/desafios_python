from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import zipfile
import pandas as pd
import yagmail

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

chrome_options.add_experimental_option("prefs", {
  "download.default_directory": "C:\\Users\\daniel.malizia\\Downloads",
  "download.prompt_for_download": False,
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.kaggle.com/sakshigoyal7/credit-card-customers")

# Botão de Download
driver.find_element(By.CLASS_NAME, 'sc-gXfVKN').click()
time.sleep(2)

# Login via e-mail
driver.find_elements(By.CLASS_NAME, 'sc-laZMeE')[1].click()
time.sleep(2)

# Preencher as credenciais
driver.find_elements(By.CLASS_NAME, 'mdc-ripple-upgraded')[0].send_keys('danielsantarita@gmail.com')
driver.find_elements(By.CLASS_NAME, 'mdc-ripple-upgraded')[1].send_keys('')
driver.find_elements(By.CLASS_NAME, 'mdc-ripple-upgraded')[1].send_keys(Keys.RETURN)
time.sleep(2)

# Download
driver.find_element(By.CLASS_NAME, 'sc-gXfVKN').click()
time.sleep(1)

for file in os.listdir("C:\\Users\\daniel.malizia\\Downloads\\"):
    if file.endswith(".crdownload"):
        time.sleep(1)
        print("Aguardando fim do download...")
print("Download OK...")

with zipfile.ZipFile(r'C:\Users\daniel.malizia\Downloads\archive.zip', 'r') as zip_ref:
    zip_ref.extractall('C:\\Users\\daniel.malizia\\Downloads\\')

print('Criando dataframe...')
pd.set_option('display.width', None)
dataframe = pd.read_csv('C:\\Users\\daniel.malizia\\Downloads\\BankChurners.csv')

"""
Clientes Ativos e Clientes em Disputa
"""

resumo_clientes = dataframe.groupby('Attrition_Flag')['Attrition_Flag'].count()
resumo_clientes.index.names = ['Categoria dos Clientes - Existing ou Attrited']

"""
Dos Ativos, qual a distribuição por tipo de cartão
"""

ativos = dataframe.loc[dataframe['Attrition_Flag'] == 'Existing Customer', ['Attrition_Flag', 'Card_Category']]
resumo_cartoes = dataframe.groupby('Card_Category')['Card_Category'].count()
resumo_cartoes.index.names = ['Categoria dos Cartões - Clientes Ativos']

"""
Tempo médio de permanencia e Limite médio dos clientes (ativos e ex-clientes)
"""

resumo_permanencia = dataframe['Months_on_book'].mean()
resumo_limite = dataframe['Credit_Limit'].mean()
print('Análise: Tempo médio de permanencia e Limite médio dos clientes')

"""
Enviar E-mail com as informações
"""

usuario = yagmail.SMTP(user='danielsantarita@gmail.com',
                       password='')

conteudo = f"""
{resumo_clientes.to_string()}

{resumo_cartoes.to_string()}

Tempo Médio de Permanência: {resumo_permanencia:.2f} meses

Limite de crédito médio: ${resumo_limite:.2f}
"""

usuario.send(to='danielsantarita@gmail.com',
             subject='Relatório - Desafio de Selenium com Pandas',
             contents=conteudo,
             attachments=r'C:\Users\daniel.malizia\Downloads\BankChurners.csv')
