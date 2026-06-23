import altair as alt
import pandas as pd
import numpy as np
import plotly.express as px
from utils.formatacao import Formatacao
from config.settings import Configuracoes
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


class Graficos:
    def __init__(self):
        self.formatacao       = Formatacao()
        self.config           = Configuracoes()
        self.tema             = self.config.tema()
        self.cor_texto        = "white" if self.tema == "dark" else "black"
        self.grafico_verde    = self.config.graficos_verde()
        self.grafico_vermelho = self.config.graficos_vermelho()


    def acoes_aporte(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        financiamento = (
            df
            .groupby(
                [
                    "ano_projeto", 
                    "orcamento_consolidado_fundo"
                ], 
                dropna=False, 
                as_index=False
            )
            .agg(
                qtd_projetos=(
                    'id_projeto', 
                    'count'
                )
            )
        )
        
        financiamento["Não Financiado"] = (
            np.where(
                financiamento["orcamento_consolidado_fundo"] == 0, 
                financiamento["qtd_projetos"], 
                0
            )
        )
        financiamento["Financiado"] = (
            np.where(
                financiamento["orcamento_consolidado_fundo"] > 0, 
                financiamento["qtd_projetos"], 
                0
            )
        )

        financiamento["ano"] = financiamento["ano_projeto"]

        df_long = financiamento.melt(
            id_vars="ano",
            value_vars=["Financiado", "Não Financiado"],
            var_name="serie",
            value_name="valor"
        )

        df_long['ano'] = pd.to_datetime(df_long['ano'], format="%Y").dt.year
        df_finan = df_long.groupby(["ano", "serie"], as_index=False)["valor"].sum()

        df_finan['valor_formatado'] = df_finan['valor'].apply(self.formatacao.formatar_valor_integer)

        graf = (
            alt.Chart(df_finan)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color=self.grafico_verde
                )
            )
            .encode(
                x=alt.X(
                    "ano:N", 
                    title=None,
                    axis=alt.Axis(
                        labelAngle=45
                    ), 
                ),
                y=alt.Y(
                    "valor:Q", 
                    title=None,
                    axis=alt.Axis(
                        labelExpr="replace(datum.label, ',', '.')"
                    )
                ),
                color=alt.Color(
                    "serie:N", 
                    scale=alt.Scale(
                        range=[self.grafico_verde, self.grafico_vermelho]
                    ),title="Série"
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("serie:N", title="Série"),
                    alt.Tooltip("valor_formatado:N", title="Quantidade")
                ]
            )
            .properties(
                height=150,
                title="Quantidade de Ações por Aporte Financeiro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf
    

    def acoes_centro(self, df):
        df_centro = df.drop_duplicates(subset="id_projeto")

        df_acoes_centro = (
            df_centro
            .groupby(df_centro["centro"])
            ["id_projeto"]
            .count()
            .reset_index()
        )

        altura_linha = 35

        altura_grafico = len(df_acoes_centro) * altura_linha

        graf_acoes_centro = (
            alt.Chart(df_acoes_centro)
            .mark_bar(color="#EF4136")
            .encode(
                y=alt.Y(
                    "centro:N",
                    sort="-x",  # ordena pela medida do eixo Y em ordem decrescente
                    title=None
                ),
                x=alt.X(
                    "id_projeto:Q",
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("id_projeto:Q", title="Quantidade")
                ],
                order=alt.Order("id_projeto:Q")
            )
        )

        texto = graf_acoes_centro.mark_text(
            align="center", 
            dy=-5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "id_projeto:Q"
            )
        )

        graf_final_acoes = (
            (graf_acoes_centro + texto)
            .properties(
                height=altura_grafico,
                title="Total de Ações por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_acoes


    def graf_categoria(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        dados_categoria = (
            df
            .groupby(["categoria"], as_index=False)["id_projeto"]
            .count()
        )

        dados_categoria['quantidade'] = (
            dados_categoria['id_projeto']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_categoria = (
            alt.Chart(dados_categoria)
            .mark_bar(color="#009553")
            .encode(
                x=alt.X(
                    "id_projeto:Q",
                    title=None
                ),
                y=alt.Y(
                    "categoria:N",
                    sort="-x",
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("categoria:N", title="Categoria"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        texto = graf_categoria.mark_text(
            align="center", 
            dx=15,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "quantidade:N"
            )
        )

        graf_final_categoria = (
            (graf_categoria + texto)
            .properties(
                height=175,
                title="Total de Ações por Atividade"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_categoria
    

    def graf_acoes(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        dados = df.groupby(["ano_projeto", "situacao_projeto"], as_index=False)["id_projeto"].count()

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
                height=260,
                title="Total de Ações Anuais por situação do Projeto"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_acoes
    

    def acoes_ano(self, df):
        df_acoes = df.drop_duplicates(subset="id_projeto")

        df_acoes['ano'] = df_acoes['data_inicio'].astype(str).str[:4]

        df_acoes_agrupadas = (
            df_acoes.groupby('ano')['id_projeto']
            .count()
            .reset_index()
        )

        df_acoes_agrupadas['quantidade'] = (
            df_acoes_agrupadas['id_projeto']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_acoes = (
            alt.Chart(df_acoes_agrupadas)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color="#067722"
                ),
                color="#067722"
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
                    "id_projeto:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
            .properties(
                height=175,
                title="Ações por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_acoes
    

    def nuvem_tematica(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        texto = " ".join(df["palavras_chave"].dropna().astype(str))

        stopwords = STOPWORDS.union({
            "de", "da", "do", "em", "para", "com", "por", "na", "no", "das", "dos", "nos", "nas", "a", "o", "as", "os", "e", "es"
        })

        wordcloud = WordCloud(
            height=305,
            background_color="white",
            stopwords=stopwords,
            colormap="viridis",
            max_words=100
        ).generate(texto)

        fig, ax = plt.subplots(figsize=(14, 7))

        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")

        ax.set_title(
            "Palavras Chave",
            fontsize=20,
            pad=20,
            loc="left", 
            fontname="Arial"
        )

        return fig
    

