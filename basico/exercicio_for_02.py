###
# Exercícios
#
# 1. Calculando % de uma lista
# Faremos algo parecido com "filtrar" uma lista.
# Mais pra frente no curso aprenderemos outras formas de fazer isso, mas
# com o nosso conhecimentoa atual já conseguimos resolver o desafio.

# Digamos que a gente tenha uma lista de vendedores e ao invés de saber todos os vendedores que bateram a meta,
# eu quero conseguir calcular o % de vendedores que bateram a meta.
# Ou seja, se temos 10 vendedores e 3 bateram a meta, temos 30% dos vendedores que bateram a meta.

meta = 10000
vendas = [
    ['João', 15000],
    ['Julia', 27000],
    ['Marcus', 9900],
    ['Maria', 3750],
    ['Ana', 10300],
    ['Alon', 7870],
]

# Vamos resolver de 2 formas:
# Criando uma lista auxiliar apenas com os vendedores que bateram a meta
# Fazendo o cálculo diretamente na lista que já temos
# Para treinar uma estrutura parecida, crie um código para responder: quem foi o vendedor que mais vendeu?

bateu_meta = []
valores = []

# 1
for indice, item in enumerate(vendas):
    if item[1] >= meta:
        bateu_meta.append(item[0])
print(bateu_meta)
print("{:.2%} dos vendedores bateram a meta".format(len(bateu_meta) / len(vendas)))

# 2
acima_meta = 0
for i in range(len(vendas)):
    if vendas[i][1] >= meta:
        acima_meta += 1
    else:
        pass
print("{:.2%} dos vendedores bateram a meta".format(acima_meta / len(vendas)))

# 3
for item in vendas:
    if item[1] >= meta:
        bateu_meta.append(item[0])
        valores.append(item[1])
print("Quem vendeu mais foi: {}, com {} vendas".format(bateu_meta[valores.index(max(valores))], max(valores)))
