# Raw Package
import streamlit as st
import numpy as np
import pandas as pd

# Data Source
import yfinance as yf

# Data viz
#import plotly.graph_objs as go

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()
# específico para jupyter notebook
# %matplotlib inline
# %matplotlib notebook
pd.set_option('display.max_columns', 500)  # número de colunas mostradas
# max. largura máxima da tabela exibida
pd.set_option('display.width', 1500)


def yf_get_data(tickers, period, interval):
    '''Puxa os dados do Yahoo Finance'''
    return yf.download(tickers=tickers, period=period, interval=interval)


def yf_is_symbol(symbol):
    '''Retorna true se Yahoo Finance tem informações sobre o ativo symbol'''
    s = yf.Ticker(symbol)
    return not (s.info['regularMarketPrice'] == None)


@st.cache(allow_output_mutation=True)
def yf_dataframe(symbol='petr4', period='2y', interval='1d'):
    '''Prepara os dados e retorna dataframe com dados do Yahoo Finance sobre o ativo symbol'''
    symbol = symbol + '.sa' if not yf_is_symbol(symbol) else symbol
    # df = yf_get_data(symbol, period, interval) if yf_is_symbol(
    #     symbol) else pd.DataFrame()
    if yf_is_symbol(symbol):
        df = yf_get_data(symbol, period, interval)
    # df.head()
    return df


def cooking(df):
    '''Calcula diferença diária e deleta colunas desnecessárias'''
    if not 'Range' in df.columns:
        df['Range'] = abs(df.Open - df.Close)
        df.drop(['Date', 'Open', 'High', 'Low', 'Close',
                 'Adj Close', 'Volume'], axis=1, inplace=True)


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
df = yf_dataframe()
# Notify the reader that the data was successfully loaded.
#data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache)")
# Se não houver dados
if len(df) == 0:
    print('Não achei os dados que você queria... \
Será que o código do ativo está correto? \
Ele pode ter mudado ou ter sido desativado.')
    quit()

cooking(df)
st.write('DataFrame')
st.write(df.head())
# grafico
#hist_values = np.histogram(df['Range'], bins=181, range=(0, 180))[0]
st.write('Grupo')
#dfg = df.groupby('Total')['Range'].count()
#dfg = df.pivot_table(values='Range', columns='Range', aggfunc='count')
dfg = df.pivot_table(values='Range', columns='Range', aggfunc='count')
st.write(dfg)
#dfg = dfg.reset_index(drop=True, inplace=True)


#st.write('Grupo 2')
# st.write(dfg.to_numpy())

#dfg = df.groupby('Range')
#x = dfg.size()
# st.write(dfg.head())
#dfg['conta'] = df.groupby(['Range']).agg('count')

hist_values = np.histogram(dfg.to_numpy())
# st.write(dfg.head())
#hist_values = df['Range'].hist(bins=10)
#hist_values = np.histogram(dfg, bins=181, range=(0, 180))[0]
st.bar_chart(hist_values, )


# TODO: input do ativo
