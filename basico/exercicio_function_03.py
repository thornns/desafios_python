"""
1. Cálculo do Percentual e da Lista de Vendedores

Queremos criar uma function que consiga identificar os vendedores que bateram uma meta, mas além disso,
consigo já me dar como resposta o cálculo do % da lista de vendedores que bateu a meta
(para eu não precisar calcular manualmente depois)

Essa function deve receber 2 informações como parâmetro: a meta e um dicionário com os vendedores e suas vendas.
E me dar 2 respostas: uma lista com o nome dos vendedores que bateram a meta e o % de vendedores que bateu a meta.
"""

meta = 10000
vendas = {
    'João': 15000,
    'Julia': 27000,
    'Marcus': 9900,
    'Maria': 3750,
    'Ana': 10300,
    'Alon': 7870,
}


def perc_meta(metas, venda):
    bate_meta = []
    for i in venda:
        if venda[i] >= metas:
            bate_meta.append(i)

    percentual = len(bate_meta) / len(venda)
    return bate_meta, percentual


resultado = perc_meta(meta, vendas)
print("{} e {} bateram a meta. Desta forma, {:.2%} bateram a meta."
      .format(', '.join(resultado[0][:-1]),
              resultado[0][-1],
              resultado[1]))
