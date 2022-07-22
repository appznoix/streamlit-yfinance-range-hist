###################################################################
# Imports e inits                                                 #
###################################################################
import streamlit as st
from comps.app_header import app_header    # cabeçalho da página
from comps.mix_vanilla import format_link
from comps.mix_flavours import body_range_histogram
###################################################################
# Funções personalizadas / Custom Functions                       #
###################################################################

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
    period = st.sidebar.radio(
        "Consultar período de: ",
        ('6mo', '1y', '2y', '5y', 'ytd', ),
        format_func=lambda x: valid_periods.get(x),)
    # Seleção do modo de exibição
    display = st.sidebar.radio(
        "Exibir variação: ",
        ('Range', 'Range_pct'),
        format_func=lambda x: options.get(x),)
    # Informações sobre o contexto
    return symbol, display, period, '1d', (f'Variação (range) {(options.get(display).lower())} diária de {symbol.upper()} no período de {valid_periods.get(period).lower()}')

###################################################################
# Código Principal / Main Code                                    #
###################################################################
def main():
    # cabeçalho do app
    app_header()
    # Mostra o cabeçalho da página e mostra o formulário de detalhes do gráfico
    symbol, display, period, interval, display_title = page_header() #symbol é o ativo, display é o formato númerico ou percentual
    # Corpo da página 
    body_range_histogram(symbol, display, period, interval, display_title )


if __name__ == "__main__":
    main()