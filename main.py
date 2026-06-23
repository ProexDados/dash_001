import streamlit as st


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
    
    page_1 = st.Page("pages/historico.py", title="Histórico Geral")
    page_2 = st.Page("pages/participantes.py", title="Participantes")
    page_3 = st.Page("pages/coordenadores.py", title="Coordenadores")
    page_4 = st.Page("pages/discentes.py", title="Discentes")
    page_5 = st.Page("pages/area_tematica.py", title="Área Temática")
    page_6 = st.Page("pages/linha_atuacao.py", title="Linha de Atuação")
    page_7 = st.Page("pages/orcamento.py", title="Orçamento")
    page_8  = st.Page("pages/publico.py", title="Público")

    pg = st.navigation(
        [
            page_1,
            page_2,
            page_3,
            page_4,
            page_5,
            page_6,
            page_7,
            page_8
        ],
        position="sidebar"
    )

    pg.run()

if __name__ == "__main__":
    navegacao()
