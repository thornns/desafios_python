###
# 1. Exercício "menos prático" para treinar manipulação de dicionário
# Dessa vez, vamos apenas treinar a manipulação de dicionário.
# Transforme as listas abaixo em 1 único dicionário no formato:

# dicionario = {
#     produto: [vendas2019, vendas2020],
#     produto2: [vendas2019, vendas2020],
#     produto3: [vendas2019, vendas2020],
#     ...
# }

# Apesar de parecer "menos prático" esse é um procedimento que precisamos nos acostumar a fazer,
# visto que algumas funções (tema dos próximos módulos) precisam de dicionários para funcionar e
# saber transformar listas em dicionários (e vice-versa) é uma habilidade muito útil

# Obs: Lembre do zip para juntar listas.
# Obs2: Repare que cada item das vendas é na verdade uma lista.
# Então é provável que você precise fazer esse código em 2 etapas

produtos = ['iphone', 'galaxy', 'ipad', 'tv', 'máquina de café', 'kindle', 'geladeira', 'adega', 'notebook dell',
            'notebook hp', 'notebook asus', 'microsoft surface', 'webcam', 'caixa de som', 'microfone', 'câmera canon']
vendas2019 = [558147, 712350, 573823, 405252, 718654, 531580, 973139, 892292, 422760, 154753, 887061, 438508, 237467,
              489705, 328311, 591120]
vendas2020 = [951642, 244295, 26964, 787604, 867660, 78830, 710331, 646016, 694913, 539704, 324831, 667179, 295633,
              725316, 644622, 994303]

tupla_vendas = list(zip(vendas2019, vendas2020))
dic_produtos = dict(zip(produtos, tupla_vendas))
print(dic_produtos)
