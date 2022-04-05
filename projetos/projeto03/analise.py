import pandas as pd
import pathlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import plotly.express as px
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.model_selection import train_test_split
import joblib

meses = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11,
         'dez': 12}

"""
1 - Importar as bases
2 - Consolidar as bases
"""
csv = pathlib.Path('dataset')
airbnb_df = pd.DataFrame()

for arquivo in csv.iterdir():
    df = pd.read_csv(f'dataset\\{arquivo.name}')
    mes = meses[arquivo.name[:3]]
    ano = int(arquivo.name[-8:].replace('.csv', ''))
    df['mes'] = mes
    df['ano'] = ano
    airbnb_df = pd.concat([airbnb_df, df])

airbnb_df.to_csv(r'dataset\total.csv', sep=';', index=False)
airbnb_df = pd.read_csv(r'dataset\total.csv', sep=';')

"""
3 - Identificar quais colunas podem ser removidas
"""
airbnb_df.head(1000).to_csv('primeiros1000.csv', sep=';', index=False)

removidas = ["id", "listing_url", "scrape_id", "last_scraped", "name", "summary", "space", "description",
             "experiences_offered", "neighborhood_overview", "notes", "transit", "access", "interaction",
             "house_rules", "thumbnail_url", "medium_url", "picture_url", "xl_picture_url", "host_id",
             "host_url", "host_name", "host_since", "host_location", "host_about", "host_acceptance_rate",
             "host_thumbnail_url", "host_picture_url", "host_neighbourhood", "host_total_listings_count",
             "host_verifications", "host_has_profile_pic", "host_identity_verified", "street", "neighbourhood",
             "neighbourhood_cleansed", "neighbourhood_group_cleansed", "city", "state", "zipcode", "market",
             "smart_location", "country_code", "country", "is_location_exact", "square_feet", "weekly_price",
             "monthly_price", "calendar_updated", "has_availability", "availability_30", "availability_60",
             "availability_90", "availability_365", "calendar_last_scraped", "first_review", "last_review",
             "requires_license", "license", "jurisdiction_names", "require_guest_profile_picture",
             "require_guest_phone_verification", "calculated_host_listings_count", "reviews_per_month",
             "minimum_minimum_nights", "maximum_minimum_nights", "minimum_maximum_nights", "maximum_maximum_nights",
             "minimum_nights_avg_ntm", "maximum_nights_avg_ntm", "number_of_reviews_ltm",
             "calculated_host_listings_count_entire_homes", "calculated_host_listings_count_private_rooms",
             "calculated_host_listings_count_shared_rooms"]

mantidas = ['host_response_time', 'host_response_rate', 'host_is_superhost', 'host_listings_count', 'latitude',
            'longitude', 'property_type', 'room_type', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'bed_type',
            'amenities', 'price', 'security_deposit', 'cleaning_fee', 'guests_included', 'extra_people',
            'minimum_nights', 'maximum_nights', 'number_of_reviews', 'review_scores_rating', 'review_scores_accuracy',
            'review_scores_cleanliness', 'review_scores_checkin', 'review_scores_communication',
            'review_scores_location', 'review_scores_value', 'instant_bookable', 'is_business_travel_ready',
            'cancellation_policy', 'mes', 'ano']

airbnb_df = airbnb_df.loc[:, mantidas]

"""
4 - Tratar valores vazios
"""
# Descobrir quantos valores vazios existem em cada coluna para avaliar a ação a ser tomada
print(airbnb_df.isnull().sum())

# As colunas com mais de 300k valores nulos serão excluídas, pois poderiam enviesar o resultado (300k é 1/3 das linhas)
for coluna in airbnb_df:
    if airbnb_df[coluna].isnull().sum() > 300000:
        airbnb_df = airbnb_df.drop([coluna], axis=1)

# As outras colunas, serão removidas as LINHAS com valores null (cerca de 2~3k linhas em um universo de 900k+)
airbnb_df = airbnb_df.dropna()
airbnb_df = airbnb_df.reset_index(drop=True)

"""
5 - Verificar os tipos de dados nas colunas
"""
print(airbnb_df.dtypes)
print('-'*60)
print(airbnb_df.iloc[0])

