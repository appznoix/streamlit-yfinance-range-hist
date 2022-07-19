import streamlit as st
def page_header():

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
    page_header()

if __name__ == "__main__":
    main()