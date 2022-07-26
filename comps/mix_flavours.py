import streamlit as st
import pandas as pd
import plotly.express as px
from comps.yf_appznoix import yf_safe_symbol, yf_safe_dataframe
from comps.mix_vanilla import chart_summary, cooking_range

#############################################
# Funções que precisam importar módulos     #
############################################# 
def body_range_histogram(symbol, display, period, interval, display_title): ##, multiplier = 1):
    # Mostra o cabeçalho da página e mostra o formulário de detalhes do gráfico
    if not symbol:
        st.markdown('Na coluna à esquerda, informe o código do ativo que você quer ver.')
        st.markdown('Toque no botão `>` que aparece no topo, para ver a coluna lateral.')
        return
    #else:
    # Busca os dados e cria dataframe    
    #if not not symbol: # processa o gráfico se algum ativo foi informado
    df = pd.DataFrame()
    
    safe_symbol,symbol = yf_safe_symbol(symbol) # verifica existencia do simbolo informado

    if safe_symbol: # se existir, busca os dados do ativo e cria o DataFrame
        with st.spinner(text="Aguarde coleta dos dados. Pode demorar alguns minutos"):
            df = yf_safe_dataframe(symbol=symbol, period=period, interval=interval)
    
        if cooking_range(df): ##, multiplier): # se o dataframe não estiver vazio, processa os dados e exibe o gráfico
            st.title(display_title)
            bins_chart, summary = chart_summary(df, display)
            st.write(summary)
            
            #st.write(df) # for debugging

            fig = px.histogram(
                df,
                x=display,
                nbins=bins_chart,
                labels={'Range': 'Variação Númerica',
                        'Range_pct': 'Variação Percentual'}
            )        
            st.plotly_chart(fig)
    else:
        st.write('Ops! Não encontramos informações deste ativo. O código pode não existir, ter sido mudado ou desativado. Confira e tente novamente.')

def app_header():
    # cria duas columas, uma para o titulo e outra para a ilustração
    col1, col2 = st.columns(2)

    with col1:
        st.title("Ranginator")    
        st.text("O tamanho do movimento")

    with col2:
        st.image("img/clipart2812051.png", width=100)