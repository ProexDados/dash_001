import streamlit as st
from services.get_files import Files
import pandas as pd
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
        st.title("PARTICIPANTES")

# -------- OBTEM DADOS --------
file = Files()
df_projeto = file.projeto()
df_membro = file.membro_projeto()

df_projeto = df_projeto[
    [
        "id_projeto", 
        "ano_projeto", 
        "centro", 
        "total_discentes_envolvidos"
    ]
]

df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])

df_membro["id_projeto"] = df_membro["id_projeto"].astype(int)

df_participantes = pd.merge(
    df_membro, 
    df_projeto, 
    on="id_projeto", 
    how="outer"
)

df_filtrado = df_participantes.copy()

# ---------- FILTROS ----------
with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    if "filtro_ano" not in st.session_state:
        st.session_state.filtro_ano = None

    ano_filtro = st.multiselect(
        "Filtrar por Ano:",
        sorted(df_participantes["ano_projeto"].dropna().astype(int).unique()),
        default=st.session_state.filtro_ano,
    )

    if len(ano_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["ano_projeto"].isin(ano_filtro)]

    # ---------- CENTRO ---------
    if "filtro_centro" not in st.session_state:
        st.session_state.filtro_centro = None

    centro_filtro = st.multiselect(
        "Filtrar por Centro:",
        sorted(df_participantes["centro"].dropna().unique()),
        default=st.session_state.filtro_centro
    )

    if len(centro_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["centro"].isin(centro_filtro)]

    # -------- CATEGORIA --------
    if "filtro_categoria_membro" not in st.session_state:
        st.session_state.filtro_categoria_membro = None

    categoria_filtro = st.multiselect(
        "Filtrar por categoria:",
        sorted(df_participantes["categoria_membro"].dropna().unique()),
        default=st.session_state.filtro_categoria_membro
    )

    if len(categoria_filtro) > 0:
        df_filtrado = df_filtrado[df_filtrado["categoria_membro"].isin(categoria_filtro)]

# ------------------------------------------------------------------------------
df_lista = df_filtrado[
    [
        "nome_membro", 
        "funcao_membro", 
        "data_inicio_membro", 
        "categoria_membro"
    ]
]

df_lista["data_inicio_membro"] = pd.to_datetime(
    df_lista["data_inicio_membro"],
    errors="coerce"
)

df_lista["data_inicio_membro"] = df_lista["data_inicio_membro"].dt.year

df_lista = df_lista.rename(
    columns={
        "nome_membro": "Nome membro",
        "funcao_membro": "Função membro",
        "data_inicio_membro": "Ano",
        "categoria_membro": "Categoria"
    }
)

# ------------------------------------------------------------------------------
df_bolsa = df_filtrado[['tipo_bolsa', 'categoria_bolsa']]

qtd_bolsa = (
    df_bolsa[df_bolsa['tipo_bolsa'].notna()]
    .groupby('tipo_bolsa', as_index=False)['categoria_bolsa']
    .count()
)
# qtd_bolsa = qtd_bolsa.rename(
#     columns={
#         'tipo_bolsa': 'tipo_bolsa', 
#         'categoria_bolsa': 'categoria_bolsa'
#     }
# )

total = qtd_bolsa['categoria_bolsa'].sum()
qtd_bolsa['percentual'] = (qtd_bolsa['categoria_bolsa'] / total)

base = alt.Chart(qtd_bolsa)

# Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
pizza = base.mark_arc(innerRadius=100).encode(
    # 'stack=True' garante que as fatias sejam empilhadas proporcionalmente
    theta=alt.Theta("percentual:Q", stack=True),
    color=alt.Color("tipo_bolsa:N", title="Tipo bolsa"),
    tooltip=[
        alt.Tooltip("tipo_bolsa:N", title="Tipo bolsa"),
        alt.Tooltip("categoria_bolsa:Q", title="Quantidade"),
        alt.Tooltip("percentual:Q", format=".2%", title="Porcentagem")
    ],
    order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
)

# Texto centralizado nas fatias
texto = base.mark_text(
    radius=135,  # Distância do centro. Aumente para afastar do meio.
    size=14, 
    fontWeight="bold",
    fill="black" # Ou "white" se a fatia for muito escura
).encode(
    # O theta DEVE ser idêntico ao da pizza para o alinhamento funcionar
    theta=alt.Theta("percentual:Q", stack=True),
    text=alt.Text("percentual:Q", format=".2%"), # format=".0f" remove casas decimais
    detail="tipo_bolsa:N",  # Garante que o texto se alinhe corretamente à fatia
    order=alt.Order("percentual:Q", sort="descending")  # Garantir que os textos sigam a mesma ordem
)

