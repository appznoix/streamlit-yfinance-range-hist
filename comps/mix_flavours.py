import streamlit as st
import pandas as pd
import plotly.express as px
from comps.yf_appznoix import check_symbol, get_symbol_data
from comps.mix_vanilla import chart_summary, cooking_range

#############################################
# Funções que precisam importar módulos     #
############################################# 
def app_header(app_title = 'Ranginator', app_header = 'O tamanho do movimento', app_image_file = 'img/clipart2812051.png', app_image_width = 100):
    ''' Exibe o cabeçalho do aplicativo. Neste caso, duas colunas com nome, slogan e imagem '''

    col1, col2 = st.columns(2)# cria duas columas, uma para o titulo e outra para a ilustração

    with col1:
        st.title(app_title)    
        st.text(app_header)

    with col2:
        st.image(app_image_file, width=app_image_width)

def body_range_histogram(symbol, display, period, interval, display_title): 
    ''' Processa os dados e exibe o gráfico. Esta função é o coração do app'''

    # Se não receber um ativo, mostra como informar o simbolo e retorna
    if not symbol:
        st.markdown('Na coluna à esquerda, informe o código do ativo que você quer ver.')
        st.markdown('Toque no botão `>` que aparece no topo, para ver a coluna lateral.')
        return
    
    
    # Busca os dados e determina o codigo do ativo e se existe
    safe_symbol, symbol = check_symbol(symbol) # verifica existência do simbolo informado

    if not safe_symbol: # não foi encontrado ativo com o código informado
        st.write('Ops! Não encontramos informações deste ativo. O código pode não existir, ter sido mudado ou desativado. Confira e tente novamente.')
        return

    df = pd.DataFrame() # dataframe vazio

    # busca os dados e cria dataframe
    with st.spinner(text="Aguarde coleta dos dados. Pode demorar alguns minutos"):
        df = get_symbol_data(symbol=symbol, period=period, interval=interval)

    if cooking_range(df): ##, multiplier): # se o dataframe não estiver vazio, processa os dados e exibe o gráfico
        st.title(display_title)
        bins_chart, summary = chart_summary(df, display)
        st.write(summary)                   #st.write(df) # for debugging
        fig = px.histogram(
            df,
            x=display,
            nbins=bins_chart,
            labels={'Range': 'Variação Númerica',
                    'Range_pct': 'Variação Percentual'}
        )        
        st.plotly_chart(fig)
