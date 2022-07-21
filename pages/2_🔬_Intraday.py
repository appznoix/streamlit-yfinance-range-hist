###################################################################
# Imports e inits                                                 #
###################################################################
from time import time
import streamlit as st
import pandas as pd
import plotly.express as px
from comps.app_header import app_header    # cabeçalho da página
from comps.yf_appznoix import yf_safe_symbol, yf_safe_dataframe
###################################################################
# Funções / Functions                                             #
###################################################################
# Todos:
# ✔ 1. adicionar valores em percentual 
# 2. valores intraday
# ✔ 4. definir periodos de valores
# ✔ 3. site multi page
# ✔ 5. otimizar código

def cooking_range(df):
    '''Executa o tratamento dos dados. Neste caso, cria a coluna de ranges e elimina as colunas desnecessárias'''
    if len(df) > 0:
        # 1. pega os valor de máxima e mínima do dia
        # 2. Compara
        if 'High' in df:
            # cria colunas com valores que serão usados
            df['Range_pct'] = (df.High/df.Low - 1) * 100
            df['Range'] = abs(df.High - df.Low)
            # elimina colunas desnecessárias
            df.drop(['Open', 'High', 'Low', 'Close',
                     'Adj Close', 'Volume'], axis=1, inplace=True)
    else:
        st.write('Ops! Não encontramos informações deste ativo. O código pode não existir, ter sido mudado ou desativado. Confira e tente novamente.')
        return False
    df.head()
    return True

def format_link(text='', name='', url=''):
    '''retorna f\'string com texto e link para url '''
    return f'{text}[{name}]({url})'


def page_header():
    '''Apresenta o topo da página. Neste caso mostra entrada de código do ativo que será pesquisado'''
    options = {
        'Range': 'Númerica',
        'Range_pct': 'Percentual'
    }
    valid_timeframes = {
        '1m' : 'Um minuto',
        '2m' : 'Dois minutos',
        '5m' : 'Cinco minutos',
        '15m' : 'Quinze minutos',
        '30m' : 'Trinta minutos',
        '60m' : 'Sessenta minutos',
        '90m' : 'Noventa minutos',
        
    }

    valid_periods = {
        '1d' : 'Um dia',
        '5d' : 'Cinco dias',
        '1mo' : 'Um mês',
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

    # Periodo de tempo considerado
    time_limit = st.sidebar.radio(
        "Consultar período de: ",
        ('1d', '5d', '1mo', ),
        format_func=lambda x: valid_periods.get(x),)


    time_frame = st.sidebar.radio(
        "Consultar tempo gráfico de:",
        ('1m','2m','5m','15m','30m','60m','90m',),
        format_func=lambda x: valid_timeframes.get(x),)
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
        st.title(f'Variação {(options.get(display).lower())} (range) de {symbol.upper()} no tempo gráfico de {valid_timeframes.get(time_frame).lower()} pelo período de {valid_periods.get(time_limit).lower()}')

    return symbol, display, time_limit, time_frame


###################################################################
# Código Principal / Main Code                                    #
###################################################################
def main():
    # cabeçalho do app
    app_header()

    # Mostra o cabeçalho da página e mostra o formulário de detalhes do gráfico
    symbol, display, period, interval  = page_header() #symbol é o ativo, display é o formato númerico ou percentual

    # Busca os dados e cria dataframe    
    if not not symbol: # processa o gráfico se algum ativo foi informado
        df = pd.DataFrame()
        
        safe_symbol,symbol = yf_safe_symbol(symbol) # verifica existencia do simbolo informado


        if safe_symbol: # se existir, busca os dados do ativo e cria o DataFrame
            # 
            with st.spinner(text="Aguarde coleta dos dados. Pode demorar alguns minutos"):
                df = yf_safe_dataframe(symbol=symbol, period=period ,interval=interval)
        
        if cooking_range(df): # se o dataframe não estiver vazio, processa os dados e exibe o gráfico
            fig = px.histogram(
                df,
                x=display,
                nbins=250,
                labels={'Range': 'Variação (range)',
                        'Range_pct': 'Variação (range)',
                        'count': 'Frequência'}
            )        
            st.plotly_chart(fig)
        

if __name__ == "__main__":
    main()