import pandas as pd
import yagmail
from pathlib import Path

pd.set_option('display.width', None)
usuario = yagmail.SMTP(user='danielsantarita@gmail.com',
                       password='')

emails_df = pd.read_excel('Bases de Dados\\Emails.xlsx')
lojas_df = pd.read_csv('Bases de Dados\\Lojas.csv', sep=';', encoding='Latin1')
vendas_df = pd.read_excel('Bases de Dados\\Vendas.xlsx')
print('importadas as bases')
print('')

vendas_df = vendas_df.merge(lojas_df, on='ID Loja')
vendas_df = vendas_df.drop('ID Loja', axis=1)
print('tratadas as bases')
print('')

# Metas
meta_faturamento_dia = 1000
meta_faturamento_ano = 1650000
meta_qtdeprodutos_dia = 4
meta_qtdeprodutos_ano = 120
meta_ticketmedio_dia = 500
meta_ticketmedio_ano = 500

# 1 Dataframe por loja
dic_loja = {}
for loja in vendas_df['Loja'].unique():
    dic_loja[loja] = vendas_df.loc[vendas_df['Loja'] == loja, :]
print('lojas separadas')
print('')

# Definir o dia mais recente
dia = vendas_df['Data'].max()
print('dia definido')
print('')

# Criar diretórios por loja e salvar o excel
for loja in dic_loja:
    # criar dir
    Path(f'Backup Arquivos Lojas/{loja}').mkdir(exist_ok=True)
    # salvar xlsx
    dic_loja[loja].to_excel(f'Backup Arquivos Lojas/{loja}/{dia.month}_{dia.day}_{loja}.xlsx', index=False)
print('diretórios criados e arquivos salvos')
print('')

# Calcular os 3 indicadores
for loja in dic_loja:
    df_ano = dic_loja[loja]
    df_dia = df_ano.loc[df_ano['Data'] == dia, :]

    # 1 - faturamento
    faturamento_ano = df_ano['Valor Final'].sum()
    faturamento_dia = df_dia['Valor Final'].sum()

    # 2 - diversidade de produtos
    diversidade_ano = len(df_ano['Produto'].unique())
    diversidade_dia = len(df_dia['Produto'].unique())

    # 3 - ticket médio
    ticket_ano = df_ano.groupby(['Código Venda']).sum()
    ticket_medio_ano = ticket_ano['Valor Final'].mean()

    ticket_dia = df_dia.groupby(['Código Venda']).sum()
    ticket_medio_dia = ticket_dia['Valor Final'].mean()

# Começo do Tratamento do E-Mail para Gerentes

    # Definindo cor do botão baseado na performance do indicador
    if faturamento_dia >= meta_faturamento_dia:
        cor_fat_dia = 'green'
    else:
        cor_fat_dia = 'red'

    if faturamento_ano >= meta_faturamento_ano:
        cor_fat_ano = 'green'
    else:
        cor_fat_ano = 'red'

    if diversidade_dia >= meta_qtdeprodutos_dia:
        cor_qtde_dia = 'green'
    else:
        cor_qtde_dia = 'red'

    if diversidade_ano >= meta_qtdeprodutos_ano:
        cor_qtde_ano = 'green'
    else:
        cor_qtde_ano = 'red'

    if ticket_medio_dia >= meta_ticketmedio_dia:
        cor_ticket_dia = 'green'
    else:
        cor_ticket_dia = 'red'

    if ticket_medio_ano >= meta_ticketmedio_ano:
        cor_ticket_ano = 'green'
    else:
        cor_ticket_ano = 'red'

    # Definindo o conteúdo do e-mail
    nome = emails_df.loc[emails_df['Loja'] == loja, 'Gerente'].values[0]
    conteudo = f'''
        <p>Bom dia {nome}!</p>

        <p>O resultado de ontem <strong>({dia.day}/{dia.month})</strong> da <strong>Loja {loja}</strong> foi:</p>

        <table>
          <tr>
            <th>Indicador</th>
            <th>Valor Dia</th>
            <th>Meta Dia</th>
            <th>Cenário Dia</th>
          </tr>
          <tr>
            <td>Faturamento</td>
            <td style="text-align: center">R${faturamento_dia:.2f}</td>
            <td style="text-align: center">R${meta_faturamento_dia:.2f}</td>
            <td style="text-align: center"><font color="{cor_fat_dia}">◙</font></td>
          </tr>
          <tr>
            <td>Diversidade de Produtos</td>
            <td style="text-align: center">{diversidade_dia}</td>
            <td style="text-align: center">{meta_qtdeprodutos_dia}</td>
            <td style="text-align: center"><font color="{cor_qtde_dia}">◙</font></td>
          </tr>
          <tr>
            <td>Ticket Médio</td>
            <td style="text-align: center">R${ticket_medio_dia:.2f}</td>
            <td style="text-align: center">R${meta_ticketmedio_dia:.2f}</td>
            <td style="text-align: center"><font color="{cor_ticket_dia}">◙</font></td>
          </tr>
        </table>
        <br>
        <table>
          <tr>
            <th>Indicador</th>
            <th>Valor Ano</th>
            <th>Meta Ano</th>
            <th>Cenário Ano</th>
          </tr>
          <tr>
            <td>Faturamento</td>
            <td style="text-align: center">R${faturamento_ano:.2f}</td>
            <td style="text-align: center">R${meta_faturamento_ano:.2f}</td>
            <td style="text-align: center"><font color="{cor_fat_ano}">◙</font></td>
          </tr>
          <tr>
            <td>Diversidade de Produtos</td>
            <td style="text-align: center">{diversidade_ano}</td>
            <td style="text-align: center">{meta_qtdeprodutos_ano}</td>
            <td style="text-align: center"><font color="{cor_qtde_ano}">◙</font></td>
          </tr>
          <tr>
            <td>Ticket Médio</td>
            <td style="text-align: center">R${ticket_medio_ano:.2f}</td>
            <td style="text-align: center">R${meta_ticketmedio_ano:.2f}</td>
            <td style="text-align: center"><font color="{cor_ticket_ano}">◙</font></td>
          </tr>
        </table>

        <p>Segue em anexo a planilha com todos os dados para mais detalhes.</p>

        <p>Qualquer dúvida estou à disposição.</p>
        <p>Att., Daniel Malizia</p>
        '''

    # Envio do E-Mail
    usuario.send(to=emails_df.loc[emails_df['Loja'] == loja, 'E-mail'].values[0],
                 subject=f'OnePage Dia {dia.day}/{dia.month} - Loja {loja}',
                 contents=conteudo,
                 attachments=f'H:\\Meu Drive\\Python\\Hashtagtreinamentos\\programas\\Projetos\\Automacao_Indicadores\\'
                             f'Backup Arquivos Lojas\\{loja}\\{dia.month}_{dia.day}_{loja}.xlsx')
    print(f'email da loja {loja} enviado')

