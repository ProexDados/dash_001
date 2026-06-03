import streamlit as st
from services.get_files import Files
from components.components import Components
from components.filtros import Filtros
import altair as alt
import pandas as pd
import numpy as np
import locale
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


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
        st.title("ORÇAMENTO")

# -------- OBTEM DADOS --------
file = Files()
filtros = Filtros()

df_projeto = file.projeto()
df_membro = file.membro_projeto()

df_projeto = df_projeto[
    [
        "id_projeto", 
        "ano_projeto", 
        "abrangencia",
        "centro", 
        "categoria",
        "total_discentes_envolvidos",
        "data_inicio",
        "bolsas_concedidas",
        "linha_pesquisa_area_tematica",
        "linha_atuacao",
        "tipo_projeto",
        "orcamento_consolidado_fundo",
        "palavras_chave"
    ]
]

df_projeto = df_projeto[df_projeto["tipo_projeto"] == "EXTENSÃO"]

df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)
df_projeto["ano_projeto"] = pd.to_numeric(df_projeto["ano_projeto"])

df_projeto['orcamento_consolidado_fundo'] = (
    df_projeto['orcamento_consolidado_fundo']
    .astype(float)
)


def formatar_valor(df):
    df["valor_formatado"] = (
        df["orcamento_consolidado_fundo"]
        .apply(
            lambda x:
            f"R$ {x:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )

    return df



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

# ------------------------------------------------------------------------------

areas_tematicas = (
    df_filtrado[
        [
            'centro'
        ]
    ]
    .drop_duplicates()
    .count()
)

# ------------------------------------------------------------------------------

orcamento_centro = df_filtrado[
    [
        'orcamento_consolidado_fundo',
        'centro',
        'ano_projeto'
    ]
]

dados_centro = (
    orcamento_centro
    .groupby(['centro', 'ano_projeto'])['orcamento_consolidado_fundo']
    .sum()
    .reset_index()
)

dados_centro = formatar_valor(dados_centro)

dados_centro['orcamento_consolidado_fundo'] = np.where(dados_centro['orcamento_consolidado_fundo'] == 0, None, dados_centro['orcamento_consolidado_fundo'])

graf_centro = (
    alt.Chart(dados_centro)
    .mark_rect()
    .encode(
        x=alt.X(
            "ano_projeto:O",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "centro:N",
            title="Centros"
        ),
        color=alt.Color(
            "orcamento_consolidado_fundo:Q",
            title="Valor",
            scale=alt.Scale(scheme="reds"),
            legend=alt.Legend(
                format="~s"
            )
        ),
        tooltip=[
            alt.Tooltip("centro:N", title="Centro"),
            alt.Tooltip("ano_projeto:O", title="Ano Projeto"),
            alt.Tooltip("valor_formatado:N", title="Valor Total")
        ]
    )
    .properties(
        height=320,
        title="Orçamento total por Centro"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------
df_orcamento_atuacoes = df_filtrado[["linha_atuacao", "orcamento_consolidado_fundo"]]
df_orcamento_atuacoes = df_orcamento_atuacoes.drop_duplicates()

df_orcamento = df_orcamento_atuacoes.groupby(["linha_atuacao"], as_index=False)["orcamento_consolidado_fundo"].sum()

df_orcamento = formatar_valor(df_orcamento)

altura_linha = 35

altura_grafico = len(df_orcamento) * altura_linha

graf_orcamento = (
    alt.Chart(df_orcamento)
    .mark_bar(color="#009553")
    .encode(
        y=alt.Y(
            "linha_atuacao:N",
            sort="-x",
            title=None
        ),

        x=alt.X(
            "orcamento_consolidado_fundo:Q",
            title=None,
            axis=alt.Axis(
                format=",.0f"  # eixo numérico simplificado
            )
        ),

        tooltip=[
            alt.Tooltip(
                "linha_atuacao:N",
                title="Linha Atuação"
            ),

            alt.Tooltip(
                "valor_formatado:N",
                title="Valor Total"
            )
        ]
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_orcamento.mark_text(
    align="left",
    dx=5
).encode(
    text=alt.Text(
        "valor_formatado:N"
    )
)

graf_barra_orcamento = (
    (graf_orcamento + texto)
    .properties(
        height=altura_grafico,
        title="Orçamento Total por Linha de Atuação"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_ano = df_filtrado[['id_projeto', 'data_inicio', 'orcamento_consolidado_fundo']]
df_ano = df_ano.drop_duplicates(subset=['id_projeto'])

df_ano["orcamento_consolidado_fundo"] = (
    df_ano["orcamento_consolidado_fundo"]
    .fillna(0)
)

df_ano["data_inicio"] = pd.to_datetime(df_ano["data_inicio"])

df_orcamento_ano = (
    df_ano
    .groupby(df_ano["data_inicio"].dt.year)
    ["orcamento_consolidado_fundo"]
    .sum()
    .reset_index()
)

df_orcamento_ano["valor_formatado"] = (
    df_orcamento_ano["orcamento_consolidado_fundo"]
    .apply(
        lambda x:
        f"R$ {x:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
)

graf_orcamento_ano = (
    alt.Chart(df_orcamento_ano)
    .mark_bar(color="#009553")
    .encode(
        x=alt.X(
            "data_inicio:N",
            axis=alt.Axis(labelAngle=45),
            title=None
        ),
        y=alt.Y(
            "orcamento_consolidado_fundo:Q",
            title=None
        ),
        tooltip=[
            alt.Tooltip("data_inicio:N", title="Ano"),
            alt.Tooltip("valor_formatado:N", title="Quantidade")
        ],
        order=alt.Order("data_inicio:N")
    )
)

# camada de texto (percentual no fim da barra)
texto = graf_orcamento_ano.mark_text(
    align="center", dy=-5
).encode(
    text=alt.Text(
        "valor_formatado:N"
    )
)

graf_final_orcamento = (
    (graf_orcamento_ano + texto)
    .properties(
        height=465,
        title="Orçamento Total por Ano"
    )
    .configure_title(
        fontSize=20
    )
)

# ------------------------------------------------------------------------------

df_spider = (
    df_filtrado[
        [
            'id_projeto', 
            'linha_pesquisa_area_tematica',
            'orcamento_consolidado_fundo'
        ]
    ]
    .drop_duplicates(subset='id_projeto')
)

df_spider_agrupado = (
    df_spider
    .groupby(['linha_pesquisa_area_tematica'])['orcamento_consolidado_fundo']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

df_spider_agrupado = formatar_valor(df_spider_agrupado)

fig_radar = px.line_polar(
    df_spider_agrupado,
    r='orcamento_consolidado_fundo',
    theta='linha_pesquisa_area_tematica',
    line_close=True,
    custom_data=['valor_formatado']
)

fig_radar.update_layout(
    width=345,
    height=345,
    title="Orçamento por Área Temática",
    title_font=dict(
        size=20
    ),
    margin=dict(
        b=40,
        l=40
    )
)

fig_radar.update_traces(
    fill='toself',
    line=dict(color="#009553"),
    mode='lines+markers',  # <- importante
    marker=dict(size=6),
    hovertemplate=
        "<b>%{theta}</b><br>" +
        "Valor: %{customdata[0]}<br>" +
        "<extra></extra>"
)

# ------------------------------------------------------------------------------

df_orcamento = df_filtrado[['id_projeto', 'orcamento_consolidado_fundo']]

df_orcamento = df_orcamento.drop_duplicates(subset='id_projeto')

df_orcamento["orcamento_consolidado_fundo"] = df_orcamento["orcamento_consolidado_fundo"].fillna(0)

df_orcamento["financiamento"] = np.where(df_orcamento["orcamento_consolidado_fundo"] > 0, "COM FINANCIAMENTO", "SEM FINANCIAMENTO")

qtd_orcamento = (
    df_orcamento
    .groupby('financiamento', as_index=False)['orcamento_consolidado_fundo']
    .count()
)

total = qtd_orcamento['orcamento_consolidado_fundo'].sum()
qtd_orcamento['percentual'] = (qtd_orcamento['orcamento_consolidado_fundo'] / total)

base = alt.Chart(qtd_orcamento)

# Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
pizza = base.mark_arc(innerRadius=80).encode(
    # 'stack=True' garante que as fatias sejam empilhadas proporcionalmente
    theta=alt.Theta("percentual:Q", stack=True),
    color=alt.Color(
        "financiamento:N", 
        title="Financiamento",
        scale=alt.Scale(
            domain=["COM FINANCIAMENTO", "SEM FINANCIAMENTO"],
            range=["#009553", "#EF4136"]
        )
    ),
    tooltip=[
        alt.Tooltip("financiamento:N", title="Financiamento"),
        alt.Tooltip("orcamento_consolidado_fundo:Q", title="Quantidade"),
        alt.Tooltip("percentual:Q", format=".2%", title="Porcentagem")
    ],
    order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
)

# Texto centralizado nas fatias
texto = base.mark_text(
    radius=105,  # Distância do centro. Aumente para afastar do meio.
    size=14, 
    fontWeight="bold",
    fill="white" # Ou "white" se a fatia for muito escura
).encode(
    # O theta DEVE ser idêntico ao da pizza para o alinhamento funcionar
    theta=alt.Theta("percentual:Q", stack=True),
    text=alt.Text("percentual:Q", format=".2%"), # format=".0f" remove casas decimais
    detail="financiamento:N",  # Garante que o texto se alinhe corretamente à fatia
    order=alt.Order("percentual:Q", sort="descending")  # Garantir que os textos sigam a mesma ordem
)

graf_financiamento = (pizza + texto).properties(
    width=345,
    height=345,
    title="Contagem de projetos com e sem financiamento"
).configure_view(
    strokeWidth=0  # Remove a borda externa do gráfico
).configure_title(
    fontSize=20
)

# ------------------------------------------------------------------------------

st.markdown("<br>", unsafe_allow_html=True)

col_1, col_2, col_3 = st.columns((0.33, 0.33, 0.34))

with col_1:
    with st.container(height=235):
        components = Components()

        components.metric_card("Unidades Gestoras", areas_tematicas['centro'], "", "#424242")

    with st.container(height=500):
        st.altair_chart(graf_final_orcamento, use_container_width=True)

with col_2:
    with st.container(height=355):
        st.altair_chart(graf_centro, use_container_width=True)

    with st.container(height=380):
        st.plotly_chart(fig_radar, use_container_width=True, config={"staticPlot": False})

with col_3:
    with st.container(height=355):
        st.altair_chart(graf_barra_orcamento, use_container_width=True)

    with st.container(height=380):
        st.altair_chart(graf_financiamento, use_container_width=True)
        