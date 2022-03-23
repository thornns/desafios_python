import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yagmail
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
"""
Para cada produto:
1 - Procurar no Google Shopping
    acessar o google
    pesquisar pelo df[Nome]
    clicar na aba Shopping
    pegar o preço do produto
2 - Procurar no Buscapé
3 - Verificar se os produtos de (1) estão na faixa de preços
4 - Verificar se os produtos de (2) estão na faixa de preços
"""

"""
Pesquisa Google:
"""
def buscar_google(navegador, produto: str, banido: str, preco_min: float, preco_max: float) -> list:
    """
    Realiza uma busca no Google Shopping por um produto e retorna uma lista de resultados.

    :param navegador: Navegador criado através do webdriver
    :param produto: Produto a ser pesquisado. Exemplo: Iphone 12 Max 64 GB
    :param banido: Termos que não devem aparecer nos resultados. Exemplo: Watch
    :param preco_min: Float com o valor mínimo a ser capturado. Exemplo: 3200.00
    :param preco_max: Float com o valor máximo a ser capturado. Exemplo: 3800.00
    :return: Retorna uma lista de tuplas no formato (nome do produto, preço do produto, link para a loja)
    """

    produto_termos = produto.split(" ")
    banido_termos = banido.split(" ")

    navegador.get("https://google.com.br")
    navegador.find_element(By.CLASS_NAME, 'gLFyf').send_keys(produto, Keys.RETURN)
    time.sleep(1)

    shopping = navegador.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for item in shopping:
        if 'Shopping' in item.text:
            item.click()
            break
        else:
            pass

    resultados = navegador.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')
    time.sleep(1)

    lista_ofertas = list()
    for resultado in resultados:
        nomes = resultado.find_element(By.CLASS_NAME, 'Xjkr3b').text.lower()

    # Verificando existência de termos banidos
        tem_banidos = False
        for termo in banido_termos:
            if termo in nomes:
                tem_banidos = True

    # Verificando se o item encontrado possui todos os itens de pesquisa
        tem_produtos = True
        for termo in produto_termos:
            if termo not in nomes:
                tem_produtos = False

        if not tem_banidos and tem_produtos:
            precos = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
            precos = precos.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            precos = float(precos)

            # Verificando os preços
            tem_preco = False
            if (precos >= float(preco_min)) and (precos <= float(preco_max)):
                tem_preco = True

            if tem_preco:
                # Pegando o link pelo CSS Selector:
                links = resultado.find_element(By.CSS_SELECTOR, 'a.shntl').get_attribute('href')
                lista_ofertas.append((nomes, precos, links))

    return lista_ofertas

"""
Pesquisa Buscapé
"""
def buscarpe(navegador, produto: str, banido: str, preco_min: float, preco_max: float) -> list:
    """
    Realiza uma busca no Buscapé por um produto e retorna uma lista de resultados.

    :param navegador: Navegador criado através do webdriver
    :param produto: Produto a ser pesquisado. Exemplo: Iphone 12 Max 64 GB
    :param banido: Termos que não devem aparecer nos resultados. Exemplo: Watch
    :param preco_min: Float com o valor mínimo a ser capturado. Exemplo: 3200.00
    :param preco_max: Float com o valor máximo a ser capturado. Exemplo: 3800.00
    :return: Retorna uma lista de tuplas no formato (nome do produto, preço do produto, link para a loja)
    """

    produto_termos = produto.split(" ")
    banido_termos = banido.split(" ")

    preco_min = float(preco_min)
    preco_max = float(preco_max)
    navegador.get("https://www.buscape.com.br")

    navegador.find_element(By.CLASS_NAME, 'search-bar__text-box').send_keys(produto, Keys.RETURN)
    time.sleep(5)

    lista_ofertas = list()
    resultados = navegador.find_elements(By.CLASS_NAME, 'Cell_Cell__1YAxR')
    for resultado in resultados:
        nomes = resultado.find_element(By.CLASS_NAME, 'Text_LabelSmRegular__2Lr6I').text.lower()

        # Verificando existência de termos banidos
        tem_banidos = False
        for termo in banido_termos:
            if termo in nomes:
                tem_banidos = True

        # Verificando se o item encontrado possui todos os itens de pesquisa
        tem_produtos = True
        for termo in produto_termos:
            if termo not in nomes:
                tem_produtos = False

        if not tem_banidos and tem_produtos:
            precos = resultado.find_element(By.CLASS_NAME, 'CellPrice_MainValue__3s0iP').text
            precos = precos.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            precos = float(precos)

            # Verificando os preços
            tem_preco = False
            if (precos >= float(preco_min)) and (precos <= float(preco_max)):
                tem_preco = True

            if tem_preco:
                # Pegando o link pelo CSS Selector:
                links = resultado.find_element(By.CSS_SELECTOR, 'a.Cell_Content__1630r').get_attribute('href')
                lista_ofertas.append((nomes, precos, links))

    return lista_ofertas

"""
Importar e visualizar os itens da base de dados
"""
df = pd.read_excel('buscas.xlsx')

tabela = pd.DataFrame()
for produtos in df['Nome']:
    banidos = df.loc[df['Nome'] == produtos, 'Termos banidos'].values[0]
    precos_min = df.loc[df['Nome'] == produtos, 'Preço mínimo'].values[0]
    precos_max = df.loc[df['Nome'] == produtos, 'Preço máximo'].values[0]
    busca_pe = buscarpe(driver, produtos, banidos, precos_min, precos_max)
    if busca_pe:
        busca_pe_df = pd.DataFrame(busca_pe, columns=['Produto', 'Preço', 'Link'])
        tabela = tabela.append(busca_pe_df)
    else:
        busca_pe_df = None
        print(f'Buscapé {produtos} Vazio')

    busca_google = buscar_google(driver, produtos, banidos, precos_min, precos_max)
    if busca_google:
        busca_google_df = pd.DataFrame(busca_google, columns=['Produto', 'Preço', 'Link'])
        tabela = tabela.append(busca_google_df)
    else:
        busca_google_df = None
        print(f'Google {produtos} Vazio')
driver.close()

"""
Salvar as ofertas em um Dataframe
Exportar para excel
"""
tabela.to_excel('ofertas.xlsx', index=False)

"""
Enviar por e-mail
"""
usuario = yagmail.SMTP(user='danielsantarita@gmail.com',
                       password='')

usuario.send(to='danielsantarita@gmail.com',
             subject='Webscrapping Selenium - Google Shopping e Buscapé',
             contents='Em Anexo.',
             attachments='ofertas.xlsx')
