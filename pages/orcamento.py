import streamlit as st
from config.settings import Configuracoes
from components.titulos import Titulo
from services.get_files import Files
from components.filtros import Filtros
from components.graficos import Graficos
from components.components import Components


# ---------- OBJETOS ----------

config     = Configuracoes()
titulo     = Titulo()
file       = Files()
filtros    = Filtros()
graficos   = Graficos()
components = Components()

# ------------ TEMA -----------

config.tema_escuro()

# ----------- LAYOUT ----------

config.layout()

config.remove_espaco()

tema = config.tema()

# ----------- TÍTULO ----------

titulo.titulo("ORÇAMENTO", tema)

# -------- OBTEM DADOS --------

df_projeto = file.projeto()

df_filtrado = df_projeto.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_projeto, "ano_projeto", df_filtrado)

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_projeto, "centro", df_filtrado)

# ----------- CARDS -----------

areas_tematicas = (
    df_filtrado[
        [
            'centro'
        ]
    ]
    .drop_duplicates()
    .count()
)

# ---------- GRÁFICOS ---------

# orçamento por ano
graf_final_orcamento = graficos.orcamento_ano(df_filtrado)

# orçamento anual por centro
graf_centro = graficos.orcamento_centro(df_filtrado)

# orçamento por área temática
fig_radar = graficos.orcamento_area(df_filtrado)

# orçamento por linha de atuação
graf_barra_orcamento = graficos.orcamento_atuacao(df_filtrado)

# projetos com e sem financiamento
graf_financiamento = graficos.projetos_financiados(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns((0.33, 0.33, 0.34))

with col_1:
    # card
    with st.container(height=235):
        components.metric_card("Unidades Gestoras", areas_tematicas['centro'], "", "#424242")

    # orçamento por ano
    with st.container(height=500):
        st.altair_chart(graf_final_orcamento, use_container_width=True)

with col_2:
    # orçamento anual por centro
    with st.container(height=355):
        st.altair_chart(graf_centro, use_container_width=True)

    # orçamento por área temática
    with st.container(height=380):
        st.plotly_chart(fig_radar, use_container_width=True, config={"staticPlot": False})

with col_3:
    # orçament opor linha de atuação
    with st.container(height=355):
        st.altair_chart(graf_barra_orcamento, use_container_width=True)

    # projetos com e sem financiamento
    with st.container(height=380):
        st.altair_chart(graf_financiamento, use_container_width=True)
        