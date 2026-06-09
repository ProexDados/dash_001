import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.titulos import Titulo
from components.filtros import Filtros
from components.tabelas import Tabelas
from components.graficos import Graficos


# ---------- OBJETOS ----------

config   = Configuracoes()
titulo   = Titulo()
file     = Files()
filtros  = Filtros()
tabela   = Tabelas()
graficos = Graficos()

# ------------ TEMA -----------

config.tema_escuro()

# ----------- LAYOUT ----------

config.layout()

config.remove_espaco()

tema = config.tema()

# ----------- TÍTULO ----------

titulo.titulo("PARTICIPANTES", tema)

# -------- OBTEM DADOS --------

df_participantes = file.participantes()

df_filtrado = df_participantes.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_projeto", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_participantes, "centro", df_filtrado)

    # -------- PARTICIPANTE --------
    df_filtrado = filtros.filtro_participante(df_participantes, "categoria_membro", df_filtrado)

# ---------- GRÁFICOS ---------

# graf_bolsa = graficos.bolsas(df_filtrado)

# discentes por ano
graf_final_discente = graficos.discente_ano(df_filtrado)

# vínculo extensionista
graf_membro = graficos.extensionistas(df_filtrado)

# tabela
df_lista = tabela.membro_categoria(df_filtrado)

# discentes por centro
graf_discente_centro = graficos.discentes_centro(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        # discente por ano
        with st.container(height=350):
            st.altair_chart(graf_final_discente, use_container_width=True)

    with col_2:
        # vínculo extensionista
        with st.container(height=350):
            st.altair_chart(graf_membro, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        # tabela
        with st.container(height=385):
            st.dataframe(df_lista, hide_index=True, height=350)

    with col_2:
        # discentes por centro
        with st.container(height=385):
            st.altair_chart(graf_discente_centro, use_container_width=True)