# price e extra_people estão sendo reconhecidos como texto, apesar de serem valores monetários.
# 1 - avaliar os separadores: , para milhar e . para centavos ($1,000.00)
# 2 - trocar os valores: remover $ e , (float32 ocupa menos espaço.)
airbnb_df['price'] = airbnb_df['price'].str.replace('$', '', regex=False)
airbnb_df['price'] = airbnb_df['price'].str.replace(',', '', regex=False)
airbnb_df['price'] = airbnb_df['price'].astype(np.float32, copy=False)

airbnb_df['extra_people'] = airbnb_df['extra_people'].str.replace('$', '', regex=False)
airbnb_df['extra_people'] = airbnb_df['extra_people'].str.replace(',', '', regex=False)
airbnb_df['extra_people'] = airbnb_df['extra_people'].astype(np.float32, copy=False)

"""
6 - Análise e tratamento de outliers
"""
# 6.1
rcParams.update({'figure.autolayout': True})
sns.heatmap(airbnb_df.corr(), annot=True, cmap='Greens')
# plt.show()

# 6.2
def limites(colunas) -> tuple:
    """
    Calcula o limite inferior e limite superior de uma coluna em um DataFrame, para posterior identificação de outliers
    :param colunas: Uma coluna do DataFrame
    :return: Tupla com o limite inferior e superior
    """
    q1 = colunas.quantile(0.25)
    q3 = colunas.quantile(0.75)
    amplitude = q3 - q1
    limit_inf = q1 - 1.5 * amplitude
    limit_sup = q3 + 1.5 * amplitude
    return limit_inf, limit_sup

def diagrama_caixa(colunas):
    """
    Define 02 gráficos de caixa.
    O primeiro contém todos os valores da coluna do DataFrame
    O segundo contém apenas os valores dentro dos limites inferior e superior definidos na função limites
    :param colunas: A coluna do DataFrame a ser analisada
    :return: 02 gráficos de caixa
    """
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(10, 5)

    sns.boxplot(x=colunas, ax=ax1)

    ax2.set_xlim(limites(colunas))
    sns.boxplot(x=colunas, ax=ax2)

def histograma(colunas):
    plt.figure(figsize=(10, 5))
    sns.histplot(colunas)

# Analisar as colunas 1 a 1 e decidir sobre a exclusão dos outliers
# Alterar esse código ao invés de repetir, evitando um código desnecessariamente grande
print(limites(airbnb_df['price']))
diagrama_caixa(airbnb_df['price'])
histograma(airbnb_df['price'])
plt.show()

# Como o objetivo é a previsão de imóveis "comuns", iremos excluir os outliers pois são diárias muito altas
def excluir_outliers(pd_df, colunas):
    num_linhas = pd_df.shape[0]
    limite_inf, limite_sup = limites(pd_df[colunas])
    pd_df = pd_df.loc[(pd_df[colunas] >= limite_inf) & (pd_df[colunas] <= limite_sup), :]
    linhas_removidas = num_linhas - pd_df.shape[0]
    return pd_df, linhas_removidas

airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'price')
print(f'price: {lin_remov} linhas removidas.')  # 87282 é cerca de 10% da base
histograma(airbnb_df['price'])
plt.show()

airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'extra_people')
print(f'extra_people: {lin_remov} linhas removidas.')  # 59194 é cerca de 4% da base

"""
Com valores discretos é melhor barra que histograma
"""
def barra(colunas):
    plt.figure(figsize=(10, 5))
    axs = sns.barplot(x=colunas.value_counts().index, y=colunas.value_counts())
    axs.set_xlim(limites(colunas))

# Alterar esse código ao invés de repetir, evitando um código desnecessariamente grande
print(limites(airbnb_df['host_listings_counts']))
diagrama_caixa(airbnb_df['host_listings_counts'])
barra(airbnb_df['host_listings_counts'])
plt.show()

# Neste caso, o limite superior é 6, então podemos excluir pois nosso objetivo são imóveis "comuns" e não imobiliárias.
# host_listings_count são o número de imóveis que 01 usuário está disponibilizando
airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'host_listings_count')
print(f'host_listings_count: {lin_remov} linhas removidas.')  # 97723 é cerca de 13% da base

