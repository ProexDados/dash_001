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
        st.title("PÚBLICO")

# -------- OBTEM DADOS --------
file = Files()
filtros = Filtros()

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
        "data_inicio",
        "bolsas_concedidas",
        "linha_pesquisa_area_tematica",
        "linha_atuacao",
        "tipo_projeto",
        "orcamento_consolidado_fundo",
        "palavras_chave",
        "publico_estimado_interno",
        "publico_estimado_externo",
        "publico_atendido"
    ]
]

df_projeto = df_projeto[df_projeto["tipo_projeto"] == "EXTENSÃO"]

df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])

df_projeto['orcamento_consolidado_fundo'] = (
    df_projeto['orcamento_consolidado_fundo']
    .astype(float)
)


def formatar_valor(valor):
    valor = (
        f"{valor:,}".replace(",",".")
    )
    
    return valor



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

    # ---------- TÍTULO ---------
    df_filtrado = filtros.filtro_titulo(df_participantes, "titulo", df_filtrado)

    # -------- ID PROJETO -------
    df_filtrado = filtros.filtro_id_projeto(df_participantes, "id_projeto", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_participantes, "centro", df_filtrado)

# ------------------------------------------------------------------------------

publico_interno = (
    df_filtrado[['id_projeto', 'publico_estimado_interno']]
    .drop_duplicates(subset='id_projeto')
    .fillna(0)
    .astype(int)
    .sum()
)

publico_interno["publico_estimado_interno"] = formatar_valor(publico_interno["publico_estimado_interno"])

# ------------------------------------------------------------------------------

publico_externo = (
    df_filtrado[['id_projeto', 'publico_estimado_externo']]
    .drop_duplicates(subset='id_projeto')
    .fillna(0)
    .astype(int)
    .sum()
)

publico_externo["publico_estimado_externo"] = formatar_valor(publico_externo["publico_estimado_externo"])

# ------------------------------------------------------------------------------

publico_atendido = (
    df_filtrado[['id_projeto', 'publico_atendido']]
    .drop_duplicates(subset='id_projeto')
    .fillna(0)
    .astype(int)
    .sum()
)

publico_atendido["publico_atendido"] = formatar_valor(publico_atendido["publico_atendido"])

# ------------------------------------------------------------------------------

df_interno = df_filtrado[['id_projeto', 'publico_estimado_interno', 'data_inicio']]
df_interno = df_interno.drop_duplicates(subset='id_projeto')


df_interno['publico_estimado_interno'] = df_interno['publico_estimado_interno'].fillna(0).astype(int)
df_interno['ano'] = df_interno['data_inicio'].astype(str).str[:4]

df_interno_agrupadas = (
    df_interno.groupby('ano')['publico_estimado_interno']
    .sum()
    .reset_index()
)

df_interno_agrupadas['publico_interno_formatado'] = (
    df_interno_agrupadas['publico_estimado_interno']
    .apply(formatar_valor)
)

graf_interno = (
    alt.Chart(df_interno_agrupadas)
    .mark_line(
        point=alt.OverlayMarkDef(
            color="#EF4136"
        ),
        color="#EF4136"
    )
    .encode(
        x=alt.X(
            "ano:N",
            axis=alt.Axis(
                labelAngle=45
            ), 
            title=None
        ),
        y=alt.Y(
            "publico_estimado_interno:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("publico_interno_formatado:N", title="Quantidade")
        ]
    )
    .properties(
        height=200,
        title="Público Estimado Interno por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_externo = df_filtrado[['id_projeto', 'publico_estimado_externo', 'data_inicio']]
df_externo = df_externo.drop_duplicates(subset='id_projeto')


df_externo['publico_estimado_externo'] = df_externo['publico_estimado_externo'].fillna(0).astype(int)
df_externo['ano'] = df_externo['data_inicio'].astype(str).str[:4]

df_externo_agrupadas = (
    df_externo.groupby('ano')['publico_estimado_externo']
    .sum()
    .reset_index()
)

df_externo_agrupadas['publico_externo_formatado'] = (
    df_externo_agrupadas['publico_estimado_externo']
    .apply(formatar_valor)
)

graf_externo = (
    alt.Chart(df_externo_agrupadas)
    .mark_line(
        point=alt.OverlayMarkDef(
            color="#067722"
        ),
        color="#067722"
    )
    .encode(
        x=alt.X(
            "ano:N",
            axis=alt.Axis(
                labelAngle=45
            ), 
            title=None
        ),
        y=alt.Y(
            "publico_estimado_externo:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("publico_externo_formatado:N", title="Quantidade")
        ]
    )
    .properties(
        height=200,
        title="Público Estimado Externo por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_atendido = df_filtrado[['id_projeto', 'publico_atendido', 'data_inicio']]
df_atendido = df_atendido.drop_duplicates(subset='id_projeto')


df_atendido['publico_atendido'] = df_atendido['publico_atendido'].fillna(0).astype(int)
df_atendido['ano'] = df_atendido['data_inicio'].astype(str).str[:4]

df_atendido_agrupadas = (
    df_atendido.groupby('ano')['publico_atendido']
    .sum()
    .reset_index()
)

df_atendido_agrupadas['publico_atendido_formatado'] = (
    df_atendido_agrupadas['publico_atendido']
    .apply(formatar_valor)
)

graf_atendido = (
    alt.Chart(df_atendido_agrupadas)
    .mark_line(
        point=alt.OverlayMarkDef(
            color="#EF4136"
        ),
        color="#EF4136"
    )
    .encode(
        x=alt.X(
            "ano:N",
            axis=alt.Axis(
                labelAngle=45
            ), 
            title=None
        ),
        y=alt.Y(
            "publico_atendido:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("publico_atendido_formatado:N", title="Quantidade")
        ]
    )
    .properties(
        height=200,
        title="Público Atendido por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

components = Components()
col_1, col_2 = st.columns((0.2, 0.8))

with col_1:
    with st.container(height=240):
        components.metric_card(
            "Público Estimado Interno", 
            publico_interno['publico_estimado_interno'], 
            "", 
            "#424242"
        )

    with st.container(height=240):
        components.metric_card(
            "Público Estimado Externo", 
            publico_externo['publico_estimado_externo'], 
            "", 
            "#424242"
        )

    with st.container(height=240):
        components.metric_card(
            "Público Atendido", 
            publico_atendido['publico_atendido'], 
            "", 
            "#424242"
        )

with col_2:
    with st.container(height=240):
        st.altair_chart(graf_interno, use_container_width=True)

    with st.container(height=240):
        st.altair_chart(graf_externo, use_container_width=True)

    with st.container(height=240):
        st.altair_chart(graf_atendido, use_container_width=True)