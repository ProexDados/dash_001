import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.components import Components
from components.titulos import Titulo
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.tabelas import Tabelas
from components.graficos import Graficos


# ---------- OBJETOS ----------

config     = Configuracoes()
titulo     = Titulo()
file       = Files()
filtros    = Filtros()
formatacao = Formatacao()
tabelas    = Tabelas()
graficos   = Graficos()
components = Components()

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

    # -------- SITUAÇÃO --------
    df_filtrado = filtros.filtro_situacao(df_projeto, "situacao_projeto", df_filtrado)

# ----------- CARDS -----------

df_filtrado = df_filtrado.sort_values(by='ano_projeto', ascending=False)

total_acoes = formatacao.formatar_valor_integer(len(df_filtrado))

# ---------- GRÁFICOS ---------

# quantidade de ações pela situação do projeto
graf_acoes = graficos.graf_acoes(df_filtrado)

# quantidade de ações por atividades de extensão
graf_final_categoria = graficos.graf_categoria(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns((2, 8))

    with col_1:
        # card
        with st.container(height=235):
            components.metric_card("Total Ações", total_acoes, "", "#424242")

    with col_2:
        # tabela
        with st.container(height=235):
            tabelas.ano_titulo(df_filtrado)

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        # quantidade de ações pela situação do projeto
        with st.container(height=500):
            st.altair_chart(graf_acoes, use_container_width=True)

    with col_2:
        # quantidade de ações por atividade de extensão
        with st.container(height=500):
            st.altair_chart(graf_final_categoria, use_container_width=True)
