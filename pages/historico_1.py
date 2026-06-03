import streamlit as st
import pandas as pd
from services.get_files import Files
from components.components import Components
from components.filtros import Filtros
import altair as alt
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder
)


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

    # -------- SITUAÇÃO --------
    df_filtrado = filtros.filtro_situacao(df_projeto, "situacao_projeto", df_filtrado)


df_filtrado = df_filtrado.sort_values(by='ano_projeto', ascending=False)

total_acoes = len(df_filtrado)

# -----------------------------
df_titulos = df_filtrado[['ano_projeto', 'titulo']]

df_titulos = df_titulos.sort_values("ano_projeto")

df_titulos = df_titulos.rename(
    columns={
        "ano_projeto": "Ano Projeto", 
        "titulo": "Título"
    }
)

gb = GridOptionsBuilder.from_dataframe(df_titulos)

gb.configure_column(
    "Ano Projeto",
    width=50
)

gb.configure_column(
    "Título",
    width=500
)

grid_options = gb.build()
        
# ---------- GRÁFICOS ---------
# Agrupa os dados
dados = df_filtrado.groupby(["ano_projeto", "situacao_projeto"], as_index=False)["id_projeto"].count()

# ações
graf_acoes = (
    alt.Chart(dados)
    .mark_rect()
    .encode(
        x=alt.X(
            "ano_projeto:O",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "situacao_projeto:N",
            title=None
        ),
        color=alt.Color(
            "id_projeto:Q",
            title="Quantidade",
            scale=alt.Scale(scheme="reds")
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:O", title="Ano"),
            alt.Tooltip("situacao_projeto:N", title="Situação"),
            alt.Tooltip("id_projeto:Q", title="Quantidade")
        ]
    )
    .properties(
        height=465,
        title="Ações pela situação do projeto"
    )
    .configure_title(
        fontSize=20
    )
)

# categorias
dados_categoria = df_filtrado.groupby(["categoria"], as_index=False)["numero_projeto"].count()

graf_categoria = (
    alt.Chart(dados_categoria)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "numero_projeto:Q",
            title=None
        ),
        x=alt.X(
            "categoria:N",
            sort="-y",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        tooltip=[
            alt.Tooltip("categoria:N", title="Categoria"),
            alt.Tooltip("numero_projeto:Q", title="Quantidade")
        ]
    )
)

texto = graf_categoria.mark_text(
    align="center", dy=-5
).encode(
    text=alt.Text(
        "numero_projeto:Q"
    )
)

graf_final_categoria = (
    (graf_categoria + texto)
    .properties(
        height=465,
        title="Quantidade de ações por tipos de atividades de extensão"
    )
    .configure_title(
        fontSize=20
    )
)

# --------- DASHBOARD ---------
st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2 = st.columns((2, 8))

    with col_1:
        components = Components()
        with st.container(height=235):
            components.metric_card("Total Ações", total_acoes, "", "#424242")

    with col_2:
        with st.container(height=235):
            grid_response = AgGrid(
                df_titulos,
                gridOptions=grid_options,
                height=195,
                width="100%",
                fit_columns_on_grid_load=False,
                theme="streamlit",  # alpine | balham | material
                enable_enterprise_modules=False
            )

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        with st.container(height=500):
            st.altair_chart(graf_acoes, use_container_width=True)

    with col_2:
        with st.container(height=500):
            st.altair_chart(graf_final_categoria, use_container_width=True)
