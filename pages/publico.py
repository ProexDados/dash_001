import streamlit as st
from config.settings import Configuracoes
from components.titulos import Titulo
from services.get_files import Files
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.components import Components
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

titulo.titulo("PÚBLICO", tema)

# -------- OBTEM DADOS --------

df_projeto = file.projeto()

df_filtrado = df_projeto.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_projeto, "ano_projeto", df_filtrado)

    # ---------- TÍTULO ---------
    df_filtrado = filtros.filtro_titulo(df_projeto, "titulo", df_filtrado)

    # -------- ID PROJETO -------
    df_filtrado = filtros.filtro_id_projeto(df_projeto, "id_projeto", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_projeto, "centro", df_filtrado)

# ----------- CARDS -----------

# público estimado interno
publico_interno = (
    df_filtrado[
        [
            'id_projeto', 
            'publico_estimado_interno'
        ]
    ]
    .drop_duplicates(subset='id_projeto')
    .fillna(0)
    .astype(int)
    .sum()
)

publico_interno["publico_estimado_interno"] = formatacao.formatar_valor_integer(publico_interno["publico_estimado_interno"])

# público estimado externo
publico_externo = (
    df_filtrado[
        [
            'id_projeto', 
            'publico_estimado_externo'
        ]
    ]
    .drop_duplicates(subset='id_projeto')
    .fillna(0)
    .astype(int)
    .sum()
)

publico_externo["publico_estimado_externo"] = formatacao.formatar_valor_integer(publico_externo["publico_estimado_externo"])

# público atendido
publico_atendido = (
    df_filtrado[
        [
            'id_projeto', 
            'publico_atendido'
        ]
    ]
    .drop_duplicates(subset='id_projeto')
    .fillna(0)
    .astype(int)
    .sum()
)

publico_atendido["publico_atendido"] = formatacao.formatar_valor_integer(publico_atendido["publico_atendido"])

# ---------- GRÁFICOS ---------

# estimado interno
graf_interno = graficos.estimado_interno(df_filtrado)

# estimado externo
graf_externo = graficos.estimado_externo(df_filtrado)

# atendido
graf_atendido = graficos.atendido_ano(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2 = st.columns((0.2, 0.8))

with col_1:
    # card
    # público estimado interno
    with st.container(height=240):
        components.metric_card(
            "Público Estimado Interno", 
            publico_interno['publico_estimado_interno'], 
            "", 
            "#424242"
        )

    # público estimado externo
    with st.container(height=240):
        components.metric_card(
            "Público Estimado Externo", 
            publico_externo['publico_estimado_externo'], 
            "", 
            "#424242"
        )

    # público atendido
    with st.container(height=240):
        components.metric_card(
            "Público Atendido", 
            publico_atendido['publico_atendido'], 
            "", 
            "#424242"
        )

with col_2:
    # estimado interno
    with st.container(height=240):
        st.altair_chart(graf_interno, use_container_width=True)

    # estimado externo
    with st.container(height=240):
        st.altair_chart(graf_externo, use_container_width=True)

    # atendido
    with st.container(height=240):
        st.altair_chart(graf_atendido, use_container_width=True)
        