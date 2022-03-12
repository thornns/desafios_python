# replit.com para publicar

from flask import Flask
import pandas as pd
df = pd.read_excel('Vendas - Dez.xlsx')

app = Flask(__name__)  # Inicia o Site


@app.route('/')  # Diz em qual caminho do site a função vai ser executada
def faturamento():
    faturamento_total = float(df['Valor Final'].sum())
    return {'Faturamento': faturamento_total}


@app.route('/vendas/produtos')
def vendas_produtos():
    vendas_prod_df = df[['Produto', 'Quantidade', 'Valor Final']].groupby('Produto').sum()
    dic_vendas_produtos = vendas_prod_df.to_dict()
    return dic_vendas_produtos


@app.route('/vendas/produtos/<produto>')
def fat_produto(produto):
    produto = produto.title()
    fat_prod = df[['Produto', 'Quantidade', 'Valor Final']].groupby('Produto').sum()
    if produto in fat_prod.index:
        fat_prod = fat_prod.loc[produto].to_dict()
        return fat_prod
    else:
        return {produto: "Inexistente"}


app.run(host='0.0.0.0')  # Executa o site
