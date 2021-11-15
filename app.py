#from MT5 import init, account, end
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import dateutil.relativedelta
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.abspath('../../appznoix'))
from MT5 import init, end, getDealsHistory

#from appznoix.MT5 import init, end, getDealsHistory

####################################################


def getDeals():
    '''Retorna todas as ordens já executadas de um período predeterminado'''
    # selecionar as datas de inicio e fim do periodo
    dateTo = datetime.datetime.now()  # hoje
    dateFrom = dateTo + \
        dateutil.relativedelta.relativedelta(years=-2)  # 2 anos atras
    # carrega as ordens executadas entre as datas
    return getDealsHistory(dateFrom, dateTo, True)


@st.cache
def cookDataframe():
    '''Cria o dataframe e usa st.cache para otimização e performance'''
    deals = getDeals()  # carrega as ordens executadas
    # Cria dataframe
    d = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
    # trata symbols (nome dos ativos) da série WIN$
    d["symbol"] = np.where(d["symbol"].str.slice(0, 3)
                           == "WIN", "WIN$", d["symbol"])
    # TODO: usar np.select para permitir varias séries sem comprometer a performance
    # d["symbol"] = np.where(d["symbol"].str.slice(0, 3)
    #                       == "WDO", "WDO$", d["symbol"])
    d = fix_df(d)
    return d  # d <=> Dataframe


def listSymbol():
    '''Retorna lista dos ativos em ordem alfabética'''
    s = df.symbol.unique()
    s = np.sort(s)
    return list(s)


def getMultiselectSymbols():
    '''Retorna widget para multiselecão de ativos'''
    return st.multiselect('Multiselect', listSymbol())
    # return st.sidebar.multiselect('Multiselect', listSymbol())


def addAccumulator(df):
    '''Adiciona coluna de acumulação de resultados por ativo e remove as colunas que ficaram inúteis'''

    # **Normaliza valores das operações** #
    # Quando for ação, reduz volume a um lote (100 unidades) e ajusta o valor
    # Quando for indice, reduz volume a uma unidade e ajusta o valor
    # Use newProfit para normalizar valores
    df['newProfit'] = np.where(df["symbol"].str.slice(0, 3) == "WIN",
                               (df["profit"] / df["volume"]),
                               (df["profit"] / (df["volume"] / 100))
                               )
    # Cria coluna com acumulador de resultados
    df["amount"] = df.groupby(["symbol"]).newProfit.cumsum()
    # Use a profit para usar os valores sem normalização
    # df["amount"] = df.groupby(["symbol"]).profit.cumsum()

    # Elimina colunas desnecessárias
    df.drop(['volume', 'profit', 'newProfit'], inplace=True, axis=1)
    return df


def fix_df(df):
    '''Trata os dados do dataframe'''
    # Remove colunas desnecessárias
    df.drop([
        "external_id", "magic", "swap", "commission", "fee", "price",
        "ticket", "order", "time_msc", "type", "entry", "position_id",
        "reason", "comment"
    ], inplace=True, axis=1)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Calcula coluna de acumulador
    df = addAccumulator(df)
    # faz de time a coluna de indexação
    df.set_index('time', inplace=True)
    return df


def showCharts():
    # Agrupa os dados
    dfg = dfs.groupby("symbol")
    for name, group in dfg:
        g = group[['amount']]
        if name in ativos_select:
            st.write(name)
            st.line_chart(g)


###########################################################
# conecta a plataforma para obter os dados
init(True)


# pega os dados tratados
df = cookDataframe()

### Seleção de Ativos ###
# cria a lista de seleção de ativos
ativos_select = getMultiselectSymbols()
# Filtra os dados dos ativos selecionados.
dfs = df.loc[df['symbol'].isin(ativos_select)]
st.title('Resultado de Operações')
# Mostra os gráficos selecionados
showCharts()
end()
