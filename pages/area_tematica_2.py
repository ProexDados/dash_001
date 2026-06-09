import streamlit as st
from config.settings import Configuracoes
from components.titulos import Titulo
from services.get_files import Files
from components.filtros import Filtros
from components.graficos import Graficos
from utils.formatacao import Formatacao


# ---------- OBJETOS ----------

config     = Configuracoes()
titulo     = Titulo()
file       = Files()
filtros    = Filtros()
graficos   = Graficos()
formatacao = Formatacao()

# ------------ TEMA -----------

config.tema_escuro()

# ----------- LAYOUT ----------

config.layout()

config.remove_espaco()

tema = config.tema()

# ----------- TÍTULO ----------

titulo.titulo("ÁREA TEMÁTICA", tema)

# -------- OBTEM DADOS --------

df_projeto = file.projeto()

df_filtrado = df_projeto.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_projeto, "ano_projeto", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_projeto, "centro", df_filtrado)

# ---------- GRÁFICOS ---------

# total orçamento por área temática e atividade
graf_tematica = graficos.orcamento_area_atividade(df_filtrado)

# ações por linha de atuação
graf_atuacoes = graficos.acoes_atuacao(df_filtrado)

# nuvem de palavras
fig = graficos.nuvem_tematica(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

col_1a, col_2a = st.columns((8, 8))

with col_1a:
    # total orçamento por área temática e atividade
    with st.container(height=367):
        st.altair_chart(graf_tematica, use_container_width=True)

    # nuvem de palavras
    with st.container(height=368):
        st.pyplot(fig)

with col_2a:
    # ações por linha de atuação
    with st.container(height=750):
        st.altair_chart(graf_atuacoes, use_container_width=True)

