import altair as alt
import streamlit as st


class Configuracoes:
    def __init__(self):
        ...


    def tema_escuro(self):
        return alt.theme.enable("dark")
    

    def tema_claro(self):
        return alt.theme.enable("none")
    

    def layout(self):
        return st.set_page_config(layout="wide")
    

    def remove_espaco(self):
        return st.markdown("""
                    <style>
                    /* Remove espaço superior do container principal */
                    .block-container {
                        padding-top: 2rem !important;
                    }
                    </style>
                    """, unsafe_allow_html=True
                )
    

    def tema(self):
        return st.get_option("theme.base")