from comps.mix_flavours import app_header, st

def main():
    app_header()

    st.header('Estudo do movimento do preço')
    st.markdown('**Home**: Esta página.')
    st.markdown('**Daily**: valores e percentuais dos movimentos diários completos.')
    st.markdown('**Intraday**: valores e percentuais dos movimentos em diversas frações de tempo menor que um dia.')
    st.header('Pra que?')
    st.markdown('**Avaliar os movimentos** dos preços e entender o comportamento do ativo para planejamento operacional.')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.warning('Este conteúdo não é recomendação de investimento e serve apenas como informação. Investimentos envolvem riscos. A responsabilidade pelo resultado é toda e somente do investidor.')

if __name__ == "__main__":
    main()
################################################################    
# TODO:
# ✔ 1. adicionar valores em percentual 
# ✔ 2. valores intraday
# ✔ 4. definir periodos de valores
# ✔ 3. site multi page
# ✔ 5. otimizar código
# ✔ 6. colocar o numero de itens do dataframe 
# ✔ 7. fazer o numero de bins igual ao de linhas do dataframe
# ✔ 8. conferir os calculos de intraday
# ✔ 9. generalização do código (abstraindo fonte dos dados)
#   10. versão metatrader
################################################################
