import streamlit as st
def app_header():
    # cria duas columas, uma para o titulo e outra para a ilustração
    col1, col2 = st.columns(2)

    with col1:
        st.title("Ranginator")    
        st.text("O tamanho do movimento")

    with col2:
        st.image("img/clipart2812051.png", width=100)

###################################################################
# Código Principal / Main Code                                    #
###################################################################
def main():
    app_header()

if __name__ == "__main__":
    main()
