###
# Exercícios
# 1. Input até o usuário parar
# Vamos criar um sistema de vendas.
# Nosso programa deve registrar os produtos e as quantidades (2 inputs) e adicionar em uma lista.
#
# O programa deve continuar rodando até o input ser vazio, ou seja,
# o usuário apertar enter sem digitar nenhum produto ou quantidade.
#
# Ao final do programa, ele deve printar todos os produtos e quantidades vendidas.
#
# Obs: Caso queira, para o print ficar mais visual, pode usar o join para cada item ser printado em uma linha.
# Sugestão para sua lista de produtos vendidos:
###

vendas = [
    ['maçã', 5],
    ['banana', 15],
    ['azeite', 1],
    ['vinho', 3],
]

while True:
    cadastro = input("Registre um produto. Deixe em branco e pressione ENTER para cancelar ")
    if cadastro:
        quantidade = input("Registre a quantidade do produto: ")
        vendas.append([cadastro, quantidade])
    else:
        break
print(vendas)

# Obs: Podemos fazer o While de 2 maneiras:
# While com a condição que finalize o programa
# While rodando para sempre, mas com uma condição dentro do while que dê um break no código.
# Vamos mostrar as 2 opções
