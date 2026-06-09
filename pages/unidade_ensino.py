import streamlit as st
from config.settings import Configuracoes
from components.titulos import Titulo
from services.get_files import Files
from components.filtros import Filtros
from components.graficos import Graficos
from components.tabelas import Tabelas


# ---------- OBJETOS ----------

config   = Configuracoes()
titulo   = Titulo()
file     = Files()
filtros  = Filtros()
graficos = Graficos()
tabelas  = Tabelas()

# ------------ TEMA -----------

config.tema_escuro()

# ----------- LAYOUT ----------

config.layout()

config.remove_espaco()

tema = config.tema()

# ----------- TÍTULO ----------

titulo.titulo("UNIDADES DE ENSINO", tema)

# -------- OBTEM DADOS --------

df_projeto = file.projeto()

df_filtrado = df_projeto.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ---------- TÍTULO ---------
    df_filtrado = filtros.filtro_titulo(df_projeto, "titulo", df_filtrado)

    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_projeto, "ano_projeto", df_filtrado)

    # -------- ID PROJETO -------
    df_filtrado = filtros.filtro_id_projeto(df_projeto, "id_projeto", df_filtrado)

    # -------- COORDENADOR ------
    df_filtrado = filtros.filtro_coordenador(df_projeto, "coordenador", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_projeto, "centro", df_filtrado)

# ---------- GRÁFICOS ---------

# ações por centro
graf_barra_acao_centro = graficos.acao_centro(df_filtrado)

# coordenadores por centro
graf_final = graficos.coordenador_centro(df_filtrado)

# ---------- TABELAS ----------

# dados dos projetos
df_lista = tabelas.unidades_ensino(df_filtrado)

# ------------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns((0.5, 0.5))

    with col_1:
        # ações por centro
        with st.container(height=367):
            st.altair_chart(graf_barra_acao_centro, use_container_width=True)

    with col_2:
        # coordenadores por centro
        with st.container(height=367):
            st.altair_chart(graf_final, use_container_width=True)

# dados dos projetos
with st.container(height=368):
    st.dataframe(df_lista, hide_index=True, height=335)
