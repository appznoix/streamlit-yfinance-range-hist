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
def symbol_dataframe(symbol='usdbrl=x', period='1y', interval='1d'):
    '''Retorna dataframe com dados do Yahoo Finance sobre o ativo symbol'''
    d = get_symbol_data(symbol, period, interval)
    return d

def get_symbol_data(tickers, period, interval):
    '''Agrega os dados do (get symbol data from) Yahoo Finance '''
    return yf.download(tickers=tickers, period=period, interval=interval)

@st.cache(show_spinner=False)
def valid_symbol(symbol):
    '''Retorna true se Yahoo Finance tem informações sobre o ativo *symbol*'''
    s = yf.Ticker(symbol)
    return not (s.info['regularMarketPrice'] == None)

@st.cache(show_spinner=False)
def exist_sa_symbol(symbol):
    '''Verifica se o simbolo existe e adiciona .sa caso não'''    
    with st.spinner(text=f'Buscando {symbol.upper()}'):
        is_fine =  valid_symbol(symbol)
    symbol = symbol if is_fine else symbol.upper() + '.SA'
    return symbol, is_fine

def exist_symbol(symbol):
    '''Verifica se o simbolo existe com e sem .sa no final'''
    symbol, found = exist_sa_symbol(symbol)
    if not found:
        with st.spinner(text=f'Buscando {symbol}'):
            found =  valid_symbol(symbol)
    return found, symbol
