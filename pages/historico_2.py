import streamlit as st
from services.get_files import Files
from components.filtros import Filtros
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
filtros = Filtros()

df_projeto = file.projeto()
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])
df_projeto = df_projeto[df_projeto["tipo_projeto"] == "EXTENSÃO"]

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


dados_tema = df_filtrado.groupby(["ano_projeto", "linha_pesquisa_area_tematica"], as_index=False)["id_projeto"].count()
dados_centro = df_filtrado.groupby(["ano_projeto", "centro"], as_index=False)["id_projeto"].count()

financiamento = df_filtrado.groupby(["data_inicio", "orcamento_consolidado_fundo"], dropna=False, as_index=False).agg(qtd_projetos=('id_projeto', 'count'))
financiamento["sem_financiamento"] = np.where(financiamento["orcamento_consolidado_fundo"].isna(), financiamento["qtd_projetos"], 1)
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
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "linha_pesquisa_area_tematica:N",
            title=None
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="greens")
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:O", title="Ano"),
            alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área temática"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=365,
        title="Quantidade de ações por ano e área temática"
    )
    .configure_title(
        fontSize=20
    )
)

# centro
graf_centro = (
    alt.Chart(dados_centro)
    .mark_rect()
    .encode(
        x=alt.X(
            "ano_projeto:O",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "centro:N",
            title=None
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="reds")
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:O", title="Ano"),
            alt.Tooltip("centro:N", title="Centro"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=365,
        title="Quantidade de ações por ano e centro"
    )
    .configure_title(
        fontSize=20
    )
)


graf = (
    alt.Chart(df_finan)
    .mark_line(point=alt.OverlayMarkDef(
            color="#EF4136"
        )
    )
    .encode(
        x=alt.X(
            "ano:T", 
            title=None
        ),
        y=alt.Y(
            "valor:Q", 
            title=None
        ),
        color=alt.Color(
            "serie:N", 
            scale=alt.Scale(
                range=["#b41f1f", "#067722"]
            ),title="Série"
        ),
        tooltip=[
            alt.Tooltip("ano:T"),
            alt.Tooltip("serie:N"),
            alt.Tooltip("valor:Q")
        ]
    )
    .properties(
        height=300,
        title="Quantidade de ações por aporte financeiro"
    )
    .configure_title(
        fontSize=20
    )
)

st.markdown("<br>", unsafe_allow_html=True)

with st.container(height=335):
    st.altair_chart(graf, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        with st.container(height=400):
            st.altair_chart(graf_tematica, use_container_width=True)

    with col_2:
        with st.container(height=400):
            st.altair_chart(graf_centro, use_container_width=True)
