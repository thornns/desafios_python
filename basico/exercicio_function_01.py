"""
1. Function para Cálculo de Carga Tributária
(Lembrando, não se atente ao funcionamento real da carga tributária,
é apenas um exemplo imaginário para treinarmos as functions com algo mais prático)

Imagine que você trabalha no setor contábil de uma grande empresa de Varejo.

Crie uma function que calcule qual o % de carga tributária que está sendo aplicado sobre um determinado produto,
dado o preço de venda, o "lucro" e os custos (com exceção do imposto) dele.

"""

preco = 1500
custo = 400
lucro = 800

"""
Repare que preço - custo não é igual ao lucro, porque ainda foi descontado o imposto.
Sua function deve calcular qual foi o % de imposto aplicado sobre o preço total.
"""


def advinhar_tributos(preco_, custo_, lucro_):
    percent_lucro = (lucro_ / preco_)
    percent_custo = (custo_ / preco_)
    return 1 - (percent_lucro + percent_custo)


print("Total de {:.2%} imposto sobre o preço final".format(advinhar_tributos(preco, custo, lucro)))
