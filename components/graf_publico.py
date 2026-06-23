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


    def estimado_interno(self, df):
        df_interno = df.drop_duplicates(subset='id_projeto')

        df_interno['publico_estimado_interno'] = df_interno['publico_estimado_interno'].fillna(0).astype(int)
        df_interno['ano'] = df_interno['data_inicio'].astype(str).str[:4]

        df_interno_agrupadas = (
            df_interno.groupby('ano')['publico_estimado_interno']
            .sum()
            .reset_index()
        )

        df_interno_agrupadas['publico_interno_formatado'] = (
            df_interno_agrupadas['publico_estimado_interno']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_interno = (
            alt.Chart(df_interno_agrupadas)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color=self.grafico_vermelho
                ),
                color=self.grafico_vermelho
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
                    "publico_estimado_interno:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("publico_interno_formatado:N", title="Quantidade")
                ]
            )
            .properties(
                height=200,
                title="Público Estimado Interno por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_interno
    

    def estimado_externo(self, df):
        df_externo = df.drop_duplicates(subset='id_projeto')

        df_externo['publico_estimado_externo'] = df_externo['publico_estimado_externo'].fillna(0).astype(int)
        df_externo['ano'] = df_externo['data_inicio'].astype(str).str[:4]

        df_externo_agrupadas = (
            df_externo.groupby('ano')['publico_estimado_externo']
            .sum()
            .reset_index()
        )

        df_externo_agrupadas['publico_externo_formatado'] = (
            df_externo_agrupadas['publico_estimado_externo']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_externo = (
            alt.Chart(df_externo_agrupadas)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color=self.grafico_verde
                ),
                color=self.grafico_verde
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
                    "publico_estimado_externo:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("publico_externo_formatado:N", title="Quantidade")
                ]
            )
            .properties(
                height=200,
                title="Público Estimado Externo por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_externo
    

    def atendido_ano(self, df):
        df_atendido = df.drop_duplicates(subset='id_projeto')

        df_atendido['publico_atendido'] = df_atendido['publico_atendido'].fillna(0).astype(int)
        df_atendido['ano'] = df_atendido['data_inicio'].astype(str).str[:4]

        df_atendido_agrupadas = (
            df_atendido.groupby('ano')['publico_atendido']
            .sum()
            .reset_index()
        )

        df_atendido_agrupadas['publico_atendido_formatado'] = (
            df_atendido_agrupadas['publico_atendido']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_atendido = (
            alt.Chart(df_atendido_agrupadas)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color=self.grafico_vermelho
                ),
                color=self.grafico_vermelho
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
                    "publico_atendido:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("publico_atendido_formatado:N", title="Quantidade")
                ]
            )
            .properties(
                height=200,
                title="Público Atendido por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_atendido
