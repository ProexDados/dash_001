import streamlit as st
from services.get_files import Files
from components.components import Components
import altair as alt
import pandas as pd
import numpy as np
import locale
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


# ===============================================
# CONFIGURAÇÃO DA PÁGINA
# ===============================================
# alt.themes.enable("blank")

# ----------- LAYOUT ----------
st.set_page_config(
    layout="wide"
)

st.markdown("""
<style>
/* Remove espaço superior do container principal */
.block-container {
    padding-top: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

tema = st.get_option("theme.base")

# ----------- TÍTULO ----------
with st.container():
    col_1, col_2 = st.columns((2, 8))

    with col_1:
        if tema == "dark":
            st.write("")
            st.image("utils/marca_PROEX_2.png")
        else:
            st.write("")
            st.image("utils/marca_PROEX.png")

    with col_2:
        st.title("MIGRAÇÃO")

# -------- OBTEM DADOS --------
file = Files()
df_projeto = file.projeto()
df_membro = file.membro_projeto()

df_projeto = df_projeto[
    [
        "id_projeto", 
        "titulo",
        "ano_projeto", 
        "abrangencia",
        "centro", 
        "categoria",
        "total_discentes_envolvidos",
        "data_fim",
        "coordenador",
        "bolsas_concedidas",
        "linha_pesquisa_area_tematica",
        "linha_atuacao",
        "tipo_projeto",
        "orcamento_consolidado_fundo",
        "palavras_chave",
        "unidade_execucao",
        "situacao_projeto"
    ]
]

df_projeto = df_projeto[df_projeto["tipo_projeto"] == "EXTENSÃO"]

df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])

df_projeto['orcamento_consolidado_fundo'] = (
    df_projeto['orcamento_consolidado_fundo']
    .astype(float)
)


def formatar_valor(df):
    df["valor_formatado"] = (
        df["orcamento_consolidado_fundo"]
        .apply(
            lambda x:
            f"R$ {x:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )

    return df



df_membro["id_projeto"] = df_membro["id_projeto"].astype(int)

df_participantes = pd.merge(
    df_membro, 
    df_projeto, 
    on="id_projeto", 
    how="outer"
)

df_participantes = df_participantes[(df_participantes['ano_projeto'] > 2016) & (df_participantes['ano_projeto'] < 2030)]

df_filtrado = df_participantes.copy()

# ---------- FILTROS ----------
with st.sidebar:
    st.title("Filtros")
    
    # ---------- TÍTULO ---------
    if "filtro_titulo" not in st.session_state:
        st.session_state.filtro_titulo = None

    titulo_filtro = st.multiselect(
        "Filtrar por Título:",
        sorted(df_participantes["titulo"].astype(str).unique()),
        default=st.session_state.filtro_titulo,
    )

    if len(titulo_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["titulo"].isin(titulo_filtro)]

    # ----------- ANO -----------
    if "filtro_ano" not in st.session_state:
        st.session_state.filtro_ano = None

    ano_filtro = st.multiselect(
        "Filtrar por Ano:",
        sorted(df_participantes["ano_projeto"].dropna().astype(int).unique()),
        default=st.session_state.filtro_ano,
    )

    if len(ano_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["ano_projeto"].isin(ano_filtro)]

    # --------- SITUAÇÃO --------
    if "filtro_situacao_projeto" not in st.session_state:
        st.session_state.filtro_situacao_projeto = None

    situacao_projeto_filtro = st.multiselect(
        "Filtrar por Situação Projeto:",
        sorted(df_participantes["situacao_projeto"].dropna().unique()),
        default=st.session_state.filtro_situacao_projeto
    )

    if len(situacao_projeto_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["situacao_projeto"].isin(situacao_projeto_filtro)]

    # ------- COORDENADOR ------
    if "filtro_coordenador" not in st.session_state:
        st.session_state.filtro_coordenador = None

    coordenador_filtro = st.multiselect(
        "Filtrar por Coordenador:",
        sorted(df_participantes["coordenador"].dropna().unique()),
        default=st.session_state.filtro_coordenador
    )

    if len(coordenador_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["coordenador"].isin(coordenador_filtro)]

    # ---------- CENTRO ---------
    if "filtro_centro" not in st.session_state:
        st.session_state.filtro_centro = None

    centro_filtro = st.multiselect(
        "Filtrar por Centro:",
        sorted(df_participantes["centro"].dropna().unique()),
        default=st.session_state.filtro_centro
    )

    if len(centro_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["centro"].isin(centro_filtro)]

# ------------------------------------------------------------------------------

df_lista = df_filtrado[
    [
        "titulo", 
        "coordenador", 
        "data_fim",
        "situacao_projeto",
        "centro"
    ]
]

df_lista["data_fim"] = pd.to_datetime(
    df_lista["data_fim"],
    errors="coerce",
    format="%Y-%m-%d"
).dt.strftime("%d/%m/%Y")

# df_lista["data_fim"] = df_lista["data_fim"].dt.year

df_lista = df_lista.rename(
    columns={
        "titulo": "Título do Projeto",
        "coordenador": "Coordenador",
        "data_fim": "Data de Fim",
        "situacao_projeto": "Situação Projeto",
        "centro": "Centro"
    }
)

df_lista = df_lista.drop_duplicates().dropna()

# ------------------------------------------------------------------------------

with st.container():
    st.dataframe(df_lista, hide_index=True)
