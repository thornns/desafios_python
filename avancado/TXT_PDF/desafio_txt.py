"""
Desafio onde vamos aprender:
Na Hashtag, sempre analisamos o nosso "Funil de Vendas".
Para isso, rastreamos de onde veio os alunos por meio de um código, do tipo:

hashtag_site_org -> Pessoas que vieram pelo site da Hashtag
hashtag_yt_org -> Pessoas que vieram pelo Youtube da Hashtag
hashtag_ig_org -> Pessoas que vieram pelo Instagram da Hashtag
hashtag_igfb_org -> Pessoas que vieram pelo Instagram ou Facebook da Hashtag
Os códigos diferentes disso, são códigos de anúncio da Hashtag.

Queremos analisar quantos alunos vieram de anúncio e quantos vieram "orgânico".
Qual a melhor fonte "orgânica" de alunos
Obs: orgânico é tudo aquilo que não veio de anúncios.

No nosso sistema, conseguimos exportar um txt com as informações dos alunos, conforme o arquivo Alunos.txt

(Os dados foram gerados aleatoriamente para simular uma situação real,
já que não podemos fornecer os dados reais dos alunos por questões de segurança)

No final, para treinar, vamos escrever todas essas respostas em um novo arquivo txt
"""

arquivo = open(r'H:\Meu Drive\Python\Hashtagtreinamentos\programas\Avancado\TXT e PDF\Alunos.txt', 'r')
lista_lines = arquivo.readlines()
del lista_lines[:4]

site = 0
youtube = 0
ig_fb = 0
anuncios = 0

for linha in lista_lines:
    email, origem = linha.split(',')
    if '_org' in origem:
        if 'hashtag_site_' in origem:
            site += 1
        if 'hashtag_yt_' in origem:
            youtube += 1
        if 'hashtag_igfb_' or 'hashtag_ig_' in origem:
            ig_fb += 1
    else:
        anuncios += 1

arquivo.close()

with open('resultado.txt', 'w') as resultado:
    resultado.write(f'Vindos do Site: {site}\n')
    resultado.write(f'Vindos do Youtube: {youtube}\n')
    resultado.write(f'Vindos do Instagram ou Facebook:{ig_fb}\n')
    resultado.write(f'Vindo de Anúncios: {anuncios}')

