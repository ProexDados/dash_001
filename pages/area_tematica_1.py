import streamlit as st
from services.get_files import Files
from components.components import Components
from components.filtros import Filtros
import altair as alt
import pandas as pd
import numpy as np
import locale
import plotly.express as px
import plotly.graph_objects as go

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
        st.title("ÁREA TEMÁTICA")

# -------- OBTEM DADOS --------
file = Files()
filtros = Filtros()

df_projeto = file.projeto()
df_membro = file.membro_projeto()

df_projeto = df_projeto[
    [
        "id_projeto", 
        "ano_projeto", 
        "abrangencia",
        "centro", 
        "categoria",
        "total_discentes_envolvidos",
        "data_inicio",
        "bolsas_concedidas",
        "linha_pesquisa_area_tematica",
        "linha_atuacao",
        "tipo_projeto"
    ]
]

df_projeto = df_projeto[df_projeto["tipo_projeto"] == "EXTENSÃO"]

df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])

df_membro["id_projeto"] = df_membro["id_projeto"].astype(int)

df_participantes = pd.merge(
    df_projeto, 
    df_membro, 
    on="id_projeto", 
    how="left"
)

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


# ------------------------------------------------------------------------------
areas_tematicas = (
    df_filtrado[
        [
            'linha_pesquisa_area_tematica'
        ]
    ]
    .drop_duplicates()
    .count()
)

# ------------------------------------------------------------------------------
linha_atuacao = (
    df_filtrado[
        [
            'linha_atuacao'
        ]
    ]
    .drop_duplicates()
    .count()
)

# ------------------------------------------------------------------------------
df_spider = (
    df_filtrado[
        [
            'id_projeto', 
            'linha_pesquisa_area_tematica'
        ]
    ]
    .drop_duplicates(subset='id_projeto')
)

df_spider_agrupado = (
    df_spider
    .groupby(['linha_pesquisa_area_tematica'])['id_projeto']
    .count()
    .sort_values(ascending=False)
    .reset_index()
)

fig_radar = px.line_polar(
    df_spider_agrupado,
    r='id_projeto',
    theta='linha_pesquisa_area_tematica',
    line_close=True
)

fig_radar.update_layout(
    width=470,
    height=470,
    title="Quantidade de ações por área temática",
    title_font=dict(
        size=20
    ),
    margin=dict(
        b=40,
        l=40,
        r=40
    )
)

fig_radar.update_traces(
    fill='toself',
    line=dict(color="#009553"),
    mode='lines+markers',  # <- importante
    marker=dict(size=6),
    hovertemplate=
        "<b>%{theta}</b><br>" +
        "Valor: %{r}<br>" +
        "<extra></extra>"
)

# ------------------------------------------------------------------------------
acoes_tematica_atividade = df_filtrado[
    [
        'id_projeto',
        'categoria',
        'linha_pesquisa_area_tematica'
    ]
]

dados_tematica = (
    acoes_tematica_atividade
    .groupby(['categoria', 'linha_pesquisa_area_tematica'])['id_projeto']
    .count()
    .reset_index()
)

dados_tematica = dados_tematica[dados_tematica['id_projeto'] > 0]

graf_tematica = (
    alt.Chart(dados_tematica)
    .mark_rect()
    .encode(
        x=alt.X(
            "categoria:N",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "linha_pesquisa_area_tematica:N",
            title="Área Temática"
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="reds"),
            legend=alt.Legend(
                format="~s"
            )
        ),
        tooltip=[
            alt.Tooltip("categoria:N", title="Categoria"),
            alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=335,
        title="Ações de extensão por área temática e tipo de atividade de extensão"
    )
    .configure_title(
        fontSize=20
    )
)
# ------------------------------------------------------------------------------
dados_abrangencia = df_filtrado[
    [
        'abrangencia',
        'categoria',
        'linha_pesquisa_area_tematica'
    ]
]

abrangencia_agrupada = (
    dados_abrangencia
    .groupby(['abrangencia', 'categoria'])['linha_pesquisa_area_tematica']
    .count()
    .reset_index()
)

abrangencia_agrupada = abrangencia_agrupada[abrangencia_agrupada['linha_pesquisa_area_tematica'] > 0]

graf_abrangencia = (
    alt.Chart(abrangencia_agrupada)
    .mark_rect()
    .encode(
        x=alt.X(
            "abrangencia:N",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "categoria:N",
            title="Categoria"
        ),
        color=alt.Color(
            "linha_pesquisa_area_tematica:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="greens"),
            legend=alt.Legend(
                format="~s"
            )
        ),
        tooltip=[
            alt.Tooltip("abrangencia:N", title="Abrangência"),
            alt.Tooltip("categoria:N", title="Categoria"),
            alt.Tooltip("linha_pesquisa_area_tematica:Q", title="Quantidade")
        ]
    )
    .properties(
        height=335,
        title="Ações por abrangência e tipo de atividade de extensão"
    )
    .configure_title(
        fontSize=20
    )
)
# ------------------------------------------------------------------------------

# --------- DASHBOARD ---------
st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2 = st.columns((2, 2))

with col_1:
    with st.container(height=230):
        col_1a, col_2a = st.columns((2, 2))
        components = Components()

        with col_1a:
            components.metric_card("Áreas Temáticas", areas_tematicas['linha_pesquisa_area_tematica'], "", "#424242")

        with col_2a:
            components.metric_card("Linhas de Atuação", linha_atuacao['linha_atuacao'], "", "#424242")

    with st.container(height=505):
        st.plotly_chart(fig_radar, use_container_width=True, config={"staticPlot": False})

with col_2:
    with st.container(height=367):
        st.altair_chart(graf_tematica, use_container_width=True)

    with st.container(height=368):
        st.altair_chart(graf_abrangencia, use_container_width=True)