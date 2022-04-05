## Contexto

No Airbnb, qualquer pessoa que tenha um quarto ou um imóvel de qualquer tipo (apartamento, casa, chalé, pousada, etc.) pode ofertar o seu imóvel para ser alugado por diária.
Você cria o seu perfil de host (pessoa que disponibiliza um imóvel para aluguel por diária) e cria o anúncio.
Nesse anúncio, o host deve descrever as características do imóvel da forma mais completa possível, de forma a ajudar os locadores/viajantes a escolherem o melhor imóvel para eles (e de forma a tornar o seu anúncio mais atrativo)
Existem dezenas de personalizações possíveis no seu anúncio, desde quantidade mínima de diária, preço, quantidade de quartos, até regras de cancelamento, taxa extra para hóspedes extras, exigência de verificação de identidade do locador, etc.

## Objetivo

Construir um modelo de previsão de preço que permita uma pessoa comum que possui um imóvel possa saber quanto deve cobrar pela diária do seu imóvel.
Ou ainda, para o locador comum, dado o imóvel que ele está buscando, ajudar a saber se aquele imóvel está com preço atrativo (abaixo da média para imóveis com as mesmas características) ou não.

## O que temos disponível, inspirações e créditos

As bases de dados foram retiradas do site kaggle: https://www.kaggle.com/allanbruno/airbnb-rio-de-janeiro
As bases de dados são os preços dos imóveis obtidos e suas respectivas características em cada mês.

Os preços são dados em reais (R$)

Temos bases de abril de 2018 a maio de 2020, com exceção de junho de 2018 que não possui base de dados

### Expectativas

Sazonalidade ser um fator importante, visto que meses como dezembro costumam ser mais caros.
Localização do imóvel fazer muita diferença no preço, já que no Rio de Janeiro a localização pode mudar completamente as características do local.
Adicionais/Comodidades podem ter um impacto significativo, visto que temos muitos prédios e casas antigas no Rio de Janeiro

## Passos e Considerações

1. Importar as bases
2. Consolidar as bases

3. Identificar quais colunas podem ser removidas
     - Colunas com ID
     - Colunas com Descrições (não será feita análise de textos)
     - Colunas com URL's (Fotos, Sites, Perfil etc...)
     - Colunas repetidas ou parecidas (coluna com data e colunas com ano ou mês, por exemplo)
     - Colunas vazias, praticamente vazias ou com todos (ou quase todos) os valores repetidos

4. Tratar valores vazios

5. Verificar os tipos de dados nas colunas

6. Análise e tratamento de outliers
     - Dados numéricos contínuos (preço) e discretos (quantidade de quartos)
     - Dados em texto (categorias)
     - Dados em listas
     - Dados em mapa (latitude e longitude)
     - Analisar a correlação entre as features e decidir se as mantém ou não
        - Uma correlação muito forte (0.9, por exemplo) indica que as colunas dizem "a mesma coisa" podemos remover uma delas da análise
     - Excluir outliers onde (Q1 - 1.5 x Amplitude) e (Q3 + 1.5 x Amplitude). Amplitude = Q3 - Q1
     - Confirmar se todas as features fazem sentido e remover as que não fizerem

     - Analisar as colunas 1 a 1 e decidir sobre a exclusão dos outliers

### Análise de Texto

Avaliar como as quantidades se distribuem na tabela
Avaliar a dispersão dos itens e entender se é necessário criar uma categoria para eles.
Por exemplo: Castelo, Ilha, Avião... não condizem com o objetivo e seriam melhor agrupados em uma única categoria.

7. Encoding - Os modelos de previsão trabalham apenas com números, precisamos tratar as colunas de:
     - True (1) or False (0)
     - Categorias
        - Trocar texto por números se houver ordinalidade
        - Criar uma coluna para cada categoria e preencher com 0 ou 1 caso não exista ordinalidade

8. Previsão
    - Definir se é Classificação (dividir em categorias: SPAM ou Não SPAM, por exemplo) ou Regressão (encontrar valor: velocidade, preço)
    - Escolher as métricas para avaliar o modelo (usaemos R² e RSME)
    - Escolher quais modelos (usaremo linear regression, random forest e extra tree)
    - Treinar os modelos e testar

9. Analisar o melhor modelo baseado nos resultados do R², RSME e velocidade de execução

10. Ajustes e melhorias no modelo

    - A coluna com o número de amenidades reflete supreendentemente bem no preço, e isso pode significar que:
      - Ter mais coisas disponíveis na casa eleva seu preço
      - O cuidado em detalhar o local pode elevar o preço. O trabalho na descrição é maior e indica um host mais atencioso
    - Tipo de cama não teve tanto efeito no preço
    - Ano é mais importante que o mês, indicando que a sazonalidade tem menos impacto que o ano
    - Poderia pensar em remover as colunas room_type, visto que 'Hotel Room' tem importancia de 0,03%, porém 'Entire Home/Apt' é muito importante para o modelo, então não é uma boa ideia.
    - Esta análise precisa passar por coluna a coluna, tipo por tipo
    - A única certeza é que podemos remover is_business_ready, que foi usada 0%.

![Impacto das Features no Preço](https://i.imgur.com/dfoHLS0.png "Impacto das Features no Preço")

11. Deploy
- Escolher a forma: Executável (Tkinter), API (Flask), Uso direto (Streamlit)
- Criar um arquivo joblib (este arquivo armazena a inteligência artificial já treinada) para usar no deployment.py
