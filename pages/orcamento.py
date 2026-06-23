import streamlit as st
from config.settings import Configuracoes
from services.get_files import Files
from components.titulos import Titulo
from components.components import Components
from components.filtros import Filtros
from utils.formatacao import Formatacao
from components.tabelas import Tabelas
from components.graf_orcamentos import Graficos


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

titulo.titulo("ORÇAMENTO", tema)

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

df_orcamento = df_filtrado.drop_duplicates(subset="id_projeto")

orcamento_total = "R$ " + formatacao.formatar_valor_float(df_orcamento['orcamento_consolidado_fundo'].sum())

# ---------- GRÁFICOS ---------

graf_acoes_aporte = graficos.acoes_aporte(df_sem_ano)

graf_taxa_financiamento = graficos.projetos_financiados(df_filtrado)

graf_orcamento_ano = graficos.orcamento_ano(df_sem_ano)

graf_radar_orcamento_tematica = graficos.orcamento_area(df_filtrado)

graf_orcamento_atuacao = graficos.orcamento_atuacao(df_filtrado)

graf_orcamento_centro = graficos.orcamento_centro(df_filtrado)

# --------- DASHBOARD ---------

col_1, col_2, col_3 = st.columns((3, 3, 4))

with col_1:
    with st.container(height=185):
        components.metric_card(
            label="Orçamento Total", 
            value=orcamento_total, 
            delta="", 
            bg_color="#424242"
        )

    with st.container(height=280):
        st.altair_chart(graf_orcamento_ano)

    with st.container(height=280):
        st.plotly_chart(graf_radar_orcamento_tematica, config={"staticPlot": False})

with col_2:
    with st.container(height=275):
        st.altair_chart(graf_taxa_financiamento)

    with st.container(height=485):
        st.altair_chart(graf_orcamento_atuacao)

with col_3:
    with st.container(height=385):
        st.altair_chart(graf_acoes_aporte)

    with st.container(height=375):
        st.altair_chart(graf_orcamento_centro)

    