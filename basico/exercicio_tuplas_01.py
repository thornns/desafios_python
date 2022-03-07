vendeu = [
    ('20/08/2020', 'iphone x', 'azul', '128gb', 350, 4000),
    ('20/08/2020', 'iphone x', 'prata', '128gb', 1500, 4000),
    ('20/08/2020', 'ipad', 'prata', '256gb', 127, 6000),
    ('20/08/2020', 'ipad', 'prata', '128gb', 981, 5000),
    ('21/08/2020', 'iphone x', 'azul', '128gb', 397, 4000),
    ('21/08/2020', 'iphone x', 'prata', '128gb', 1017, 4000),
    ('21/08/2020', 'ipad', 'prata', '256gb', 50, 6000),
    ('21/08/2020', 'ipad', 'prata', '128gb', 4000, 5000),
]
faturamento = 0
# Qual o faturamento de iphone no dia 20/08/2020?

for data, produto, cor, capacidade, unidades, valor_unitario in vendeu:
    if ('iphone' in produto) and ('20/08/2020' in data):
        faturamento += unidades * valor_unitario
print(faturamento)

# Qual o item mais vendido (em unidades) no dia 21/08/2020?

produto_mais_vendido = ''
mais_vendido = 0
for data, produto, cor, capacidade, unidades, valor_unitario in vendeu:
    if '21/08/2020' in data:
        if mais_vendido < unidades:
            produto_mais_vendido = produto + ' ' + cor + ' ' + capacidade
            mais_vendido = unidades

print("O produto mais vendido foi {}, com {} unidades vendidas.".format(produto_mais_vendido, mais_vendido))
