import streamlit as st
import altair as alt


# ===============================================
# CONFIGURAÇÃO DA PÁGINA
# ===============================================
alt.themes.enable("dark")

# ===============================================
# NAVEGAÇÃO
# ===============================================
def navegacao():
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"]::before {
            content: "Índice de navegação";
            display: block;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            padding-left: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    page_1 = st.Page("pages/historico_1.py", title="Histórico Geral 1")
    page_2 = st.Page("pages/historico_2.py", title="Histórico Geral 2")
    page_3 = st.Page("pages/participantes_1.py", title="Participantes 1")
    page_4 = st.Page("pages/participantes_2.py", title="Participantes 2")
    page_5 = st.Page("pages/area_tematica_1.py", title="Área Temática 1")
    page_6 = st.Page("pages/area_tematica_2.py", title="Área Temática 2")
    page_7 = st.Page("pages/orcamento.py", title="Orçamento")
    page_8 = st.Page("pages/unidade_ensino.py", title="Unidade de Ensino")
    page_9 = st.Page("pages/iniciativas_centros.py", title="Iniciativas por Centro")
    page_10 = st.Page("pages/publico.py", title="Público")
    page_11 = st.Page("pages/migracao.py", title="Migração")

    pg = st.navigation(
        [
            page_1,
            page_2,
            page_3,
            page_4,
            page_5,
            page_6,
            page_7,
            page_8,
            page_9,
            page_10
        ],
        position="sidebar"
    )

    pg.run()

if __name__ == "__main__":
    navegacao()
