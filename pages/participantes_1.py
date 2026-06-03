import streamlit as st
from services.get_files import Files
from components.filtros import Filtros
import pandas as pd
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
        "total_discentes_envolvidos"
    ]
]

df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)

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

df_lista = df_lista.drop_duplicates().dropna()

# ------------------------------------------------------------------------------
df_bolsa = df_filtrado[['tipo_bolsa', 'categoria_bolsa']]

qtd_bolsa = (
    df_bolsa[df_bolsa['tipo_bolsa'].notna()]
    .groupby('tipo_bolsa', as_index=False)['categoria_bolsa']
    .count()
)

total = qtd_bolsa['categoria_bolsa'].sum()
qtd_bolsa['percentual'] = (qtd_bolsa['categoria_bolsa'] / total)

base = alt.Chart(qtd_bolsa)

# Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
pizza = base.mark_arc(innerRadius=70).encode(
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
    radius=100,  # Distância do centro. Aumente para afastar do meio.
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
    width=315,
    height=315,
    title="Tipo de bolsa"
).configure_view(
    strokeWidth=0  # Remove a borda externa do gráfico
).configure_title(
    fontSize=20
)

# ------------------------------------------------------------------------------
df_ano = df_filtrado[['id_projeto', 'ano_projeto', 'total_discentes_envolvidos']]
df_ano = df_ano.drop_duplicates(subset=['id_projeto'])
df_ano = df_ano.drop_duplicates()
df_ano["total_discentes_envolvidos"] = (
    df_ano["total_discentes_envolvidos"]
    .fillna(0)
    .astype(int)
)


df_discentes_ano = df_ano.groupby(["ano_projeto"], as_index=False)["total_discentes_envolvidos"].sum()

graf_discente_ano = (
    alt.Chart(df_discentes_ano)
    .mark_bar(color="#009553")
    .encode(
        x=alt.X(
            "ano_projeto:N",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "total_discentes_envolvidos:Q",
            title=None
        ),
        tooltip=[
            alt.Tooltip("ano_projeto:N", title="Ano"),
            alt.Tooltip("total_discentes_envolvidos:Q", title="Quantidade")
        ],
        order=alt.Order("ano_projeto:N")
    )
)

texto = graf_discente_ano.mark_text(
    align="center", dy=-5
).encode(
    text=alt.Text(
        "total_discentes_envolvidos:Q"
    )
)

graf_final_discente = (
    (graf_discente_ano + texto)
    .properties(
        height=315,
        title="Total de Discentes envolvidos por Ano"
    )
    .configure_title(
        fontSize=20
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
    radius=90,  # Distância do centro. Aumente para afastar do meio.
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
    width=315,
    height=315,
    title="Tipo de vínculo do extensionista"
).configure_view(
    strokeWidth=0  # Remove a borda externa do gráfico
).configure_title(
    fontSize=20
)

# ------------------------------------------------------------------------------
df_discentes_centro = df_filtrado[["centro", "total_discentes_envolvidos"]]
df_discentes_centro = df_discentes_centro.drop_duplicates()
df_discentes_centro["total_discentes_envolvidos"] = (
    df_discentes_centro["total_discentes_envolvidos"]
    .fillna(0)
    .astype(int)
)

df_discentes = df_discentes_centro.groupby(["centro"], as_index=False)["total_discentes_envolvidos"].sum()

graf_discente = (
    alt.Chart(df_discentes)
    .mark_bar(color="#EF4136")
    .encode(
        y=alt.Y(
            "centro:N",
            sort="-x",
            title=None
        ),
        x=alt.X(
            "total_discentes_envolvidos:Q",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        tooltip=[
            alt.Tooltip("centro:N", title="Categoria"),
            alt.Tooltip("total_discentes_envolvidos:Q", title="Quantidade")
        ]
    )
)

texto = graf_discente.mark_text(
    align="left",
    dx=5
).encode(
    text=alt.Text(
        "total_discentes_envolvidos:Q"
    )
)

graf_discente_centro = (
    (graf_discente + texto)
    .properties(
        height=350,
        title="Total de Discentes envolvidos por Centro"
    )
    .configure_title(
        fontSize=20
    )
)

# ---------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col_1, col_2, col_3 = st.columns(3)

    with col_1:
        with st.container(height=350):
            st.altair_chart(graf_bolsa, use_container_width=True)
    
    with col_2:
        with st.container(height=350):
            st.altair_chart(graf_final_discente, use_container_width=True)

    with col_3:
        with st.container(height=350):
            st.altair_chart(graf_membro, use_container_width=True)

with st.container():
    col_1, col_2 = st.columns(2)

    with col_1:
        with st.container(height=385):
            st.dataframe(df_lista, hide_index=True, height=350)

    with col_2:
        with st.container(height=385):
            st.altair_chart(graf_discente_centro, use_container_width=True)