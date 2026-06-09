import streamlit as st
from config.settings import Configuracoes
from components.titulos import Titulo
from services.get_files import Files
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.graficos import Graficos
from components.components import Components


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

titulo.titulo("INICIATIVAS POR CENTRO", tema)

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

# ----------- CARDS -----------

card_iniciativas = (
    formatacao.formatar_valor_integer(
        len(
            df_filtrado.drop_duplicates(
                subset="id_projeto"
            )
        )
    )
)

# ---------- GRÁFICOS ---------

# ações por coordenador
graf_barra_acao_coordenador = graficos.acao_coordenador(df_filtrado)

# ações por centro
graf_final_acoes = graficos.acoes_centro(df_filtrado)

# participantes por ano
graf_participantes = graficos.participantes_ano(df_filtrado)

# ações por ano
graf_acoes = graficos.acoes_ano(df_filtrado)

# discentes por ano
graf_discentes = graficos.discentes_ano(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns((0.3, 0.3, 0.3))

with col_1:
    # card
    with st.container(height=235):
        components.metric_card("Total Iniciativas", card_iniciativas, "", "#424242")

    # ações por coordenador
    with st.container(height=500):
        st.altair_chart(graf_barra_acao_coordenador, use_container_width=True)

with col_2:
    # ações por centro
    with st.container(height=367):
        st.altair_chart(graf_final_acoes, use_container_width=True)

    # participantes por ano
    with st.container(height=368):
        st.altair_chart(graf_participantes, use_container_width=True)

with col_3:
    # ações por ano
    with st.container(height=367):
        st.altair_chart(graf_acoes, use_container_width=True)

    # discentes por ano
    with st.container(height=368):
        st.altair_chart(graf_discentes, use_container_width=True)
