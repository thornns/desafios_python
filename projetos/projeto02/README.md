### Webscrapping com Selenium - Google Shopping e Buscapé
## Objetivo
Através de um dataframe excel, buscar produtos em uma determinada faixa de preços, evitando termos 'banidos' que possam atrapalhar o resultado

O dataframe possui 4 colunas: Nome, Termos Banidos, Preço Mínimo e Preço Máximo

Exemplo:

| Nome          | Termos Banidos           | Preço Mínimo  | Preço Máximo |
|---------------|--------------------------|---------------|--------------|
|iphone 12 64 gb|         mini watch       |      4200     |     8000     |

## Passos
Para cada produto:
- transformar a coluna 'Nome' em uma lista
- transformar a coluna 'Termos Banidos' em uma lista
- acessar o site
- pesquisar pelo 'Nome'
- clicar na aba Shopping (passo exclusivo do Google Shopping)
- capturar o nome do produto
- confrontar o nome do produto com lista de nomes, verificando se possui todas as palavras-chave
- confrontar o nome do produto com a lista de termos banidos
- capturar o preço do produto (se o passo anterior for bem sucedido)
- tratar o preço do produto, transformando-o em um float
- avaliar se o preço do produto está no intervalo desejado
- capturar a URL do produto (se o passo anterior for bem sucedido)
- retornar uma tupla (Nome, Preço, Link)
- caso a tupla não esteja vazia, concatenar (append) em um dataframe
- caso a tupla esteja vazia, deve ser definida como None

Após os passos acima, salvar o dataframe e o enviar por e-mail.
