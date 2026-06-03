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
        st.title("INICIATIVAS POR CENTRO")

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
        "coordenador",
        "bolsas_concedidas",
        "linha_pesquisa_area_tematica",
        "linha_atuacao",
        "tipo_projeto",
        "orcamento_consolidado_fundo",
        "palavras_chave",
        "unidade_execucao"
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

# ------------------------------------------------------------------------------

df_acao_coordenador = df_filtrado[["id_projeto", "coordenador"]]
df_acao_coordenador = df_acao_coordenador.drop_duplicates(subset="id_projeto")

df_acao_coordenador = df_acao_coordenador.groupby(["coordenador"], as_index=False)["id_projeto"].count()

altura_linha = 25

altura_grafico = len(df_acao_coordenador) * altura_linha

graf_acao_coordenador = (
    alt.Chart(df_acao_coordenador)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "coordenador:N",
            sort="-x",
            title=None
        ),

        x=alt.X(
            "id_projeto:Q",
            title=None
        ),

        tooltip=[
            alt.Tooltip(
                "coordenador:N",
                title="Coordenador"
            ),

            alt.Tooltip(
                "id_projeto:N",
                title="Quantidade"
            )
        ]
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_acao_coordenador.mark_text(
    align="left",
    dx=5
).encode(
    text=alt.Text(
        "id_projeto:N"
    )
)

graf_barra_acao_coordenador = (
    (graf_acao_coordenador + texto)
    .properties(
        height=altura_grafico,
        title="Ações por Coordenador"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_centro = df_filtrado[['id_projeto', 'centro']]
df_centro = df_centro.drop_duplicates(subset=['id_projeto'])

df_acoes_centro = (
    df_centro
    .groupby(df_centro["centro"])
    ["id_projeto"]
    .count()
    .reset_index()
)

graf_acoes_centro = (
    alt.Chart(df_acoes_centro)
    .mark_bar(color="#EF4136")
    .encode(
        x=alt.X(
            "centro:N",
            sort="-y",  # ordena pela medida do eixo Y em ordem decrescente
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "id_projeto:Q",
            title=None
        ),
        tooltip=[
            alt.Tooltip("centro:N", title="Centro"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ],
        order=alt.Order("id_projeto:Q")
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_acoes_centro.mark_text(
    align="center", 
    dy=-5
).encode(
    text=alt.Text(
        "id_projeto:Q"
    )
)

graf_final_acoes = (
    (graf_acoes_centro + texto)
    .properties(
        height=335,
        title="Total Ações por Centro"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_participantes = df_filtrado[['id_projeto', 'id_pessoa_membro_datageracao', 'data_inicio']]

df_participantes['ano'] = df_participantes['data_inicio'].astype(str).str[:4]

df_participantes_agrupadas = (
    df_participantes.groupby('ano')['id_pessoa_membro_datageracao']
    .count()
    .reset_index()
)

graf_participantes = (
    alt.Chart(df_participantes_agrupadas)
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
            "id_pessoa_membro_datageracao:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("id_pessoa_membro_datageracao:Q", title="Quantidade")
        ]
    )
    .properties(
        height=335,
        title="Total Participantes por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_acoes = df_filtrado[['id_projeto', 'data_inicio']]
df_acoes = df_acoes.drop_duplicates(subset='id_projeto')

df_acoes['ano'] = df_acoes['data_inicio'].astype(str).str[:4]

df_acoes_agrupadas = (
    df_acoes.groupby('ano')['id_projeto']
    .count()
    .reset_index()
)

graf_acoes = (
    alt.Chart(df_acoes_agrupadas)
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
            "id_projeto:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=335,
        title="Ações por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_discentes = df_filtrado[['categoria_membro', 'data_inicio']]
df_discentes = df_discentes[df_discentes['categoria_membro'] == 'DISCENTE']

df_discentes['ano'] = df_discentes['data_inicio'].astype(str).str[:4]

df_discentes_agrupadas = (
    df_discentes.groupby('ano')['categoria_membro']
    .count()
    .reset_index()
)

graf_discentes = (
    alt.Chart(df_discentes_agrupadas)
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
            "categoria_membro:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("categoria_membro:Q", title="Quantidade")
        ]
    )
    .properties(
        height=335,
        title="Total Discentes por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns((0.3, 0.3, 0.3))

with col_1:
    with st.container(height=750):
        st.altair_chart(graf_barra_acao_coordenador, use_container_width=True)

with col_2:
    with st.container(height=367):
        st.altair_chart(graf_final_acoes, use_container_width=True)

    with st.container(height=368):
        st.altair_chart(graf_participantes, use_container_width=True)

with col_3:

    with st.container(height=367):
        st.altair_chart(graf_acoes, use_container_width=True)

    with st.container(height=368):
        st.altair_chart(graf_discentes, use_container_width=True)