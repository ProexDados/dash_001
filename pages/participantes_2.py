import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.titulos import Titulo
from components.components import Components
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.graficos import Graficos


# ---------- OBJETOS ----------

config     = Configuracoes()
titulo     = Titulo()
file       = Files()
filtros    = Filtros()
formatacao = Formatacao()
graficos   = Graficos()
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

# ----------- CARDS -----------

media_discentes = df_filtrado['total_discentes_envolvidos'].fillna(0).astype(int).mean()

total_acoes = formatacao.formatar_valor_integer(len(df_filtrado[['id_projeto']].drop_duplicates()))

# ---------- GRÁFICOS ---------

# extensionista por centro
graf_final = graficos.extencionista_centro(df_filtrado)

# bolsas por ano
graf_bolsas = graficos.bolsas_ano(df_filtrado)

# extensionistas por área temática
graf_final_tematica = graficos.extencionista_area(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns((2, 8))

    with col_1:
        # cards
        with st.container(height=455):
            components.metric_card("Média de discentes envolvidos em ações", f"{media_discentes:.2f}".replace(".", ","), "", "#424242")
            st.markdown("<br>", unsafe_allow_html=True)
            components.metric_card("Total de ações", total_acoes, "", "#424242")

    with col_2:
        # extensionista por centro
        with st.container(height=455):
            st.altair_chart(graf_final, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns((2,2))

    with col_1:
        # bolsas por ano
        with st.container(height=280):
            st.altair_chart(graf_bolsas, use_container_width=True)

    with col_2:
        # extensionistas por área temática
        with st.container(height=280):
            st.altair_chart(graf_final_tematica, use_container_width=True)
            