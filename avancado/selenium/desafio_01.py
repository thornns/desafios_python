"""
Desafio - Rotina de Baixar uma Planilha da Web
Imagine que você trabalhe no Mercado Financeiro e tem que rtodo dia/semana baixar uma planilha com as cotações do dólar
Usaremos o site investing.com para baixar esses dados
O link onde ficam esses dados é: https://br.investing.com/currencies/usd-brl-historical-data
Escolhemos o site investing.com porque ele é cheio de coisinha chata que vai obrigar a gente a fazer um código completo
Crie uma conta no site antes de começar, é gratuito
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import os

# Executar o chrome em modo headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')

# Permitir Downloads no modo headless
chrome_options.add_experimental_option("prefs", {
  "download.default_directory": "C:\\Users\\daniel.malizia\\Downloads",
  "download.prompt_for_download": False,
})

# Configurar a variável driver e abrir o site
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://br.investing.com/currencies/usd-brl-historical-data")
print("Carregou o Site")

# Aceitar Cookies
cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
cookies.click()
print("Cookies OK")

# Botão de Login
login_btn = driver.find_element(By.XPATH, '//*[@id="userAccount"]/div/a[1]')
login_btn.click()
print("Clicar em Login OK")

# Campo de Usuário
login_user = driver.find_element(By.ID, 'loginFormUser_email')
login_user.click()
login_user.send_keys('danielsantarita_955@hotmail.com')
print("Usuário OK")

# Campo de Senha
login_pwd = driver.find_element(By.ID, 'loginForm_password')
login_pwd.click()
login_pwd.send_keys('@Rbn876rx')
login_pwd.send_keys(Keys.RETURN)
print("Senha OK")

# Fechar Pop-up de investimentos (se ela aparecer)
x = 0
while len(driver.find_elements(By.ID, 'dealCloseButton')) == 0:
    time.sleep(1)
    x += 1
    if x < 5:
        pass
    else:
        break

if x < 5:
    # Fechar a Pop-up
    popup_investimentos = driver.find_element(By.ID, 'dealCloseButton')
    time.sleep(1)
    popup_investimentos.click()
    print("Popup de Investimentos OK")

    # Baixar o documento
    download_excel = driver.find_element(By.XPATH, '//*[@id="column-content"]/div[4]/div/a')
    download_excel.click()

    # Aguardar o download
    for file in os.listdir("C:\\Users\\daniel.malizia\\Downloads\\"):
        if file.endswith(".crdownload"):
            time.sleep(1)
            print("Aguardando fim do download")
    print("Download OK")

else:
    # Baixar o documento
    download_excel = driver.find_element(By.XPATH, '//*[@id="column-content"]/div[4]/div/a')
    download_excel.click()

    # Aguardar o download
    for file in os.listdir("C:\\Users\\daniel.malizia\\Downloads\\"):
        if file.endswith(".crdownload"):
            time.sleep(1)
            print("Aguardando fim do download")
    print("Download OK")
