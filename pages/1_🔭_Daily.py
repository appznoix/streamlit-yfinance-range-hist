###################################################################
# Imports e inits                                                 #
###################################################################
from time import time
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
from comps.app_header import app_header    # cabeçalho da página

###################################################################
# Funções / Functions                                             #
###################################################################
# Todos:
# ✔ 1. adicionar valores em percentual 
# 4. definir periodos de valores
# 3. site multi page
# 2. valores intraday
# 5. otimizar código


@st.cache(allow_output_mutation=True)
def yf_get_data(tickers, period, interval):
    '''Agrega os dados do (get symbol data from) Yahoo Finance '''
    return yf.download(tickers=tickers, period=period, interval=interval)

foo= '''
@st.cache
def yf_is_symbol(symbol):
    \'''Retorna true se Yahoo Finance tem informações sobre o ativo *symbol*\'''
    #with st.spinner(text="Localizando informações do ativo. Aguarde por gentileza. Pode demorar alguns minutos"):
    s = yf.Ticker(symbol)    
    return not (s.info['regularMarketPrice'] == None)


def yf_dataframe(symbol='usdbrl=x', period='1y', interval='1d'):
    \'''Prepara os dados e retorna dataframe com dados do Yahoo Finance sobre o ativo symbol\'''
    symbol = symbol + '.sa' if not yf_is_symbol(symbol) else symbol    
    d = pd.DataFrame() if not yf_is_symbol(
        symbol) else yf_get_data(symbol, period, interval)
    return d
'''
#############

@st.cache(show_spinner=False)
def yf_safe_is_symbol(symbol):
    '''Retorna true se Yahoo Finance tem informações sobre o ativo *symbol*'''
    #with st.spinner(text="Obtendo informações do ativo. Aguarde por gentileza. Pode demorar alguns minutos"):
    s = yf.Ticker(symbol)
    return not (s.info['regularMarketPrice'] == None)

@st.cache(show_spinner=False)
def yf_sa_symbol(symbol):
    '''Verifica se o simbolo existe e adiciona .sa caso não'''    
    with st.spinner(text=f'Buscando {symbol.upper()}'):
        is_fine =  yf_safe_is_symbol(symbol)

    symbol = symbol if is_fine else symbol.upper() + '.SA'
    return symbol, is_fine


def yf_safe_symbol(symbol):
    symbol, found = yf_sa_symbol(symbol)
    if not found:
        with st.spinner(text=f'Buscando {symbol}'):
            found =  yf_safe_is_symbol(symbol)
    return found, symbol


def yf_safe_dataframe(symbol='usdbrl=x', period='1y', interval='1d'):
    '''Prepara os dados e retorna dataframe com dados do Yahoo Finance sobre o ativo symbol'''
    d = yf_get_data(symbol, period, interval)
    return d


def cooking_range(df):
    '''Executa o tratamento dos dados. Neste caso, cria a coluna de ranges e elimina as colunas desnecessárias'''
    if len(df) > 0:
        # 1. pega os valor de máxima e mínima do dia
        # 2. Compara
        if 'High' in df:
            df['Range_pct'] = (df.High/df.Low - 1) * 100
            df['Range'] = abs(df.High - df.Low)
            df.drop(['Open', 'High', 'Low', 'Close',
                     'Adj Close', 'Volume'], axis=1, inplace=True)
    else:
        st.write('Ops! Não encontramos informações deste ativo. O código pode não existir, ter sido mudado ou desativado. Confira e tente novamente.')
        return False
    df.head()
    return True

baz= '''
def cooking(df, calculation):
    \'''Executa o tratamento dos dados. Neste caso, cria a coluna de ranges e elimina as colunas desnecessárias\'''
    if len(df) > 0:
        st.write(f'Dados coletados. Processando tipo {calculation}')
        # 1. pega os valor de máxima e mínima do dia
        # 2. Compara
        if 'High' in df:
            if calculation == 'Percentual':  # Calcular a variação do range entre máxima e mínima do dia
                st.write("Calculando Percentual")
                df['Range'] = (df.High/df.Low - 1) * 100
            else:
                st.write("Calculando Numerico")
                df['Range'] = abs(df.High - df.Low)
            # elimina colunas desnecessárias
            df.drop(['Open', 'High', 'Low', 'Close',
                     'Adj Close', 'Volume'], axis=1, inplace=True)
        # st.write(df.head())
    else:
        st.write('Ops! Não achei as informações deste ativo. O código pode ter mudado ou ter sido desativado. Confira e tente novamente.')
        return False
    df.head()
    return True
'''

def format_link(text='', name='', url=''):
    '''retorna f\'string com texto e link para url '''
    return f'{text}[{name}]({url})'


def page_header():
    '''Apresenta o topo da página. Neste caso mostra entrada de código do ativo que será pesquisado'''
    options = {
        'Range': 'Númerica',
        'Range_pct': 'Percentual'
    }
    valid_periods = {
        '6mo' : 'Seis meses',
        '1y' : 'Um ano',
        '2y' : 'Dois anos',
        '5y' : 'Cinco anos',
        'ytd' : 'Este ano',
    }
    # Entradas/sidebar:
    # Código do ativo
    symbol = st.sidebar.text_input(
        'Informe o código do ativo: ',"", placeholder= 'Ex: PETR4')
    st.sidebar.markdown(
        format_link('🍒 Use o formato ', 'Yahoo Finance',
                    'https://br.financas.yahoo.com'),
        unsafe_allow_html=True)
    # Periodo de tempo considerado
    time_limit = st.sidebar.radio(
        "Consultar período de: ",
        ('6mo', '1y', '2y', '5y', 'ytd', ),
        format_func=lambda x: valid_periods.get(x),)
    # Seleção do modo de exibição
    display = st.sidebar.radio(
        "Exibir variação: ",
        ('Range', 'Range_pct'),
        format_func=lambda x: options.get(x),)
    # Informações sobre o contexto
    #st.write(        f'Range {(options.get(display).lower())} de {symbol.upper()}') 
    if not symbol:
        st.markdown('Na coluna à esquerda, informe o código do ativo que você quer ver.')
        st.markdown('Toque no botão `>` que aparece no topo, para ver a coluna lateral.')
    else:
        st.title(f'Variação {(options.get(display).lower())} diária (range) de {symbol.upper()} no período de {valid_periods.get(time_limit).lower()}')

    return symbol, display, time_limit


###################################################################
# Código Principal / Main Code                                    #
###################################################################
def main():
    # cabeçalho do app
    app_header()

    # Mostra o cabeçalho da página
    symbol, display, time_limit = page_header() #symbol é o ativo, display é o formato númerico ou percentual
    if not not symbol:
    # Busca os dados e cria dataframe    
        df = pd.DataFrame()
        #with st.spinner(text="Checando código do ativo. Pode demorar alguns minutos"):
        safe_symbol,symbol = yf_safe_symbol(symbol) # verifica existencia do simbolo

        if safe_symbol: # se existir, busca os dados do ativo e cria o DataFrame
            with st.spinner(text="Aguarde coleta dos dados. Pode demorar alguns minutos"):
                df = yf_safe_dataframe(symbol=symbol, period=time_limit)
        
        if cooking_range(df): # se o dataframe não estiver vazio, processa os dados e exibe o gráfico
            fig = px.histogram(df,
                            x=display,
                            nbins=250,
                            labels={'Range': 'Variação diária',
                                    'Range_pct': 'Variação diária',
                                    'count': 'Frequência'}
                            )        
            st.plotly_chart(fig)
        

if __name__ == "__main__":
    main()