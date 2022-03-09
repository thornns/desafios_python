"""
Digamos que você trabalha em uma indústria e está responsável pela área de inteligência de negócio.

rTodo dia, você, a equipe ou até mesmo um programa, gera um report diferente para cada área da empresa:

Financeiro
Logística
Manutenção
Marketing
Operações
Produção
Vendas
Cada um desses reports deve ser enviado por e-mail para o Gerente de cada Área.

Crie um programa que faça isso automaticamente.
A relação de Gerentes (com seus respectivos e-mails) e áreas está no arquivo 'Enviar E-mails.xlsx'.

Dica: Use o pandas read_excel para ler o arquivo dos e-mails que isso vai facilitar.
"""

import pandas as pd
import yagmail

df = pd.read_excel('Enviar E-mails.xlsx')

usuario = yagmail.SMTP(user='danielsantarita@gmail.com',
                       password='')

for i, email in enumerate(df['E-mail']):

    gerente = df.loc[i, 'Gerente']
    area = df.loc[i, 'Relatório']
    print(area, ' ', email)
    usuario.send(to=email,
                 subject='Relatório de {}'.format(area),
                 contents='Prezado(a) {},\nEm anexo, o relatório de {}'.format(gerente, area),
                 attachments='{}.xlsx'.format(area))
