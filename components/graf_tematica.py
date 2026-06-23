import altair as alt
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


    def acoes_area(self, df):
        df_spider = (
            df[
                [
                    'id_projeto', 
                    'linha_pesquisa_area_tematica'
                ]
            ]
            .drop_duplicates(subset='id_projeto')
        )

        df_spider_agrupado = (
            df_spider
            .groupby(['linha_pesquisa_area_tematica'])['id_projeto']
            .count()
            .reset_index()
        )

        # df_spider_agrupado['id_projeto']

        fig_radar = px.line_polar(
            df_spider_agrupado,
            r='id_projeto',
            theta='linha_pesquisa_area_tematica',
            line_close=True
        )

        fig_radar.update_layout(
            width=325,
            height=325,
            title="Quantidade de ações por área temática",
            title_font=dict(
                size=20
            ),
            margin=dict(
                b=40,
                l=40,
                r=40
            ),
            polar=dict(
                    radialaxis=dict(
                       color="black"
                )
            )
        )
        
        fig_radar.update_traces(
            fill='toself',
            line=dict(color=self.grafico_verde),
            mode='lines+markers',
            marker=dict(size=6),
            hovertemplate=
                "<b>%{theta}</b><br>" +
                "Valor: %{customdata}<br>" +
                "<extra></extra>",
            customdata=[
                [
                    f"{valor:,.0f}".replace(",", ".")
                ]
                for valor in df_spider_agrupado["id_projeto"]
            ]
        )

        return fig_radar
    

    def acoes_tematica(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        dados_tema = df.groupby(["ano_projeto", "linha_pesquisa_area_tematica"], as_index=False)["id_projeto"].count()

        graf_tematica = (
            alt.Chart(dados_tema)
            .mark_rect()
            .encode(
                x=alt.X(
                    "ano_projeto:O",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
                    "linha_pesquisa_area_tematica:N",
                    title=None
                ),
                color=alt.Color(
                    "id_projeto:Q",
                    title="Quantidade",
                    scale=alt.Scale(scheme="greens"),
                    legend=alt.Legend(
                        format="~s"
                    )
                ),
                tooltip=[
                    alt.Tooltip("ano_projeto:O", title="Ano"),
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área temática"),
                    alt.Tooltip("id_projeto:Q", title="Quantidade")
                ]
            )
            .properties(
                height=365,
                title="Quantidade de Ações Anuais por Área Temática"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_tematica


    def area_atividade(self, df):
        acoes_tematica_atividade = df[
            [
                'id_projeto',
                'categoria',
                'linha_pesquisa_area_tematica'
            ]
        ].drop_duplicates(subset="id_projeto")

        dados_tematica = (
            acoes_tematica_atividade
            .groupby(['categoria', 'linha_pesquisa_area_tematica'])['id_projeto']
            .count()
            .reset_index()
        )

        dados_tematica = dados_tematica[dados_tematica['id_projeto'] > 0]

        graf_tematica = (
            alt.Chart(dados_tematica)
            .mark_rect()
            .encode(
                x=alt.X(
                    "categoria:N",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
                    "linha_pesquisa_area_tematica:N",
                    title=None
                ),
                color=alt.Color(
                    "id_projeto:Q",
                    title="Quantidade",
                    scale=alt.Scale(scheme="reds"),
                    legend=alt.Legend(
                        format="~s"
                    )
                ),
                tooltip=[
                    alt.Tooltip("categoria:N", title="Categoria"),
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
                    alt.Tooltip("id_projeto:Q", title="Quantidade")
                ]
            )
            .properties(
                height=365,
                title="Quantidade de Ações por Área Temática e Categoria"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_tematica
    

    def area_centro(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        dados_tema = df.groupby(["linha_pesquisa_area_tematica", "centro"], as_index=False)["id_projeto"].count()

        graf_tematica = (
            alt.Chart(dados_tema)
            .mark_rect()
            .encode(
                x=alt.X(
                    "linha_pesquisa_area_tematica:N",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
                    "centro:N",
                    title=None
                ),
                color=alt.Color(
                    "id_projeto:Q",
                    title="Quantidade",
                    scale=alt.Scale(scheme="greens"),
                    legend=alt.Legend(
                        format="~s"
                    )
                ),
                tooltip=[
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("id_projeto:Q", title="Quantidade")
                ]
            )
            .properties(
                height=325,
                title="Quantidade de Ações por Área Temática e Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_tematica
    

    # def area_centro_3d(self, df):

    #     dados_tema = (
    #         df
    #         .groupby(
    #             [
    #                 "linha_pesquisa_area_tematica",
    #                 "centro"
    #             ],
    #             as_index=False
    #         )["id_projeto"]
    #         .count()
    #     )


    #     fig = px.scatter_3d(
    #         dados_tema,
    #         x="linha_pesquisa_area_tematica",
    #         y="centro",
    #         z="id_projeto",
    #         size="id_projeto",
    #         color="id_projeto",
    #         color_continuous_scale="Greens",
    #         hover_data=[
    #             "linha_pesquisa_area_tematica",
    #             "centro",
    #             "id_projeto"
    #         ]
    #     )


    #     fig.update_layout(
    #         width=700,
    #         height=600,
    #         title="Quantidade de Ações por Área Temática e Centro",
    #         scene=dict(
    #             xaxis_title=None,
    #             yaxis_title=None,
    #             zaxis_title=None
    #         )
    #     )


    #     return fig