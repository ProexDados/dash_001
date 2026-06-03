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
        "tipo_projeto",
        "orcamento_consolidado_fundo",
        "palavras_chave"
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



df_filtrado = df_participantes.copy()

# ---------- FILTROS ----------
with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_projeto", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_participantes, "centro", df_filtrado)

# ------------------------------------------------------------------------------

orcamento_tematica_atividade = df_filtrado[
    [
        'orcamento_consolidado_fundo',
        'categoria',
        'linha_pesquisa_area_tematica'
    ]
]

orcamento_tematica_atividade['orcamento_consolidado_fundo'] = (
    orcamento_tematica_atividade['orcamento_consolidado_fundo']
    .astype(float)
)

dados_tematica = (
    orcamento_tematica_atividade
    .groupby(['categoria', 'linha_pesquisa_area_tematica'])['orcamento_consolidado_fundo']
    .sum()
    .reset_index()
)

dados_tematica['orcamento_consolidado_fundo'] = np.where(dados_tematica['orcamento_consolidado_fundo'] == 0, None, dados_tematica['orcamento_consolidado_fundo'])
dados_tematica['orcamento_consolidado_fundo'] = dados_tematica["orcamento_consolidado_fundo"].astype(float)

dados_tematica = formatar_valor(dados_tematica)

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
            "orcamento_consolidado_fundo:Q",
            title="Valor",
            scale=alt.Scale(scheme="reds"),
            legend=alt.Legend(
                format="~s"
            )
        ),
        tooltip=[
            alt.Tooltip("categoria:N", title="Categoria"),
            alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
            alt.Tooltip("valor_formatado:N", title="Valor")
        ]
    )
    .properties(
        height=335,
        title="Orçamento por Área Temática e tipo de Atividade de Extensão"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------
df_atuacoes_acoes = df_filtrado[["linha_atuacao", "id_projeto"]]
df_atuacoes_acoes = df_atuacoes_acoes.drop_duplicates()

df_atuacoes = df_atuacoes_acoes.groupby(["linha_atuacao"], as_index=False)["id_projeto"].count()

graf_atuacoes = (
    alt.Chart(df_atuacoes)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "linha_atuacao:N",
            sort="-x",
            title=None
        ),
        x=alt.X(
            "id_projeto:Q",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        tooltip=[
            alt.Tooltip("linha_atuacao:N", title="Linha Atuação"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=715,
        title="Ações por Linha de Atuação"
    )
    .configure_title(
        fontSize=20
    )
)
# ------------------------------------------------------------------------------
texto = " ".join(df_filtrado["palavras_chave"].dropna().astype(str))

stopwords = STOPWORDS.union({
    "de", "da", "do", "em", "para", "com", "por", "na", "no", "das", "dos", "nos", "nas", "a", "o", "as", "os", "e", "es"
})

wordcloud = WordCloud(
    width=1200,
    height=500,
    background_color="white",
    stopwords=stopwords,
    colormap="viridis",
    max_words=100
).generate(texto)

fig, ax = plt.subplots(figsize=(14, 7))

ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

ax.set_title(
    "Palavras Chave",
    fontsize=20,
    pad=20,
    loc="left", 
    fontname="Arial"
)

# ------------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

col_1a, col_2a = st.columns((8, 8))

with col_1a:
    with st.container(height=367):
        st.altair_chart(graf_tematica, use_container_width=True)

    with st.container(height=368):
        st.pyplot(fig)

with col_2a:
    with st.container(height=750):
        st.altair_chart(graf_atuacoes, use_container_width=True)

