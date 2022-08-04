###################################################################
# Imports e inits                                                 #
###################################################################
import streamlit as st
import yfinance as yf
import pandas as pd

###################################################################
# Funções / Functions                                             #
###################################################################
@st.cache(allow_output_mutation=True, show_spinner=False)
def get_symbol_data(symbol='usdbrl=x', period='1y', interval='1d'):
    '''Retorna dataframe com dados do Yahoo Finance sobre o ativo symbol'''
    d = download_symbol_data(symbol, period, interval)
    return d

def download_symbol_data(tickers, period, interval):
    '''Agrega os dados do (get symbol data from) Yahoo Finance '''
    return yf.download(tickers=tickers, period=period, interval=interval)

@st.cache(show_spinner=False)
def check_symbol(symbol):
    '''Verifica se Yahoo Finance reconhece este ativo'''    
    if search_symbol(symbol): # busca o nome do ativo passada
        return True, symbol.upper() # achou o ativo com o symbol passado pelo usuario sem modificação  

    if not search_symbol(symbol.upper()+'.SA'): # adiciona '.SA' ao symbol tenta novamente
        return False, symbol

    return True, symbol.upper()+'.SA' # achou o ativo na segunda passada, retorna adicionando .SA
    

@st.cache(show_spinner=False)
def search_symbol(symbol):
    ''' Retorna True se symbol existe'''
    with st.spinner(text=f'Buscando informações de {symbol.upper()}'):
        found = valid_symbol(symbol)
    return found

@st.cache(show_spinner=False)
def valid_symbol(symbol):
    '''Retorna true se Yahoo Finance tem informações sobre o ativo *symbol*'''
    s = yf.Ticker(symbol)
    return not (s.info['regularMarketPrice'] == None)