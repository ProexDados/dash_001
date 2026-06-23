import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.titulos import Titulo
from components.components import Components
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.tabelas import Tabelas
from components.graf_tematica import Graficos


# ---------- OBJETOS ----------

config     = Configuracoes()
titulo     = Titulo()
file       = Files()
filtros    = Filtros()
formatacao = Formatacao()
tabela     = Tabelas()
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

df_participantes = file.participantes()

df_sem_ano = df_participantes.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ---------- CENTRO ---------
    df_sem_ano = filtros.filtro_centro(df_participantes, "centro", df_sem_ano)
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_projeto", df_sem_ano, "Ano da Ação")

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

# ======================================================================================
df_area_tematica = (
    df_filtrado[["id_projeto", "linha_pesquisa_area_tematica"]]
)

# Remove vazios/NaN
df_filtered = (
    df_area_tematica[
        df_area_tematica["linha_pesquisa_area_tematica"].notna() & 
        (df_area_tematica["linha_pesquisa_area_tematica"] != "")
    ]
    .drop_duplicates(subset="id_projeto")
)

total_projetos = len(df_filtered)

ranking = (
    df_filtered["linha_pesquisa_area_tematica"]
    .value_counts()
    .reset_index()
)

ranking.columns = ["Linha Temática", "Frequência"]
ranking["Percentual (%)"] = (
    ranking["Frequência"] / total_projetos * 100
).round(2)

top_1 = ranking.iloc[0]

tema_mais_frequente = top_1["Linha Temática"]
freq_mais_frequente = formatacao.formatar_valor_integer(top_1["Frequência"])
perc_mais_frequente = formatacao.formatar_valor_float(top_1["Percentual (%)"])

# ======================================================================================


# ---------- GRÁFICOS ---------

# ações por área temática
fig_radar = graficos.acoes_area(df_filtrado)

# área temática por centro
graf_tematica_centro = graficos.area_centro(df_filtrado)
# graf_tematica_centro_3d = graficos.area_centro_3d(df_filtrado)

# tematica
graf_tematica_anual = graficos.acoes_tematica(df_sem_ano)

# total ações por área temática e atividade
graf_tematica = graficos.area_atividade(df_filtrado)

# --------- DASHBOARD ---------

col_1, col_2 = st.columns(2)

with col_1:
    with st.container():
        col_1a, col_1b = st.columns((4, 6))

        with col_1a:
            with st.container(height=360):
                components.metric_card(
                    label="Áreas Temáticas", 
                    value=areas_tematicas['linha_pesquisa_area_tematica'], 
                    delta="",
                    bg_color="#424242"
                )
            
                st.markdown("<br>", unsafe_allow_html=True)

                components.metric_card(
                    label="Área Temática mais frequente", 
                    value=tema_mais_frequente, 
                    delta=f"{freq_mais_frequente} projetos ({perc_mais_frequente}%)",
                    bg_color="#424242",
                    font_size="24px"
                )

        with col_1b:
            with st.container(height=360):
                st.plotly_chart(fig_radar, use_container_width=True, config={"staticPlot": False})

    with st.container(height=400):
        st.altair_chart(graf_tematica_anual, use_container_width=True)

with col_2:
    with st.container(height=360):
        st.altair_chart(graf_tematica_centro, use_container_width=True)

    with st.container(height=400):
        st.altair_chart(graf_tematica, use_container_width=True)

# st.plotly_chart(
#     graf_tematica_centro_3d,
#     use_container_width=True
# )