import altair as alt
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


    def linha_atuacao_categoria(self, df):
        df = df.drop_duplicates(subset=["categoria", "linha_atuacao"])

        dados_linha_atuacao = df.groupby(["categoria"], as_index=False)["linha_atuacao"].count()

        graf_atuacoes = (
            alt.Chart(dados_linha_atuacao)
            .mark_bar(color=self.grafico_verde)
            .encode(
                y=alt.Y(
                    "categoria:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "linha_atuacao:Q",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("categoria:N", title="Categoria"),
                    alt.Tooltip("linha_atuacao:Q", title="Quantidade")
                ]
            )
        )

        texto = graf_atuacoes.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "linha_atuacao:N"
            )
        )

        graf_final_atuacoes = (
            (graf_atuacoes + texto)
            .properties(
                height=225,
                title="Total Linha de Atuação por Categorias"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_atuacoes
    

    def acoes_atuacao(self, df):
        df = df.drop_duplicates(subset="id_projeto")

        df_atuacoes = df.groupby(["linha_atuacao"], as_index=False)["id_projeto"].count()

        altura_linha = 35

        altura_grafico = len(df_atuacoes) * altura_linha

        graf_atuacoes = (
            alt.Chart(df_atuacoes)
            .mark_bar(color=self.grafico_vermelho)
            .encode(
                y=alt.Y(
                    "linha_atuacao:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "id_projeto:Q",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("linha_atuacao:N", title="Linha Atuação"),
                    alt.Tooltip("id_projeto:Q", title="Quantidade")
                ]
            )
        )

        texto = graf_atuacoes.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "id_projeto:N"
            )
        )

        graf_final_atuacoes = (
            (graf_atuacoes + texto)
            .properties(
                height=altura_grafico,
                title="Total Ações por Linha de Atuação"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_atuacoes
    

    def atuacoes_centros(self, df):
        df = df.drop_duplicates(subset=["centro", "linha_atuacao"])

        df_atuacoes_grupado = (
            df
            .groupby("centro")["linha_atuacao"]
            .count()
            .reset_index()
        )

        df_atuacoes_grupado['quantidade'] = (
            df_atuacoes_grupado['linha_atuacao']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_participantes = (
            alt.Chart(df_atuacoes_grupado)
            .mark_bar(
                color=self.grafico_vermelho
            )
            .encode(
                x=alt.X(
                    "centro:N",
                    axis=alt.Axis(
                        labelAngle=45
                    ), 
                    title=None
                ),
                y=alt.Y(
                    "linha_atuacao:Q", 
                    title=None,
                    axis=alt.Axis(
                        labelExpr="replace(datum.label, ',', '.')"
                    )
                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        texto = graf_participantes.mark_text(
            align="center",
            dy=-5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "quantidade:N"
            )
        )

        graf_final = (
            (graf_participantes + texto)
            .properties(
                height=365,
                title="Total de Linha de Atuação por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final
    

    def linha_atuacao_area_conhecimento(self, df):
        df = df.drop_duplicates(subset=["area_conhecimento_cnpq_projeto", "linha_atuacao"])

        dados_linha_atuacao = df.groupby(["area_conhecimento_cnpq_projeto"], as_index=False)["linha_atuacao"].count()

        graf_atuacoes = (
            alt.Chart(dados_linha_atuacao)
            .mark_bar(color="#009553")
            .encode(
                y=alt.Y(
                    "area_conhecimento_cnpq_projeto:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "linha_atuacao:Q",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("area_conhecimento_cnpq_projeto:N", title="Área do Conhecimento"),
                    alt.Tooltip("linha_atuacao:Q", title="Quantidade")
                ]
            )
        )

        texto = graf_atuacoes.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "linha_atuacao:N"
            )
        )

        graf_final_atuacoes = (
            (graf_atuacoes + texto)
            .properties(
                height=325,
                title="Total Linha de Atuação por Área do Conhecimento"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_atuacoes
