import pandas as pd
import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.titulos import Titulo
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.components import Components
from components.tabelas import Tabelas
from components.graf_historico import Graficos


# ---------- OBJETOS ----------

config     = Configuracoes()
titulo     = Titulo()
file       = Files()
filtros    = Filtros()
formatacao = Formatacao()
tabela     = Tabelas()
graficos   = Graficos()
components = Components()

# ------------ TEMA -----------

config.tema_escuro()

# ----------- LAYOUT ----------

config.layout()

config.remove_espaco()

tema = config.tema()

# ----------- TÍTULO ----------

titulo.titulo("HISTÓRICO", tema)

# -------- OBTEM DADOS --------

df_participantes = file.participantes()

df_sem_ano = df_participantes.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ---------- CENTRO ---------
    df_sem_ano = filtros.filtro_centro(df_participantes, "centro", df_sem_ano)
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_projeto", df_sem_ano, "Ano da Ação")

# ---------- CARDS ------------    

df_acoes = df_filtrado.drop_duplicates(subset='id_projeto')

total_acoes = formatacao.formatar_valor_integer(len(df_acoes['id_projeto']))

# ---------- GRÁFICOS ---------

graf_acoes_aporte = graficos.acoes_aporte(df_sem_ano)

graf_centro = graficos.acoes_centro(df_filtrado)

graf_final_categoria = graficos.graf_categoria(df_filtrado)

graf_acoes = graficos.graf_acoes(df_sem_ano)

graf_acoes_ano = graficos.acoes_ano(df_sem_ano)

fig = graficos.nuvem_tematica(df_filtrado)

# --------- DASHBOARD ---------

col_1, col_2 = st.columns(2)

with col_1:
    col_1a, col_1b = st.columns((3, 7))

    with col_1a:
        with st.container(height=185):
            components.metric_card(
                label="Total de Ações", 
                value=total_acoes, 
                delta="",
                bg_color="#424242"
            )

    with col_1b:
        with st.container(height=185):
            st.altair_chart(graf_acoes_aporte)

    col_1c, col_1d = st.columns((5, 6))

    with col_1c:
        with st.container(height=320):
            st.altair_chart(graf_centro)

    with col_1d:
        with st.container(height=320):
            st.pyplot(fig)

with col_2:
    col_2a, col_2b = st.columns(2)

    with col_2a:
        with st.container(height=210):
            st.altair_chart(graf_final_categoria)

    with col_2b:
        with st.container(height=210):
            st.altair_chart(graf_acoes_ano)

    with st.container(height=295):
        st.altair_chart(graf_acoes)

with st.container(height=240):
    tabela.dados_acao(df_filtrado)
