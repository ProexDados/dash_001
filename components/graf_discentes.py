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


    def discentes_area(self, df):
        df_discentes_tematico = df[
            [
                'id_projeto', 
                'id_pessoa_membro_datageracao', 
                'categoria_membro', 
                'linha_pesquisa_area_tematica'
            ]
        ]

        df_discentes_tematico = df_discentes_tematico.drop_duplicates(subset=['id_pessoa_membro_datageracao', 'id_projeto'])

        df_discentes_tematico = df_discentes_tematico[df_discentes_tematico['categoria_membro'] == 'DISCENTE']

        df_discentes_tematico = df_discentes_tematico.drop_duplicates().dropna()

        df_discentes_tematico_agrupado = (
            df_discentes_tematico.groupby(
                [
                    'linha_pesquisa_area_tematica'
                ]
            )['categoria_membro']
            .count()
            .reset_index()
        )

        total = df_discentes_tematico_agrupado['categoria_membro'].sum()

        df_discentes_tematico_agrupado['percentual'] = (
            df_discentes_tematico_agrupado['categoria_membro'] / total
        )

        df_discentes_tematico_agrupado['pecentual_formatado'] = (
            df_discentes_tematico_agrupado['percentual']
            .apply(lambda x: f"{x:.2%}".replace(".", ","))
        )

        df_discentes_tematico_agrupado['quantidade'] = (
            df_discentes_tematico_agrupado['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_discentes_tematica = (
            alt.Chart(df_discentes_tematico_agrupado)
            .mark_bar(color=self.grafico_verde)
            .encode(
                y=alt.Y(
                    "linha_pesquisa_area_tematica:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "percentual:Q",
                    axis=alt.Axis( 
                        format=".0%",
                        labelAngle=45
                    ),
                    title=None

                ),
                tooltip=[
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
                    alt.Tooltip("pecentual_formatado:N", title="Percentual"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_discentes_tematica.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "pecentual_formatado:N"
            )
        )

        graf_final_tematica = (
            (graf_discentes_tematica + texto)
            .properties(
                height=325,
                title="Taxa de Discentes por Área Temática"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_tematica
    

    def graf_discente_categoria(self, df):
        df_discentes_centro = df[["id_projeto", "id_pessoa_membro_datageracao", "categoria", "categoria_membro"]]
        df_discentes_centro = df_discentes_centro.drop_duplicates(subset=["id_pessoa_membro_datageracao", "id_projeto"])
        
        df_discentes_centro = df_discentes_centro[df_discentes_centro['categoria_membro'] == 'DISCENTE']
        dados_categoria = df_discentes_centro.groupby('categoria')['categoria_membro'].count().reset_index()

        dados_categoria['quantidade'] = (
            dados_categoria['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_categoria = (
            alt.Chart(dados_categoria)
            .mark_bar(color=self.grafico_vermelho)
            .encode(
                y=alt.Y(
                    "categoria:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "categoria_membro:Q",
                    sort="-y",
                    axis=alt.Axis(
                        labelAngle=45,
                        labelExpr="replace(datum.label, ',', '.')"    
                    ),
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
                height=325,
                title="Total de Discentes por tipo de Atividade"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_categoria
    

    def discentes_ano(self, df):
        df_discentes = df[
            [
                'id_projeto',
                'id_pessoa_membro_datageracao',
                'categoria_membro', 
                'data_inicio'
            ]
        ]

        df_discentes = df_discentes.drop_duplicates(subset=['id_pessoa_membro_datageracao', 'data_inicio', 'id_projeto'])

        df_discentes = df_discentes[df_discentes['categoria_membro'] == 'DISCENTE']

        df_discentes['ano'] = df_discentes['data_inicio'].astype(str).str[:4]

        df_discentes_agrupadas = (
            df_discentes.groupby('ano')['categoria_membro']
            .count()
            .reset_index()
        )

        df_discentes_agrupadas['quantidade'] = (
            df_discentes_agrupadas['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_discentes = (
            alt.Chart(df_discentes_agrupadas)
            .mark_bar(
                color=self.grafico_vermelho
            )
            .encode(
                x=alt.X(
                    "ano:N",
                    axis=alt.Axis(
                        labelAngle=45,
                    ), 
                    title=None
                ),
                y=alt.Y(
                    "categoria_membro:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        texto = graf_discentes.mark_text(
            align="center",
            dy=-5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "quantidade:N"
            )
        )

        graf_final_discentes = (
            (graf_discentes + texto)
            .properties(
                height=360,
                title="Total Discentes por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_discentes


    def discentes_centro(self, df):
        df_discentes_centro = df[["id_projeto", "id_pessoa_membro_datageracao", "centro", "categoria_membro"]]
        df_discentes_centro = df_discentes_centro.drop_duplicates(subset=["id_pessoa_membro_datageracao", "id_projeto"])
        
        df_discentes_centro = df_discentes_centro[df_discentes_centro['categoria_membro'] == 'DISCENTE']
        df_discentes = df_discentes_centro.groupby('centro')['categoria_membro'].count().reset_index()

        df_discentes['quantidade'] = (
            df_discentes['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_discente = (
            alt.Chart(df_discentes)
            .mark_bar(color=self.grafico_verde)
            .encode(
                y=alt.Y(
                    "centro:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "categoria_membro:Q",
                    axis=alt.Axis(
                        labelAngle=45,
                        labelExpr="replace(datum.label, ',', '.')"
                    ),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Categoria"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        texto = graf_discente.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "quantidade:N"
            )
        )

        graf_discente_centro = (
            (graf_discente + texto)
            .properties(
                height=360,
                title="Total de Discentes envolvidos por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_discente_centro