from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Esse site não existe mais!!!!
driver.get("https://pbdatareader.com.br/jogosdodia")

while len(driver.find_elements(By.TAG_NAME, 'iframe')) == 0:
    time.sleep(1)

iframe = driver.find_element(By.TAG_NAME, 'iframe')
driver.switch_to.frame(iframe)

iframe = driver.find_element(By.TAG_NAME, 'iframe')
driver.switch_to.frame(iframe)

# Criar a tabela inicial
tabela = driver.find_element(By.CLASS_NAME, 'innerContainer')

texto = tabela.text  # retornou 20 valores
lista_texto = texto.split('\n')
colunas = lista_texto[:11]
valores = lista_texto[11:]

dic = {}
for coluna in colunas:
    dic[coluna] = []
    for i in range(20):
        dic[coluna].append(valores[i])
    valores = valores[20:]

tabela_df = pd.Dataframe.from_dict(dic)

# Criar as próximas tabelas
for i in range(200):
    y = 250 * i
    driver.execute_script(f'document.getElementsByClassName("bodyCells")[0].scroll(0, {y})')

    tabela = driver.find_element(By.CLASS_NAME, 'innerContainer')

    texto = tabela.text
    lista_texto = texto.split('\n')
    colunas = lista_texto[:11]
    valores = lista_texto[11:]

    dic = {}
    for coluna in colunas:
        dic[coluna] = []
        for i in range(20):
            dic[coluna].append(valores[i])
        valores = valores[20:]

    tabela_temp = pd.Dataframe.from_dict(dic)
    tabela_df = tabela_df.append(tabela_temp, ignore_index=True)

# Remover duplicatas
tabela_df = tabela_df.drop_duplicates()

# Salvar em Excel
tabela_df.to_excel("Tabela de Jogos.xlsx", index=False)