# Criando estrutura de rankings para a Diretoria
fat_lojas_ano_df = vendas_df.groupby(['Loja'])[['Loja', 'Valor Final']].sum()
fat_lojas_ano_df = fat_lojas_ano_df.sort_values(by='Valor Final', ascending=False)
fat_lojas_ano_df.to_excel(f'Backup Arquivos Lojas/{dia.month}_{dia.day}_Ranking Anual.xlsx', index=False)

vendas_dia_df = vendas_df.loc[vendas_df['Data'] == dia, :]
fat_lojas_dia_df = vendas_dia_df.groupby(['Loja'])[['Loja', 'Valor Final']].sum()
fat_lojas_dia_df = fat_lojas_dia_df.sort_values(by='Valor Final', ascending=False)
fat_lojas_dia_df.to_excel(f'Backup Arquivos Lojas/{dia.month}_{dia.day}_Ranking Diário.xlsx', index=False)
print('Estruturas para Diretoria Criadas')
print('')

usuario.send(to=emails_df.loc[emails_df['Loja'] == 'Diretoria', 'E-mail'].values[0],
             subject=f'Ranking Dia {dia.day}/{dia.month}',
             contents=f'''
             Prezados, Bom dia!
             Melhor loja do dia: {fat_lojas_dia_df.index[0]}, com faturamento de R${fat_lojas_dia_df.iloc[0, 0]:.2f}
             Pior loja do dia: {fat_lojas_dia_df.index[-1]}, com faturamento de R${fat_lojas_dia_df.iloc[-1, 0]:.2f}
             
             Melhor loja do ano: {fat_lojas_ano_df.index[0]}, com faturamento de R${fat_lojas_ano_df.iloc[0, 0]:.2f}
             Pior loja do ano: {fat_lojas_ano_df.index[-1]}, com faturamento de R${fat_lojas_ano_df.iloc[-1, 0]:.2f}
             
             Seguem anexos referente aos ranking anual e diário de todas as lojas.
             Qualquer dúvida, estou à disposição.
             
             Att.,
             Daniel Malizia''',
             attachments=[f'H:\\Meu Drive\\Python\\Hashtagtreinamentos\\programas\\Projetos\\Automacao_Indicadores\\'
                          f'Backup Arquivos Lojas\\{dia.month}_{dia.day}_Ranking Anual.xlsx',
                          f'H:\\Meu Drive\\Python\\Hashtagtreinamentos\\programas\\Projetos\\Automacao_Indicadores\\'
                          f'Backup Arquivos Lojas\\{dia.month}_{dia.day}_Ranking Diário.xlsx'])
print('E-mail da Diretoria enviado. Fim do Projeto.')
print('')
