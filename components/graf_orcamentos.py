import altair as alt
import pandas as pd
import numpy as np
import plotly.express as px
from utils.formatacao import Formatacao
from config.settings import Configuracoes


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
                height=350,
                title="Quantidade de Ações por Aporte Financeiro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf
    

    def projetos_financiados(self, df):
        df_orcamento = df[
            [
                'id_projeto', 
                'orcamento_consolidado_fundo'
            ]
        ]

        df_orcamento = df_orcamento.drop_duplicates(subset='id_projeto')

        df_orcamento["orcamento_consolidado_fundo"] = (
            df_orcamento["orcamento_consolidado_fundo"]
            .fillna(0)
        )

        df_orcamento["financiamento"] = (
            np.where(
                df_orcamento["orcamento_consolidado_fundo"] > 0, 
                "FINANCIADO", 
                "NÃO FINANCIADO"
            )
        )

        qtd_orcamento = (
            df_orcamento
            .groupby('financiamento', as_index=False)['orcamento_consolidado_fundo']
            .count()
        )

        total = qtd_orcamento['orcamento_consolidado_fundo'].sum()
        qtd_orcamento['percentual'] = (qtd_orcamento['orcamento_consolidado_fundo'] / total)

        qtd_orcamento['quantidade'] = (
            qtd_orcamento['orcamento_consolidado_fundo']
            .apply(self.formatacao.formatar_valor_integer)
        )

        base = alt.Chart(qtd_orcamento)

        pizza = base.mark_arc(innerRadius=60).encode(
            theta=alt.Theta("percentual:Q", stack=True),
            color=alt.Color(
                "financiamento:N", 
                title="Financiamento",
                scale=alt.Scale(
                    domain=["FINANCIADO", "NÃO FINANCIADO"],
                    range=[self.grafico_verde, self.grafico_vermelho]
                )
            ),
            tooltip=[
                alt.Tooltip("financiamento:N", title="Financiamento"),
                alt.Tooltip("quantidade:N", title="Quantidade"),
                alt.Tooltip("percentual:Q", format=".2%", title="Porcentagem")
            ],
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
        )

        texto = base.mark_text(
            radius=85,
            size=12, 
            fontWeight="bold",
            fill="white"
        ).encode(
            theta=alt.Theta("percentual:Q", stack=True),
            text=alt.Text("percentual:Q", format=".2%"),
            detail="financiamento:N",
            order=alt.Order("percentual:Q", sort="descending")
        )

        graf_financiamento = (pizza + texto).properties(
            width=240,
            height=240,
            title="Ações Com e Sem Financiamento"
        ).configure_view(
            strokeWidth=0
        ).configure_title(
            fontSize=20
        )

        return graf_financiamento
    

    def orcamento_ano(self, df):
        df = df.drop_duplicates(subset=['id_projeto'])

        df["orcamento_consolidado_fundo"] = (
            df["orcamento_consolidado_fundo"]
            .fillna(0)
        )

        df_orcamento_ano = (
            df
            .groupby(df["ano_projeto"])
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
            .mark_bar(color=self.grafico_verde)
            .encode(
                x=alt.X(
                    "ano_projeto:N",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
                    "orcamento_consolidado_fundo:Q",
                    title=None,
                    axis=alt.Axis(
                        labelExpr="'R$ ' + replace(datum.label, /,/g, '.')"
                    )
                ),
                tooltip=[
                    alt.Tooltip("ano_projeto:N", title="Ano"),
                    alt.Tooltip("valor_formatado:N", title="Orçamento")
                ],
                order=alt.Order("ano_projeto:N")
            )
        )

        texto = graf_orcamento_ano.mark_text(
            align="center", 
            dy=-5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "valor_formatado:N"
            )
        )

        graf_final_orcamento = (
            (graf_orcamento_ano + texto)
            .properties(
                height=245,
                title="Orçamento Total por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_orcamento
    

    def orcamento_area(self, df):
        df_spider = (
            df
            .drop_duplicates(subset='id_projeto')
        )

        df_spider_agrupado = (
            df_spider
            .groupby(['linha_pesquisa_area_tematica'])['orcamento_consolidado_fundo']
            .sum()
            .reset_index()
        )
        
        df_spider_agrupado['valor_formatado'] = (
            "R$ " +
            df_spider_agrupado['orcamento_consolidado_fundo']
            .apply(self.formatacao.formatar_valor_float)
        )

        fig_radar = px.line_polar(
            df_spider_agrupado,
            r='orcamento_consolidado_fundo',
            theta='linha_pesquisa_area_tematica',
            line_close=True,
            custom_data=['valor_formatado']
        )

        fig_radar.update_layout(
            width=245,
            height=245,
            title="Orçamento Total por Área Temática",
            title_font=dict(
                size=20
            ),
            margin=dict(
                b=40,
                l=40
            ),
            polar=dict(
                    radialaxis=dict(
                       color="black"
                )
            )
        )

        fig_radar.update_traces(
            fill='toself',
            line=dict(color=self.grafico_vermelho),
            mode='lines+markers',  # <- importante
            marker=dict(size=6),
            hovertemplate=
                "<b>%{theta}</b><br>" +
                "Valor: %{customdata[0]}<br>" +
                "<extra></extra>"
        )

        return fig_radar
    

    def orcamento_atuacao(self, df):
        df_orcamento_atuacoes = df.drop_duplicates(subset='id_projeto')

        df_orcamento = (
            df_orcamento_atuacoes
            .groupby(["linha_atuacao"], as_index=False)["orcamento_consolidado_fundo"]
            .sum()
        )

        df_orcamento['valor_formatado'] = (
            "R$ " +
            df_orcamento['orcamento_consolidado_fundo']
            .apply(self.formatacao.formatar_valor_float)
        )

        altura_linha = 35

        altura_grafico = len(df_orcamento) * altura_linha

        graf_orcamento = (
            alt.Chart(df_orcamento)
            .mark_bar(color=self.grafico_verde)
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
                        format=",.0f"
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

        texto = graf_orcamento.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "valor_formatado:N"
            )
        )

        graf_barra_orcamento = (
            (graf_orcamento + texto)
            .properties(
                height=altura_grafico,
                title="Orçamento Total por Atuação"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_barra_orcamento
    

    def orcamento_centro(self, df):
        df = df.drop_duplicates(subset='id_projeto')

        df_centro = (
            df
            .groupby('centro')['orcamento_consolidado_fundo']
            .sum()
            .reset_index()
        )

        df_centro['valor_formatado'] = (
            "R$ " +
            df_centro['orcamento_consolidado_fundo']
            .apply(self.formatacao.formatar_valor_float)
        )

        graf_centro = (
            alt.Chart(df_centro)
            .mark_bar(
                color=self.grafico_vermelho
            )
            .encode(
                x=alt.X(
                    'centro:N',
                    axis=alt.Axis(
                        labelAngle=45
                    ),
                    title=None
                ),
                y=alt.Y(
                    "orcamento_consolidado_fundo:Q",
                    title=None,
                    axis=alt.Axis(
                        labelExpr="'R$ ' + replace(datum.label, /,/g, '.')"
                    )
                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("valor_formatado:N", title="Orçamento")
                ]
            )
        )

        texto = graf_centro.mark_text(
            align="center",
            dy=-5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "valor_formatado:N"
            )
        )

        graf_final_centro = (
            (graf_centro + texto)
            .properties(
                height=340,
                title="Orçamento Total por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_centro