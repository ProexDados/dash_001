import pandas as pd
import streamlit as st
from dash.config.settings import Configuracoes
from services.get_files import Files
from dash.components.titulos import Titulo
from dash.components.components import Components
from dash.components.filtros import Filtros
from utils.formatacao import Formatacao
from dash.components.tabelas import Tabelas
from dash.components.graf_coordenadores import Graficos


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

titulo.titulo("COORDENADORES", tema)

# -------- OBTEM DADOS --------

df_participantes = file.participantes()

df_participantes["ano_inicio"] = pd.to_datetime(df_participantes["data_inicio"])
df_participantes["ano_inicio"] = df_participantes["ano_inicio"].dt.year

df_sem_ano = df_participantes.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ---------- CENTRO ---------
    df_sem_ano = filtros.filtro_centro(df_participantes, "centro", df_sem_ano)
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_inicio", df_sem_ano, "Ano de Início")

# ----------- CARDS -----------

df_participantes = df_filtrado[['id_projeto', 'funcao_membro', 'id_pessoa_membro_datageracao']]

df_coordenador = df_participantes[df_participantes['funcao_membro'] == 'COORDENADOR(A)']
df_coordenador_filtrado = df_coordenador.drop_duplicates(subset=['id_pessoa_membro_datageracao'])

total_coordenador = formatacao.formatar_valor_integer(df_coordenador_filtrado['funcao_membro'].count())

df_media_coordenador = df_coordenador.groupby(['id_pessoa_membro_datageracao','funcao_membro'])['id_projeto'].count().reset_index()
media_coordenador = df_media_coordenador['id_projeto'].fillna(0).astype(int).mean()

# ---------- GRÁFICOS ---------

# docentes por área temática
graf_final_tematica = graficos.docentes_area(df_filtrado)

# docentes por centro
graf_docente_centro = graficos.docentes_centro(df_filtrado)

# docentes por ano
graf_docentes = graficos.docentes_ano(df_sem_ano)

# docentes por atividades de extensão
graf_final_categoria = graficos.graf_docente_categoria(df_filtrado)

# ações por coordenador
graf_barra_acao_coordenador = graficos.acao_coordenador(df_filtrado)

# --------- DASHBOARD ---------

col_1a, col_2a = st.columns((7, 3))

with col_1a:

    col_1, col_2, col_3 = st.columns((3, 5, 5))

    with col_1:
        # cards
        with st.container(height=360):
            components.metric_card(
                label="Total de Coordenadores", 
                value=total_coordenador, 
                delta="",
                bg_color="#424242"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            components.metric_card(
                label="Média de Ações por Coordenadores", 
                value=f"{media_coordenador:.2f}".replace(".", ","), 
                delta="",
                bg_color="#424242"
            )

    with col_2:
        with st.container(height=360):
            st.altair_chart(graf_final_tematica, use_container_width=True)
            

    with col_3:
        with st.container(height=360):
            st.altair_chart(graf_final_categoria, use_container_width=True)

    col_1b, col_2b = st.columns((5, 5))

    with col_1b:
        with st.container(height=395):
            st.altair_chart(graf_docentes, use_container_width=True)

    with col_2b:
        with st.container(height=395):
            st.altair_chart(graf_docente_centro, use_container_width=True)
        
with col_2a:
    with st.container(height=770):
        st.altair_chart(graf_barra_acao_coordenador, use_container_width=True)
