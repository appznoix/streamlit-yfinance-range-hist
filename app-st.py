###################################################################
# Imports e inits                                                 #
###################################################################
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

###################################################################
# Funções / Functions                                             #
###################################################################


@st.cache(allow_output_mutation=True)
def yf_get_data(tickers, period, interval):
    '''Puxa os dados do (get symbol data from) Yahoo Finance '''
    return yf.download(tickers=tickers, period=period, interval=interval)


@st.cache
def yf_is_symbol(symbol):
    '''Retorna true se Yahoo Finance tem informações sobre o ativo symbol'''
    s = yf.Ticker(symbol)
    return not (s.info['regularMarketPrice'] == None)


def yf_dataframe(symbol='usdbrl=x', period='2y', interval='1d'):
    '''Prepara os dados e retorna dataframe com dados do Yahoo Finance sobre o ativo symbol'''
    symbol = symbol + '.sa' if not yf_is_symbol(symbol) else symbol
    d = pd.DataFrame() if not yf_is_symbol(
        symbol) else yf_get_data(symbol, period, interval)
    return d


def cooking(df):
    '''Executa o tratamento dos dados. Neste caso, cria a coluna de ranges e elimina as colunas desnecessárias'''
    if len(df) > 0:
        st.write('Dados coletados. Processando...')
        if 'High' in df:
            df['Range'] = abs(df.High - df.Low)
            df.drop(['Open', 'High', 'Low', 'Close',
                     'Adj Close', 'Volume'], axis=1, inplace=True)
        # st.write(df.head())
    else:
        st.write('Ops! Não achei as informações deste ativo. O código pode ter mudado ou ter sido desativado. Confira e tente novamente.')
        return False
    return True


def format_link(text='', name='', url=''):
    '''retorna f string com texto e link para url '''
    return f'{text}[{name}]({url})'


def app_header():
    '''Apresenta o topo da página. Neste caso mostra entrada de código do ativo que será pesquisado'''
    st.title('Frequência diária de variação de preços')
    i = st.text_input(
        'Informe o codigo do ativo: ', 'PETR4')

    st.markdown(
        format_link('Use o formato ', 'Yahoo Finance',
                    'https://br.financas.yahoo.com'),
        unsafe_allow_html=True)
    return i


###################################################################
# Código Principal / Main Code                                    #
###################################################################
# Mostra o cabeçalho da página
s = app_header()
# Busca os dados e cria dataframe
df = yf_dataframe(symbol=s)
# Se os dados estiverem corretos, exibe o histograma correspondente
if cooking(df):
    fig = px.histogram(df,
                       x="Range",
                       nbins=250,
                       labels={'Range': 'Variação diária',
                               'Count': 'Frequência'}
                       )
    st.plotly_chart(fig)
