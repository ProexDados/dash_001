import streamlit as st
from services.get_files import Files
import pandas as pd
from components.components import Components
from components.filtros import Filtros
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
        st.title("PARTICIPANTES")

# -------- OBTEM DADOS --------
file = Files()
filtros = Filtros()

df_projeto = file.projeto()
df_membro = file.membro_projeto()

df_projeto = df_projeto[
    [
        "id_projeto", 
        "ano_projeto", 
        "centro", 
        "total_discentes_envolvidos",
        "data_inicio",
        "bolsas_concedidas",
        "linha_pesquisa_area_tematica",
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
media_discentes = df_filtrado['total_discentes_envolvidos'].fillna(0).astype(int).mean()

total_acoes = len(df_filtrado[['id_projeto']].drop_duplicates())

# ------------------------------------------------------------------------------
df_extensionistas = df_filtrado[
    [
        'id_projeto_datageracao', 
        'id_pessoa_membro_datageracao', 
        'categoria_membro', 
        'centro'
    ]
]

df_extensionistas = df_extensionistas.drop_duplicates().dropna()

df_extensionistas_agrupado = (
    df_extensionistas.groupby(
        [
            'centro'
        ]
    )['categoria_membro']
    .count()
    .reset_index()
)

total = df_extensionistas_agrupado['categoria_membro'].sum()

df_extensionistas_agrupado['percentual'] = (
    df_extensionistas_agrupado['categoria_membro'] / total
)

graf_extensionistas = (
    alt.Chart(df_extensionistas_agrupado)
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
            alt.Tooltip("categoria_membro:Q", title="Quantidade")
        ]
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_extensionistas.mark_text(
    align="left",
    dx=5  # deslocamento à direita
).encode(
    text=alt.Text(
        "percentual:Q",
        format=".2%"
    )
)

graf_final = (
    (graf_extensionistas + texto)
    .properties(
        height=400,
        title="Taxa de extensionistas por centro"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------
df_bolsas = df_filtrado[['id_projeto', 'data_inicio', 'bolsas_concedidas']]
df_bolsas = df_bolsas.drop_duplicates(subset='id_projeto')
df_bolsas['bolsas_concedidas'] = df_bolsas['bolsas_concedidas'].fillna(0)

df_bolsas['ano'] = df_bolsas['data_inicio'].astype(str).str[:4]
df_bolsas['bolsas_concedidas'] = df_bolsas['bolsas_concedidas'].astype(int)

df_bolsas_agrupadas = (
    df_bolsas.groupby('ano')['bolsas_concedidas']
    .sum()
    .reset_index()
)

graf_bolsas = (
    alt.Chart(df_bolsas_agrupadas)
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
            "bolsas_concedidas:Q", 
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano:N", title="Ano"),
            alt.Tooltip("bolsas_concedidas:Q", title="Quantidade")
        ]
    )
    .properties(
        height=245,
        title="Total de bolsas concedidas por ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------
df_extensionistas_tematico = df_filtrado[
    [
        'id_projeto_datageracao', 
        'id_pessoa_membro_datageracao', 
        'categoria_membro', 
        'linha_pesquisa_area_tematica'
    ]
]

df_extensionistas_tematico = df_extensionistas_tematico.drop_duplicates().dropna()

df_extensionistas_tematico_agrupado = (
    df_extensionistas_tematico.groupby(
        [
            'linha_pesquisa_area_tematica'
        ]
    )['categoria_membro']
    .count()
    .reset_index()
)

total = df_extensionistas_tematico_agrupado['categoria_membro'].sum()

df_extensionistas_tematico_agrupado['percentual'] = (
    df_extensionistas_tematico_agrupado['categoria_membro'] / total
)

graf_extensionistas_tematica = (
    alt.Chart(df_extensionistas_tematico_agrupado)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "linha_pesquisa_area_tematica:N",
            sort="-x",
            title=None
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
            alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
            alt.Tooltip("percentual:Q", title="Percentual", format=".2%"),
            alt.Tooltip("categoria_membro:Q", title="Quantidade")
        ]
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_extensionistas_tematica.mark_text(
    align="left",
    dx=5  # deslocamento à direita
).encode(
    text=alt.Text(
        "percentual:Q",
        format=".2%"
    )
)

graf_final_tematica = (
    (graf_extensionistas_tematica + texto)
    .properties(
        height=245,
        title="Taxa de extensionistas por área temática"
    )
    .configure_title(
        fontSize=20
    )
)


# --------- DASHBOARD ---------
st.markdown("<br>", unsafe_allow_html=True)

components = Components()

with st.container():
    col_1, col_2 = st.columns((2, 8))

    with col_1:
        with st.container(height=455):
            components.metric_card("Média de discentes envolvidos em ações", f"{media_discentes:.2f}".replace(".", ","), "", "#424242")
            st.markdown("<br>", unsafe_allow_html=True)
            components.metric_card("Total de ações", total_acoes, "", "#424242")

    with col_2:
        with st.container(height=455):
            st.altair_chart(graf_final, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns((2,2))

    with col_1:
        with st.container(height=280):
            st.altair_chart(graf_bolsas, use_container_width=True)

    with col_2:
        with st.container(height=280):
            st.altair_chart(graf_final_tematica, use_container_width=True)