# Neste caso, o limite superior é 9, casas que acomodam mais do que essa quantidade de hóspedes tendem a ser grandes.
airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'accommodates')
print(f'accommodates: {lin_remov} linhas removidas.')  # 13146 é cerca de 2% da base

# Neste caso, o limite superior é 3.5 banheiros
airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'bathrooms')
print(f'bathrooms: {lin_remov} linhas removidas.')  # 6894 é cerca de 1% da base

# Neste caso, o limite superior é 3
airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'bedrooms')
print(f'bedrooms: {lin_remov} linhas removidas.')  # 5482 é cerca de 1% da base

# Neste caso, o limite superior é 6
airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'beds')
print(f'beds: {lin_remov} linhas removidas.')  # 5622 é cerca de 1% da base

# Neste caso, os limites estão em 1. Parece que os usuários não costumam preencher essa informação e usam o valor padrão
# Desta forma, será melhor remover a coluna inteira.
print(limites(airbnb_df['guests_included']))
airbnb_df = airbnb_df.drop('guests_included', axis=1)

# Neste caso, o limite superior é 8, não estamos procurando aluguel de temporada. Podemos remover os outliers
airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'minimum_nights')
print(f'minimum_nights: {lin_remov} linhas removidas.')  # 40383 é cerca de 6% da base

# Neste caso, o limite superior é 2000, não estamos procurando aluguel de temporada. Podemos remover a coluna
airbnb_df = airbnb_df.drop('maximum_nights', axis=1)

# Neste caso, o limite superior é 15.
# Além de não parecer impactar no preço, remover locais com mais reviews pode remover hosts mais antigos (ou melhores)
airbnb_df = airbnb_df.drop('number_of_reviews', axis=1)

"""
Análise de colunas com Texto
"""
grafico = sns.countplot('property_type', data=airbnb_df)
grafico.tick_params(axis='x', rotation=90)
plt.show()

tipos_casa_df = airbnb_df['property_type'].value_counts()
agrupar_tipo = []
for tipo in tipos_casa_df.index:
    if tipos_casa_df[tipo] < 2000:
        agrupar_tipo.append(tipo)
for tipo in agrupar_tipo:
    airbnb_df.loc[airbnb_df['property_type'] == tipo, 'property_type'] = 'Outros'

# O novo valor 'Outros' substituiu 8850 valores, em um universo superior a 500.000
print(airbnb_df['property_type'].value_counts())

# Só existem 4 categorias, não precisa alterar.
grafico = sns.countplot('room_type', data=airbnb_df)
grafico.tick_params(axis='x', rotation=90)
plt.show()

# Só existem 5 categorias, mas uma delas é responsável por 90% dos valores (Real Bed)
grafico = sns.countplot('bed_type', data=airbnb_df)
grafico.tick_params(axis='x', rotation=90)
plt.show()

tipos_cancelamento_df = airbnb_df['bed_type'].value_counts()
agrupar_tipo = []
for tipo in tipos_cancelamento_df.index:
    if tipo != 'Real Bed':
        agrupar_tipo.append(tipo)
for tipo in agrupar_tipo:
    airbnb_df.loc[airbnb_df['bed_type'] == tipo, 'bed_type'] = 'Outros'

# O novo valor 'Outros' substituiu 11340 valores, em um universo superior a 500.000
print(airbnb_df['bed_type'].value_counts())

# Só existem 6 categorias, 3 delas muito pequenas e semelhantes entre si (strict)
grafico = sns.countplot('cancellation_policy', data=airbnb_df)
grafico.tick_params(axis='x', rotation=90)
plt.show()

tipos_cancelamento_df = airbnb_df['cancellation_policy'].value_counts()
agrupar_tipo = []
for tipo in tipos_cancelamento_df.index:
    if (tipo == 'strict') or (tipo == 'super_strict_30') or (tipo == 'super_strict_60'):
        agrupar_tipo.append(tipo)
for tipo in agrupar_tipo:
    airbnb_df.loc[airbnb_df['cancellation_policy'] == tipo, 'cancellation_policy'] = 'Restrito'

# O novo valor 'Restrito' substituiu 9863 valores, em um universo superior a 500.000
print(airbnb_df['cancellation_policy'].value_counts())

