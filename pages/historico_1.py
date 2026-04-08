import streamlit as st
import pandas as pd
from services.get_files import Files
from components.components import Components
import altair as alt


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

df_filtrado = df_filtrado[(df_filtrado['ano_projeto'] > 2016) & (df_filtrado['ano_projeto'] < 2030)]

# ---------- FILTROS ----------
with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    if "filtro_ano" not in st.session_state:
        st.session_state.filtro_ano = None

    ano_filtro = st.multiselect(
        "Filtrar por Ano:",
        sorted(df_projeto["ano_projeto"].unique()),
        default=st.session_state.filtro_ano,
    )
    
    if len(ano_filtro) > 0:
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

df_filtrado = df_filtrado.sort_values(by='ano_projeto', ascending=False)

total_acoes = len(df_filtrado)

# --------- DASHBOARD ---------
st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns((2, 8))

    with col_1:
        components = Components()
        components.metric_card("Total Ações", total_acoes, "", "#424242")

    with col_2:
        st.dataframe(df_filtrado[['ano_projeto', 'titulo']], hide_index=True, height=200)

# ---------- GRÁFICOS ---------
# Agrupa os dados
dados = df_filtrado.groupby(["ano_projeto", "situacao_projeto"], as_index=False)["id_projeto"].count()
dados_categoria = df_filtrado.groupby(["categoria"], as_index=False)["numero_projeto"].count()

# ações
graf_acoes = (
    alt.Chart(dados)
    .mark_rect()
    .encode(
        x=alt.X(
            "ano_projeto:O",
            title="Ano"
        ),
        y=alt.Y(
            "situacao_projeto:N",
            title="Status"
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="purples")
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:O"),
            alt.Tooltip("situacao_projeto:N"),
            alt.Tooltip("id_projeto:Q")
        ]
    )
    .properties(
        height=400,
        title="Ações pela situação do projeto"
    )
)

# categorias
graf_categoria = (
    alt.Chart(dados_categoria)
    .mark_bar()
    .encode(
        y=alt.Y(
            "numero_projeto:Q",
            title="Quantidade"
        ),
        x=alt.X(
            "categoria:N",
            sort="-y",
            title="Categoria"
        ),
        tooltip=[
            alt.Tooltip("categoria:N", title="Categoria"),
            alt.Tooltip("numero_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=400,
        title="Quantidade de ações por tipos de atividades de extensão"
    )
)

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns(2)

# Exibe no dashboard
    with col_1:
        st.altair_chart(graf_acoes, use_container_width=True, height=500)

    with col_2:
        st.altair_chart(graf_categoria, use_container_width=True, height=500)