graf_bolsa = (pizza + texto).properties(
    width=400,
    height=400,
    title="Tipo de bolsa"
).configure_view(
    strokeWidth=0  # Remove a borda externa do gráfico
)

# ------------------------------------------------------------------------------
df_ano = df_filtrado[['id_projeto', 'ano_projeto', 'total_discentes_envolvidos']]
df_ano = df_ano.drop_duplicates(subset=['id_projeto'])

df_discentes_ano = df_ano.groupby(["ano_projeto"], as_index=False)["total_discentes_envolvidos"].sum()

graf_discente_ano = (
    alt.Chart(df_discentes_ano)
    .mark_bar()
    .encode(
        x=alt.X(
            "ano_projeto:N",
            title="Ano"
        ),
        y=alt.Y(
            "total_discentes_envolvidos:Q",
            title="Total"
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:N", title="Categoria"),
            alt.Tooltip("total_discentes_envolvidos:Q", title="Quantidade")
        ],
        order=alt.Order("ano_projeto:N")
    )
    .properties(
        height=400,
        title="Total de discentes envolvidos por ano"
    )
)

# ------------------------------------------------------------------------------
df_membros = df_filtrado[['categoria_membro', 'id_projeto']]
df_membros = df_membros.drop_duplicates()

qtd_membro = (
    df_membros
    .groupby('categoria_membro', as_index=False)['id_projeto']
    .count()
)

# qtd_membro = qtd_membro.rename(
#     columns={
#         'categoria_membro': 'categoria_membro', 
#         'id_projeto': 'id_projeto'
#     }
# )

total = qtd_membro['id_projeto'].sum()
qtd_membro['percentual'] = (qtd_membro['id_projeto'] / total)

base = alt.Chart(qtd_membro)

# Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
pizza = base.mark_arc().encode(
    # 'stack=True' garante que as fatias sejam empilhadas proporcionalmente
    theta=alt.Theta("percentual:Q", stack=True),
    color=alt.Color("categoria_membro:N", title="Tipo vínculo"),
    tooltip=[
        alt.Tooltip("categoria_membro:N", title="Tipo vínculo"),
        alt.Tooltip("id_projeto:Q", title="Quantidade"),
        alt.Tooltip("percentual:Q", format=".2%", title="Porcentagem")
    ],
    order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
)

# Texto centralizado nas fatias
texto = base.mark_text(
    radius=135,  # Distância do centro. Aumente para afastar do meio.
    size=14, 
    fontWeight="bold",
    fill="black" # Ou "white" se a fatia for muito escura
).encode(
    # O theta DEVE ser idêntico ao da pizza para o alinhamento funcionar
    theta=alt.Theta("percentual:Q", stack=True),
    text=alt.Text("percentual:Q", format=".2%"), # format=".0f" remove casas decimais
    detail="categoria_membro:N",  # Garante que o texto se alinhe corretamente à fatia
    order=alt.Order("percentual:Q", sort="descending")  # Garantir que os textos sigam a mesma ordem
)

graf_membro = (pizza + texto).properties(
    width=400,
    height=400,
    title="Tipo de vínculo do extensionista"
).configure_view(
    strokeWidth=0  # Remove a borda externa do gráfico
)

# ------------------------------------------------------------------------------
df_discentes = df_filtrado.groupby(["centro"], as_index=False)["total_discentes_envolvidos"].sum()

graf_discente = (
    alt.Chart(df_discentes)
    .mark_bar()
    .encode(
        y=alt.Y(
            "centro:N",
            title="Centro"
        ),
        x=alt.X(
            "total_discentes_envolvidos:Q",
            sort="-x",
            title="Total"
        ),
        tooltip=[
            alt.Tooltip("centro:N", title="Categoria"),
            alt.Tooltip("total_discentes_envolvidos:Q", title="Quantidade")
        ]
    )
    .properties(
        height=400,
        title="Taxa de discentes envolvidos por centro"
    )
)

with st.container():
    col_1, col_2, col_3 = st.columns(3)

    with col_1:
        st.altair_chart(graf_bolsa, use_container_width=True)
    
    with col_2:
        st.altair_chart(graf_discente_ano, use_container_width=True)

    with col_3:
        st.altair_chart(graf_membro, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        st.dataframe(df_lista, hide_index=True)

    with col_2:
        st.altair_chart(graf_discente, use_container_width=True)