# Esta solução sobre o número de amenidades foi feita de acordo com o racicínio do dev original: https://www.kaggle.com/allanbruno/airbnb-rio-de-janeiro
# Em resumo: Existem muitas amenities, algumas iguais, mas escritas de forma diferente
# Algumas podem estar descritas ou não (como elevador. Algo tão comum que o host não adicione na lista, mas possua um no local)
# Desta forma, para o modelo, será avaliada QUANTIDADE e não QUAIS amenities.
airbnb_df['numero_amenities'] = airbnb_df['amenities'].str.split(',').apply(len)
airbnb_df = airbnb_df.drop('amenities', axis=1)

# Tratar os outliers da nova coluna, numérica discreta.
diagrama_caixa(airbnb_df['numero_amenities'])
barra(airbnb_df['numero_amenities'])
plt.show()

airbnb_df, lin_remov = excluir_outliers(airbnb_df, 'numero_amenities')
print(f'numero_amenities: {lin_remov} linhas removidas.')

# Mapa Iterativo (latitude e longitude)
amostra = airbnb_df.sample(n=50000)
centro_mapa = {'lat': amostra.latitude.mean(), 'lon': amostra.latitude.mean()}
mapa = px.density_mapbox(amostra,
                         lat='latitude',
                         lon='longitude',
                         z='price',
                         radius=2.5,
                         center=centro_mapa,
                         zoom=10,
                         mapbox_style='stamen-terrain')
mapa.show()

"""
7 - Encoding
"""

# Encoding True or False: host_is_superhost, instant_bookable, is_business_travel_ready
colunas_td = ['host_is_superhost', 'instant_bookable', 'is_business_travel_ready']
airbnb_df_encoding = airbnb_df.copy()

for coluna in colunas_td:
    airbnb_df_encoding.loc[airbnb_df_encoding[coluna] == 't', coluna] = 1
    airbnb_df_encoding.loc[airbnb_df_encoding[coluna] == 'f', coluna] = 0

# Encoding Categorias (Texto) usando Dummies: property_type, room_type, bed_type, cancellation_policy
colunas_categorias = ['property_type', 'room_type', 'bed_type', 'cancellation_policy']
airbnb_df_encoding = pd.get_dummies(data=airbnb_df_encoding, columns=colunas_categorias)

"""
8 - Previsão
"""

def avaliar_modelo(nome_modelo, y_test, previsao_do_modelo):
    """
    :param nome_modelo: Nome do modelo, para identificação
    :param y_test: O preço real
    :param previsao_do_modelo: O preço que o modelo previu
    :return:
    """
    r2 = r2_score(y_test, previsao_do_modelo)
    rsme = np.sqrt(mean_squared_error(y_test, previsao_do_modelo))
    return f'Modelo {nome_modelo}:\nR² = {r2}\nRSME = {rsme}'

# x = variaveis, y = previsao
y = airbnb_df['price']
x = airbnb_df.drop('price', axis=1)

modelo_ef = ExtraTreesRegressor()
modelo_lr = LinearRegression()
modelo_rt = RandomForestRegressor()

modelos = {'Random Forest': modelo_rt,
           'Linear Regression': modelo_lr,
           'Extra Trees': modelo_ef}

# A ordem é importante!!!
# O random_state é para garantir a mesma seed sempre
x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, random_state=0)

for nome, modelo in modelos.items():
    # treino
    modelo.fit(x_treino, y_treino)

    # teste
    previsao = modelo.predict(x_teste)
    print(avaliar_modelo(nome, y_teste, previsao))

"""
9 - Analisar o melhor modelo

ExtraTreesRegressor().feature_importances_:
Retorna uma lista com a % de importancia das colunas (na ordem de x_teste ou x_train)
"""
importancia_colunas = pd.DataFrame(modelo_ef.feature_importances_, x_treino.columns)
importancia_colunas = importancia_colunas.sort_values(by=0, ascending=False)

ax = sns.barplot(x=importancia_colunas.index, y=importancia_colunas[0])
ax.tick_params(axis='x', rotation=90)
plt.show()

joblib.dump(modelo_ef, 'modelo.joblib')
