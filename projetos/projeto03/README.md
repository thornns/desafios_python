###Contexto

No Airbnb, qualquer pessoa que tenha um quarto ou um imóvel de qualquer tipo (apartamento, casa, chalé, pousada, etc.) pode ofertar o seu imóvel para ser alugado por diária.
Você cria o seu perfil de host (pessoa que disponibiliza um imóvel para aluguel por diária) e cria o anúncio.
Nesse anúncio, o host deve descrever as características do imóvel da forma mais completa possível, de forma a ajudar os locadores/viajantes a escolherem o melhor imóvel para eles (e de forma a tornar o seu anúncio mais atrativo)
Existem dezenas de personalizações possíveis no seu anúncio, desde quantidade mínima de diária, preço, quantidade de quartos, até regras de cancelamento, taxa extra para hóspedes extras, exigência de verificação de identidade do locador, etc.

###Objetivo

Construir um modelo de previsão de preço que permita uma pessoa comum que possui um imóvel possa saber quanto deve cobrar pela diária do seu imóvel.
Ou ainda, para o locador comum, dado o imóvel que ele está buscando, ajudar a saber se aquele imóvel está com preço atrativo (abaixo da média para imóveis com as mesmas características) ou não.

###O que temos disponível, inspirações e créditos

As bases de dados foram retiradas do site kaggle: https://www.kaggle.com/allanbruno/airbnb-rio-de-janeiro
As bases de dados são os preços dos imóveis obtidos e suas respectivas características em cada mês.

Os preços são dados em reais (R$)

Temos bases de abril de 2018 a maio de 2020, com exceção de junho de 2018 que não possui base de dados

###Expectativas

Sazonalidade ser um fator importante, visto que meses como dezembro costumam ser mais caros.
Localização do imóvel fazer muita diferença no preço, já que no Rio de Janeiro a localização pode mudar completamente as características do local.
Adicionais/Comodidades podem ter um impacto significativo, visto que temos muitos prédios e casas antigas no Rio de Janeiro

1 - Importar as bases
2 - Consolidar as bases

3 - Identificar quais colunas podem ser removidas
Colunas com ID
Colunas com Descrições (não será feita análise de textos)
Colunas com URL's (Fotos, Sites, Perfil etc...)
Colunas repetidas ou parecidas (coluna com data e colunas com ano ou mês, por exemplo)
Colunas vazias, praticamente vazias ou com todos (ou quase todos) os valores repetidos

4 - Tratar valores vazios

5 - Verificar os tipos de dados nas colunas

6 - Análise e tratamento de outliers
    Dados numéricos contínuos (preço) e discretos (quantidade de quartos)
    Dados em texto (categorias)
    Dados em listas
    Dados em mapa (dicionario)
6.1 - Ver a correlação entre as features e decidir se mantém ou não
      (correlação muito forte (0.9, por exemplo) indica que as colunas dizem "a mesma coisa" e você pode remover uma)
6.2 - Excluir outliers onde (Q1 - 1.5 x Amplitude) e (Q3 + 1.5 x Amplitude). Amplitude = Q3 - Q1
6.2 - Confirmar se todas as features fazem sentido e remover as que não fizerem

Analisar as colunas 1 a 1 e decidir sobre a exclusão dos outliers

### Texto
Avaliar como as quantidades se distribuem na tabela
Avaliar a dispersão dos itens e entender se é necessário criar uma categoria para ele.
Por exemplo: Castelo, Ilha, Avião... além de serem poucos (menos de 100 cada), não condizem com o objetivo.

7 - Encoding - Os modelos de previsão trabalham apenas com números, precisamos tratar as colunas de:
    True (1) or False (0)
    Categorias
        - Trocar por números se houver ordinalidade
        - Criar uma coluna para cada categoria e preencher com 0 ou 1 (Dummies)

8 - Previsão
    - Definir se é Classificação (dividir em categorias: SPAM ou Não SPAM) ou Regressão (encontrar valor: velocidade)
    - Escolher as métricas para avaliar o modelo (R² e RSME)
    - Escolher quais modelos (linear regression, random forest, extra tree)
    - Treinar os modelos e testar

9 - Analisar o melhor modelo

10 - Ajuster e melhorias no modelo
A coluna is_business_ready não foi nem usada pelo modelo, podemos remover.
A coluna com o número de amenidades reflete supreendentemente bem no preço, e isso pode significar que:
1 - Ter mais coisas disponíveis na casa eleva seu preço
2 - O cuidado em detalhar o local pode elevar o preço. O trabalho na descrição é maior e indica um host mais atencioso
Tipo de cama não teve tanto efeito no preço
Ano é mais importante que o mês, indicando que a sazonalidade tem menos impacto que a idade do local
Podemos pensar em remover as colunas room_type, visto que 'Hotel Room' tem importancia de 0,03%, 
porém 'Entire Home/Apt' é muito importante para o modelo, então não é uma boa ideia.
Esta análise precisa passar por coluna a coluna, tipo por tipo
A única certeza é que podemos remover is_business_ready.

10 - Deploy
10.1 - Escolher a forma: Executável (Tkinter), API (Flask), Uso direto (Streamlit)
Criar um arquivo joblib e usar no deployment.py
