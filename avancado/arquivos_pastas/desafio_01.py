"""
Você trabalha em uma empresa que tem 18 lojas espalhadas por rtodo o Brasil e divididas em 5 estados diferentes:

RJ
SP
MG
GO
AM

rTodo trimestre, são calculados os indicadores de cada funcionário de cada loja e
esses indicadores são armazenados em um arquivo em Excel.

Cada estado tem 1 Gerente Geral responsável por todas as lojas daqueles estados.

Pediram para você enviar para cada Gerente Geral todas as bases de indicadores
correspondentes às lojas que ele é responsável, porque a equipe deles precisa desses indicadores.

Obs: Não vamos enviar por e-mail porque ainda não aprendemos a fazer isso,
mas vamos deixar todos os arquivos em uma pasta única para cada gerente, ou seja, para cada estado.

Então o seu desafio é separar todos os arquivos de forma que cada arquivo
esteja na pasta do estado correspondente aquele arquivo.

Obs: Para pegar o nome de um arquivo como um texto no pathlib, você pode usar Path.name ou arquivo.name:

caminho = Path('Pasta/Arquivo.csv')
print(caminho.name) -> resposta: 'Arquivo.csv'
"""
from pathlib import Path
import shutil

caminho = Path(r'H:/Meu Drive/Python/Hashtagtreinamentos/programas/Avancado/Arquivos_Pastas/Arquivos_Lojas')
estados = ['RJ', 'SP', 'MG', 'GO', 'AM']

arquivos = caminho.iterdir()
Path(r'pasta_estados').mkdir(exist_ok=True)
for item in estados:
    Path(f'pasta_estados/{item}').mkdir(exist_ok=True)
for arquivo in arquivos:
    for item in estados:
        if item in arquivo.name:
            arquivo_copiar = (caminho / Path(f'{arquivo.name}'))
            destino_copiar = Path(f'pasta_estados/{item}/{arquivo.name}')
            shutil.copy2(arquivo_copiar, destino_copiar)
