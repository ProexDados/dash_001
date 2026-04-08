import streamlit as st
from services.get_files import Files
from components.components import Components
import altair as alt
import pandas as pd
import numpy as np
import locale

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
        st.title("HISTÓRICO GERAL")

# -------- OBTEM DADOS --------
file = Files()
df_projeto = file.projeto()
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])

df_filtrado = df_projeto.copy()

df_filtrado = df_filtrado[df_filtrado['ano_projeto'] < 2030]

# ---------- FILTROS ----------
with st.sidebar:
    st.title("Filtros")
    teste = df_projeto[["ano_projeto"]]
    teste = teste[teste['ano_projeto'] > 2016]
    teste
    # ----------- ANO -----------
    if "filtro_ano" not in st.session_state:
        st.session_state.filtro_ano = sorted(teste["ano_projeto"].unique())

    ano_filtro = st.multiselect(
        "Filtrar por Ano:",
        sorted(df_projeto["ano_projeto"].unique()),
        default=st.session_state.filtro_ano,
    )

    if len(ano_filtro)> 0:
        df_filtrado = df_filtrado[df_filtrado["ano_projeto"].isin(ano_filtro)]

    # ---------- CENTRO ---------
    if "filtro_centro" not in st.session_state:
        st.session_state.filtro_centro = None

    centro_filtro = st.multiselect(
        "Filtrar por Centro:",
        sorted(df_projeto["centro"].unique()),
        default=st.session_state.filtro_centro
    )

    if len(centro_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["centro"].isin(centro_filtro)]

    # -------- CATEGORIA --------
    if "filtro_categoria" not in st.session_state:
        st.session_state.filtro_categoria = None

    categoria_filtro = st.multiselect(
        "Filtrar por categoria:",
        sorted(df_projeto["categoria"].unique()),
        default=st.session_state.filtro_categoria
    )

    if len(categoria_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["categoria"].isin(categoria_filtro)]


dados_tema = df_filtrado.groupby(["ano_projeto", "linha_pesquisa_area_tematica"], as_index=False)["id_projeto"].count()
dados_centro = df_filtrado.groupby(["ano_projeto", "centro"], as_index=False)["id_projeto"].count()

financiamento = df_filtrado.groupby(["data_inicio", "orcamento_consolidado_fundo"], dropna=False, as_index=False).agg(qtd_projetos=('id_projeto', 'count'))
financiamento["sem_financiamento"] = np.where(financiamento["orcamento_consolidado_fundo"].isna(), financiamento["qtd_projetos"], None)
financiamento["com_financiamento"] = np.where(financiamento["orcamento_consolidado_fundo"].notna(), financiamento["qtd_projetos"], None)
financiamento["ano"] = financiamento["data_inicio"].str[:4]

df_long = financiamento.melt(
    id_vars="ano",
    value_vars=["com_financiamento", "sem_financiamento"],
    var_name="serie",
    value_name="valor"
)

df_long['ano'] = pd.to_datetime(df_long['ano'], format="%Y")
df_finan = df_long.groupby(["ano", "serie"], as_index=False)["valor"].sum()


# ---------- GRÁFICOS ---------
# tematica
graf_tematica = (
    alt.Chart(dados_tema)
    .mark_rect()
    .encode(
        x=alt.X(
            "ano_projeto:O",
            title="Ano"
        ),
        y=alt.Y(
            "linha_pesquisa_area_tematica:N",
            title="Status"
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="blues")
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:O", title="Ano"),
            alt.Tooltip("linha_pesquisa_area_tematica:N", title="Status"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=400,
        title="Quantidade de ações por ano e área temática"
    )
)

# centro
graf_centro = (
    alt.Chart(dados_centro)
    .mark_rect()
    .encode(
        x=alt.X(
            "ano_projeto:O",
            title="Ano"
        ),
        y=alt.Y(
            "centro:N",
            title="Centro"
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="purples")
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:O", title="Ano"),
            alt.Tooltip("centro:N", title="Centro"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=400,
        title="Quantidade de ações por ano e centro"
    )
)


graf = (
    alt.Chart(df_finan)
    .mark_line()
    .encode(
        x=alt.X("ano:T", title="Data"),
        y=alt.Y("valor:Q", title="Valor"),
        color=alt.Color("serie:N", scale=alt.Scale(
        range=["#b41f1f", "#067722"]
    ),title="Série"),
        tooltip=[
            alt.Tooltip("ano:T"),
            alt.Tooltip("serie:N"),
            alt.Tooltip("valor:Q")
        ]
    )
    .properties(height=400)
)

with st.container():
    st.altair_chart(graf, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        st.altair_chart(graf_tematica, use_container_width=True)

    with col_2:
        st.altair_chart(graf_centro, use_container_width=True)
