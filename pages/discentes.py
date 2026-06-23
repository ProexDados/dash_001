import pandas as pd
import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.titulos import Titulo
from components.components import Components
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.tabelas import Tabelas
from components.graf_discentes import Graficos


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

titulo.titulo("DISCENTES", tema)

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

df_participantes = df_filtrado[['id_projeto', 'categoria_membro', 'id_pessoa_membro_datageracao']]

df_discentes = df_participantes[df_participantes['categoria_membro'] == 'DISCENTE']
df_discentes_filtrado = df_discentes.drop_duplicates(subset=['id_pessoa_membro_datageracao'])

total_discentes = formatacao.formatar_valor_integer(df_discentes_filtrado['categoria_membro'].count())

df_media_discentes = df_discentes.groupby('id_projeto')['categoria_membro'].count().reset_index()
media_discentes = df_media_discentes['categoria_membro'].fillna(0).astype(int).mean()

# ---------- GRÁFICOS ---------

# discentes por área temática
graf_final_tematica = graficos.discentes_area(df_filtrado)

# discentes por centro
graf_discente_centro = graficos.discentes_centro(df_filtrado)

# discentes por ano
graf_discentes = graficos.discentes_ano(df_sem_ano)

# discentes por atividades de extensão
graf_final_categoria = graficos.graf_discente_categoria(df_filtrado)

# --------- DASHBOARD ---------

col_1, col_2, col_3 = st.columns((2, 4, 4))

with col_1:
    # cards
    with st.container(height=360):
        components.metric_card(
            label="Total de Discentes", 
            value=total_discentes, 
            delta="",
            bg_color="#424242"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        components.metric_card(
            label="Média de Discentes em Ações", 
            value=f"{media_discentes:.2f}".replace(".", ","), 
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
        st.altair_chart(graf_discentes, use_container_width=True)

with col_2b:
    with st.container(height=395):
        st.altair_chart(graf_discente_centro, use_container_width=True)
        