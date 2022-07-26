###################################################################
# Imports e inits                                                 #
###################################################################
from comps.mix_vanilla import yf_link
from comps.mix_flavours import body_range_histogram, app_header, st

###################################################################
# Funções / Functions                                             #
###################################################################

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
        #'1mo' : 'Um mês',
    }

    # Entradas/sidebar:
    # Código do ativo
    symbol = st.sidebar.text_input(
        'Informe o código do ativo: ',"", placeholder= 'Ex: PETR4')
    st.sidebar.markdown(yf_link(), unsafe_allow_html=True)

    # Periodo de tempo considerado
    period = st.sidebar.radio(
        "Consultar período de: ",
        ('1d', '5d', ),
        format_func=lambda x: valid_periods.get(x),)

    interval = st.sidebar.radio(
        "Consultar tempo gráfico de:",
        ('1m','2m','5m','15m','30m','60m','90m',),
        format_func=lambda x: valid_timeframes.get(x),)
    # Seleção do modo de exibição
    display = st.sidebar.radio(
        "Exibir variação: ",
        ('Range', 'Range_pct'),
        format_func=lambda x: options.get(x),)
    # Informações sobre o contexto
    return symbol, display, period, interval, (f'Variação {(options.get(display).lower())} (range) de {symbol.upper()} no tempo gráfico de {valid_timeframes.get(interval).lower()} pelo período de {valid_periods.get(period).lower()}') 

###################################################################
# Código Principal / Main Code                                    #
###################################################################
def main():
    # cabeçalho do app
    app_header()
    # Exibe formulário de detalhes do gráfico
    symbol, display, period, interval, display_title = page_header() #symbol é o ativo, display é o formato númerico ou percentual
    # Corpo da página
    body_range_histogram(symbol, display, period, interval, display_title) ##, multiplier )

if __name__ == "__main__":
    main()
