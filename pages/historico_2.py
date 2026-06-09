import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.filtros import Filtros
from components.titulos import Titulo
from components.graficos import Graficos


# ---------- OBJETOS ----------

config   = Configuracoes()
file     = Files()
filtros  = Filtros()
titulo   = Titulo()
graficos = Graficos()

# ------------ TEMA -----------

config.tema_escuro()

# ----------- LAYOUT ----------

config.layout()

config.remove_espaco()

tema = config.tema()

# ----------- TÍTULO ----------

titulo.titulo("HISTÓRICO GERAL", tema)

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

    # -------- CATEGORIA --------
    df_filtrado = filtros.filtro_categoria(df_projeto, "categoria", df_filtrado)


# ---------- GRÁFICOS ---------

# aporte financeiro
graf = graficos.acoes_aporte(df_filtrado)

# tematica
graf_tematica = graficos.acoes_tematica(df_filtrado)

# centro
graf_centro = graficos.acoes_centro(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

# aporte financeiro
with st.container(height=335):
    st.altair_chart(graf, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        # tematica
        with st.container(height=400):
            st.altair_chart(graf_tematica, use_container_width=True)

    with col_2:
        # centro
        with st.container(height=400):
            st.altair_chart(graf_centro, use_container_width=True)
