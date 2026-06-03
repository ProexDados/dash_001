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
        st.title("UNIDADES DE ENSINO")

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
    
    # ---------- TÍTULO ---------
    df_filtrado = filtros.filtro_titulo(df_participantes, "titulo", df_filtrado)

    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_projeto", df_filtrado)

    # -------- ID PROJETO -------
    df_filtrado = filtros.filtro_id_projeto(df_participantes, "id_projeto", df_filtrado)

    # -------- COORDENADOR ------
    df_filtrado = filtros.filtro_coordenador(df_participantes, "coordenador", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_participantes, "centro", df_filtrado)

# ------------------------------------------------------------------------------

df_acao_centro = df_filtrado[["id_projeto", "centro", "data_inicio"]]
df_acao_centro = df_acao_centro.drop_duplicates(subset="id_projeto")

df_acao_centro = df_acao_centro.groupby(["centro"], as_index=False)["data_inicio"].count()

altura_linha = 35

altura_grafico = len(df_acao_centro) * altura_linha

graf_acao_centro = (
    alt.Chart(df_acao_centro)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "centro:N",
            sort="-x",
            title=None
        ),

        x=alt.X(
            "data_inicio:Q",
            title=None
        ),

        tooltip=[
            alt.Tooltip(
                "centro:N",
                title="Centro"
            ),

            alt.Tooltip(
                "data_inicio:N",
                title="Quantidade"
            )
        ]
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_acao_centro.mark_text(
    align="left",
    dx=5
).encode(
    text=alt.Text(
        "data_inicio:N"
    )
)

graf_barra_acao_centro = (
    (graf_acao_centro + texto)
    .properties(
        height=335,
        title="Ações por Centro"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_coordenador_centro = df_filtrado[
    [
        'centro', 
        'coordenador'
    ]
]

df_coordenador_centro = df_coordenador_centro.drop_duplicates(subset="coordenador").dropna()

df_coordenador_centro_agrupado = (
    df_coordenador_centro.groupby(
        [
            'centro'
        ]
    )['coordenador']
    .count()
    .reset_index()
)

total = df_coordenador_centro_agrupado['coordenador'].sum()

df_coordenador_centro_agrupado['percentual'] = (
    df_coordenador_centro_agrupado['coordenador'] / total
)

graf_coordenador_centro = (
    alt.Chart(df_coordenador_centro_agrupado)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "centro:N",
            sort="-x",
            title="Centro"
        ),
        x=alt.X(
            "percentual:Q",
            axis=alt.Axis(
                format=".2%", 
                labelAngle=45
            ),
            title=None

        ),
        tooltip=[
            alt.Tooltip("centro:N", title="Centro"),
            alt.Tooltip("percentual:Q", title="Percentual", format=".2%"),
            alt.Tooltip("coordenador:Q", title="Quantidade")
        ]
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_coordenador_centro.mark_text(
    align="left",
    dx=5  # deslocamento à direita
).encode(
    text=alt.Text(
        "percentual:Q",
        format=".2%"
    )
)

graf_final = (
    (graf_coordenador_centro + texto)
    .properties(
        height=335,
        title="Percentual de Coordenador por Centro"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_lista = df_filtrado[
    [
        "titulo", 
        "coordenador", 
        "orcamento_consolidado_fundo", 
        "data_inicio",
        "unidade_execucao",
        "id_projeto",
        "linha_pesquisa_area_tematica"
    ]
]

df_lista["data_inicio"] = pd.to_datetime(
    df_lista["data_inicio"],
    errors="coerce",
    format="%Y-%m-%d"
).dt.strftime("%d/%m/%Y")

# df_lista["data_inicio"] = df_lista["data_inicio"].dt.year

df_lista = df_lista.rename(
    columns={
        "titulo": "Título do Projeto",
        "coordenador": "Coordenador",
        "orcamento_consolidado_fundo": "Orçamento Consolidado",
        "data_inicio": "Data de Início",
        "unidade_execucao": "Unidade Execução",
        "id_projeto": "ID Projeto",
        "linha_pesquisa_area_tematica": "Área Temática"
    }
)

df_lista = df_lista.drop_duplicates().dropna()

# ------------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns((0.5, 0.5))

    with col_1:
        with st.container(height=367):
            st.altair_chart(graf_barra_acao_centro, use_container_width=True)

    with col_2:
        with st.container(height=367):
            st.altair_chart(graf_final, use_container_width=True)

with st.container(height=368):
    st.dataframe(df_lista, hide_index=True, height=335)