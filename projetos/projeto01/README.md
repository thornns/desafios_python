# Automação de Processos
## Objetivo:
Enviar um e-mail, diáriamente, para todos os gerentes (1 e-mail por gerente) com os indicadores de sua loja:
Faturamento (diário e anual), Diversidade de produtos vendidos (diário e anual) e o Ticket Médio (diário e anual)

Enviar outro e-mail, desta vez para a diretoria, com um ranking das lojas (diário e anual)

Por fim, manter um histórico dessas tabelas

## Formato do e-mail:
![Exemplo do formato de apresentação dos indicadores](https://i.imgur.com/rAi66cA.png)

## Módulos
- Pandas
- Yagmail
- Pathlib PATH

## Passos:
- Importar os arquivos com Pandas[^1]
- Juntar a tabela vendas_df com lojas_df, baseado na coluna ID Loja
- Definir as metas
- Separar os Dataframes por loja
- Criar diretórios (1 por loja) para manter um histórico
- Salvar os Dataframes por loja
- Calcular os 3 Indicadores
- Elaborar o e-mail dos gerentes em HTML (O esqueleto foi montado aqui: https://www.w3schools.com/html/html_tables.asp)
- Editar o HTML para que seja dinâmico, usando as variáveis dos indicadores
- Enviar os e-mails, baseado no Dataframe de E-Mail
- Criar a estrutura requerida pela Diretoria
- Elaborar o e-mail da diretoria
- Enviar o e-mail

[^1]: Os arquivos excel não são meus, por isso, não serão disponibilizados.
