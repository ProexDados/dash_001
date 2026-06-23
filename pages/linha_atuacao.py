import streamlit as st
from dash.config.settings import Configuracoes
from services.get_files import Files
from dash.components.titulos import Titulo
from dash.components.components import Components
from dash.components.filtros import Filtros
from utils.formatacao import Formatacao
from dash.components.tabelas import Tabelas
from dash.components.graf_linha_atuacao import Graficos


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

titulo.titulo("LINHA DE ATUAÇÃO", tema)

# -------- OBTEM DADOS --------

df_participantes = file.participantes()

df_filtrado = df_participantes.copy()

# ---------- FILTROS ----------

with st.sidebar:
    st.title("Filtros")
    
    # ----------- ANO -----------
    df_filtrado = filtros.filtro_ano(df_participantes, "ano_projeto", df_filtrado, "Ano da Ação")

    # ---------- CENTRO ---------
    df_filtrado = filtros.filtro_centro(df_participantes, "centro", df_filtrado)

# ----------- CARDS -----------

df_linha_atuacao = df_filtrado[['linha_atuacao']]
df_linha_atuacao = df_linha_atuacao['linha_atuacao'].dropna().unique()

total_linha_atuacao = len(df_linha_atuacao)

# =============================================================================

df_linha_atuacao = (
    df_filtrado[["id_projeto", "linha_atuacao"]]
)

# Remove vazios/NaN
df_filtered = (
    df_linha_atuacao[
        df_linha_atuacao["linha_atuacao"].notna() & 
        (df_linha_atuacao["linha_atuacao"] != "") &
        (df_linha_atuacao["linha_atuacao"] != "Não Informada")
    ]
    .drop_duplicates(subset="id_projeto")
)

total_projetos = len(df_filtered)

ranking = (
    df_filtered["linha_atuacao"]
    .value_counts()
    .reset_index()
)

ranking.columns = ["Linha Atuação", "Frequência"]
ranking["Percentual (%)"] = (
    ranking["Frequência"] / total_projetos * 100
).round(2)

top_1 = ranking.iloc[0]

tema_mais_frequente = top_1["Linha Atuação"]
freq_mais_frequente = formatacao.formatar_valor_integer(top_1["Frequência"])
perc_mais_frequente = formatacao.formatar_valor_float(top_1["Percentual (%)"])

# ---------- GRÁFICOS ---------

graf_atuacao_categoria = graficos.linha_atuacao_categoria(df_filtrado)

graf_acoes_atuacao = graficos.acoes_atuacao(df_filtrado)

graf_atuacoes_centros = graficos.atuacoes_centros(df_filtrado)

graf_conhecimento_atuacao = graficos.linha_atuacao_area_conhecimento(df_filtrado)

# --------- DASHBOARD ---------

col_1a, col_2a = st.columns((6, 4))

with col_1a:
    col_1aa, col_1ab = st.columns((4, 6))

    with col_1aa:
        with st.container(height=360):
            components.metric_card(
                label="Linha de Atuação", 
                value=total_linha_atuacao, 
                delta="", 
                bg_color="#424242"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            components.metric_card(
                label="Linha de Atuação mais frequente", 
                value=tema_mais_frequente, 
                delta=f"{freq_mais_frequente} projetos ({perc_mais_frequente}%)",
                bg_color="#424242",
                font_size="24px"
            )

    with col_1ab:
        with st.container(height=360):
            st.altair_chart(graf_conhecimento_atuacao)

    # col_1ac, col_1ad = st.columns(2)

    # with col_1ac:

    # with col_1ad:
    with st.container(height=400):
        st.altair_chart(graf_atuacoes_centros)

with col_2a:
    with st.container(height=500):
        st.altair_chart(graf_acoes_atuacao)

    with st.container(height=260):
        st.altair_chart(graf_atuacao_categoria)
    

