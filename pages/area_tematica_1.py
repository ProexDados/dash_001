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

titulo.titulo("ÁREA TEMÁTICA", tema)

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
            'linha_pesquisa_area_tematica'
        ]
    ]
    .drop_duplicates()
    .count()
)

linha_atuacao = (
    df_filtrado[
        [
            'linha_atuacao'
        ]
    ]
    .drop_duplicates()
    .count()
)

# ---------- GRÁFICOS ---------

# ações por área temática
fig_radar = graficos.acoes_area(df_filtrado)

# total ações por área temática e atividade
graf_tematica = graficos.area_atividade(df_filtrado)

# total ações por abrangência e atividade
graf_abrangencia = graficos.categoria_abrangencia(df_filtrado)

# --------- DASHBOARD ---------

st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2 = st.columns((2, 2))

with col_1:
    # cards
    with st.container(height=230):
        col_1a, col_2a = st.columns((2, 2))

        with col_1a:
            components.metric_card("Áreas Temáticas", areas_tematicas['linha_pesquisa_area_tematica'], "", "#424242")

        with col_2a:
            components.metric_card("Linhas de Atuação", linha_atuacao['linha_atuacao'], "", "#424242")

    # ações por área temática
    with st.container(height=505):
        st.plotly_chart(fig_radar, use_container_width=True, config={"staticPlot": False})

with col_2:
    # total ações por área temática e atividade
    with st.container(height=367):
        st.altair_chart(graf_tematica, use_container_width=True)

    # total ações por abrangência e atividade
    with st.container(height=368):
        st.altair_chart(graf_abrangencia, use_container_width=True)
        