import matplotlib.ticker
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

conexao = pyodbc.connect(r"Driver=SQL Server;"
                         r"Server=;"
                         r"Database=ContosoRetailDW;"
                         r"UID=python;"
                         r"PWD=1234567890;")

pd.set_option('display.width', None)
produtos_df = pd.read_sql('select DateKey,'
                          'SalesAmount,'
                          'TotalCost,'
                          'DiscountAmount '
                          'from ContosoRetailDW.dbo.FactSales',
                          conexao)

produtos_df = produtos_df.groupby('DateKey', dropna=False)[['SalesAmount', 'TotalCost', 'DiscountAmount']].sum()

produtos_df['Total Diário'] = produtos_df['SalesAmount'] - produtos_df['TotalCost'] - produtos_df['DiscountAmount']

grafico = produtos_df['Total Diário'].plot(figsize=(15, 5))
grafico.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('${x:,.0f}'))
plt.show()
