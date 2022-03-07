"""
1. Tirando informações de listas e dicionários
Digamos que você está analisando as vendas de produtos de uma empresa de varejo.

Essa lista tem: (produto, vendas de 2019, vendas de 2020) para cada produto.

Crie uma lista com as vendas de 2019.
"""
vendas_produtos = [('iphone', 558147, 951642), ('galaxy', 712350, 244295), ('ipad', 573823, 26964),
                   ('tv', 405252, 787604), ('máquina de café', 718654, 867660), ('kindle', 531580, 78830),
                   ('geladeira', 973139, 710331), ('adega', 892292, 646016), ('notebook dell', 422760, 694913),
                   ('notebook hp', 154753, 539704), ('notebook asus', 887061, 324831),
                   ('microsoft surface', 438508, 667179), ('webcam', 237467, 295633),
                   ('caixa de som', 489705, 725316), ('microfone', 328311, 644622), ('câmera canon', 591120, 994303)]

"""
Agora, qual o maior valor de vendas de 2019?
E se eu quisesse descobrir o produto que mais vendeu em 2019? Temos 2 formas de fazer, refazendo o list comprehension ou
consultando a lista original
"""

vendas_ano_2019 = [vendas_2019 for produto, vendas_2019, vendas_2020 in vendas_produtos]
vendas_ano_2019.sort(reverse=True)
print(vendas_ano_2019)

vendas_ano_2019.clear()

vendas_ano_2019 = [(vendas_2019, produto) for produto, vendas_2019, vendas2020 in vendas_produtos]
vendas_ano_2019.sort(reverse=True)
print(vendas_ano_2019[0][1])
