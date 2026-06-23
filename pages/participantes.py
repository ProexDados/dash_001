import pandas as pd
import streamlit as st
from dash.config.settings import Configuracoes
from services.get_files import Files
from dash.components.titulos import Titulo
from dash.components.filtros import Filtros
from utils.formatacao import Formatacao
from dash.components.components import Components
from dash.components.tabelas import Tabelas
from dash.components.graf_participantes import Graficos


# ---------- OBJETOS ----------

config   = Configuracoes()
titulo   = Titulo()
file     = Files()
filtros  = Filtros()
formatacao = Formatacao()
tabela   = Tabelas()
graficos = Graficos()
components = Components()

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

df_participantes["ano_inicio"] = pd.to_datetime(df_participantes["data_inicio"])
df_participantes["ano_inicio"] = df_participantes["ano_inicio"].dt.year

df_sem_ano = df_participantes.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ---------- CENTRO ---------
    df_sem_ano = filtros.filtro_centro(df_participantes, "centro", df_sem_ano)
    
    # -------- PARTICIPANTE --------
    df_sem_ano = filtros.filtro_participante(df_participantes, "categoria_membro", df_sem_ano)
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_inicio", df_sem_ano, "Ano de Início")

# ---------- CARDS ------------    

df_total = df_filtrado[['id_projeto', 'categoria_membro', 'id_pessoa_membro_datageracao']]
df_total_unico = df_total.drop_duplicates(subset=['id_pessoa_membro_datageracao'])

contagem_participantes_unicos = df_total_unico.groupby('id_projeto')['categoria_membro'].count().reset_index()
total_participantes = formatacao.formatar_valor_integer(contagem_participantes_unicos['categoria_membro'].sum())

contagem_participantes = df_total.groupby('id_projeto')['categoria_membro'].count().reset_index()
media_participantes = formatacao.formatar_valor_float(contagem_participantes['categoria_membro'].mean())

# ---------- GRÁFICOS ---------

# graf_bolsa = graficos.bolsas(df_filtrado)

# vínculo extensionista
graf_membro = graficos.extensionistas(df_filtrado)

# extensionista por centro
graf_final = graficos.extencionista_centro(df_filtrado)

# participantes por ano
graf_participantes = graficos.participantes_ano(df_sem_ano)

# extensionistas por área temática
graf_final_tematica = graficos.extencionista_area(df_filtrado)

# volume participantes
df_volume = graficos.volume_participante_centro(df_filtrado)

# docentes por atividades de extensão
graf_final_categoria = graficos.graf_participante_categoria(df_filtrado)

# --------- DASHBOARD ---------

with st.container():
    col_1a, col_2a, col_3a = st.columns((4, 3, 3))

    with col_1a:
        with st.container(height=185):
            col_1b, col_2b = st.columns((5, 5))

            with col_1b:
                components.metric_card(
                    label="Total de Participantes Únicos", 
                    value=total_participantes, 
                    delta="",
                    bg_color="#424242"
                )

            with col_2b:
                components.metric_card(
                    label="Média de Participantes por Projeto", 
                    value=media_participantes, 
                    delta="",
                    bg_color="#424242"
                )

        with st.container(height=300):
            st.altair_chart(graf_membro, use_container_width=True)

    with col_2a:
        with st.container(height=500):
            st.altair_chart(graf_final, use_container_width=True)

    with col_3a:
        with st.container(height=500):
            st.altair_chart(df_volume, use_container_width=True)

with st.container():
    col_1b, col_2b, col_3b = st.columns(3)

    with col_1b:
        with st.container(height=255):
            st.altair_chart(graf_final_tematica, use_container_width=True)

    with col_2b:
        with st.container(height=255):
            st.altair_chart(graf_participantes, use_container_width=True)
        
    with col_3b:
        with st.container(height=255):
            st.altair_chart(graf_final_categoria)

