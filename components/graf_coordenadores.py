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


    def docentes_area(self, df):
        df_docentes_tematico = df[
            [
                'id_projeto', 
                'id_pessoa_membro_datageracao', 
                'categoria_membro', 
                'linha_pesquisa_area_tematica'
            ]
        ]

        df_docentes_tematico = df_docentes_tematico.drop_duplicates(subset=['id_pessoa_membro_datageracao', 'id_projeto'])

        df_docentes_tematico = df_docentes_tematico[df_docentes_tematico['categoria_membro'] == 'DOCENTE']

        df_docentes_tematico = df_docentes_tematico.drop_duplicates().dropna()

        df_docentes_tematico_agrupado = (
            df_docentes_tematico.groupby(
                [
                    'linha_pesquisa_area_tematica'
                ]
            )['categoria_membro']
            .count()
            .reset_index()
        )

        total = df_docentes_tematico_agrupado['categoria_membro'].sum()

        df_docentes_tematico_agrupado['percentual'] = (
            df_docentes_tematico_agrupado['categoria_membro'] / total
        )

        df_docentes_tematico_agrupado['percentual_formatado'] = (
            df_docentes_tematico_agrupado['percentual']
            .apply(lambda x: f"{x:.2%}".replace(".", ","))
        )

        df_docentes_tematico_agrupado['quantidade'] = (
            df_docentes_tematico_agrupado['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_docentes_tematica = (
            alt.Chart(df_docentes_tematico_agrupado)
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
                        labelAngle=45,
                        labelExpr="replace(datum.label, '.', ',')"
                    ),
                    title=None

                ),
                tooltip=[
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
                    alt.Tooltip("percentual_formatado:N", title="Percentual"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_docentes_tematica.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "percentual_formatado:N"
            )
        )

        graf_final_tematica = (
            (graf_docentes_tematica + texto)
            .properties(
                height=325,
                title="Taxa de Coordenadores por Área Temática"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_tematica
    

    def graf_docente_categoria(self, df):
        df_docentes_centro = df[["id_projeto", "id_pessoa_membro_datageracao", "categoria", "categoria_membro"]]
        df_docentes_centro = df_docentes_centro.drop_duplicates(subset=["id_pessoa_membro_datageracao", "id_projeto"])
        
        df_docentes_centro = df_docentes_centro[df_docentes_centro['categoria_membro'] == 'DOCENTE']
        dados_categoria = df_docentes_centro.groupby('categoria')['categoria_membro'].count().reset_index()

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
                title="Total de Coordenadores por tipo de Atividade"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_categoria
    

    def docentes_ano(self, df):
        df_docentes = df[
            [
                'id_projeto',
                'id_pessoa_membro_datageracao',
                'categoria_membro', 
                'data_inicio'
            ]
        ]

        df_docentes = df_docentes.drop_duplicates(subset=['id_pessoa_membro_datageracao', 'data_inicio', 'id_projeto'])

        df_docentes = df_docentes[df_docentes['categoria_membro'] == 'DOCENTE']

        df_docentes['ano'] = df_docentes['data_inicio'].astype(str).str[:4]

        df_docentes_agrupadas = (
            df_docentes.groupby('ano')['categoria_membro']
            .count()
            .reset_index()
        )

        df_docentes_agrupadas['quantidade'] = (
            df_docentes_agrupadas['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_docentes = (
            alt.Chart(df_docentes_agrupadas)
            .mark_bar(
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
                    "categoria_membro:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        texto = graf_docentes.mark_text(
            align="center",
            dy=-5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "quantidade:N"
            )
        )

        graf_final_docentes = (
            (graf_docentes + texto)
            .properties(
                height=360,
                title="Total Coordenadores por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_docentes


    def docentes_centro(self, df):
        df_docentes_centro = df[["id_projeto", "id_pessoa_membro_datageracao", "centro", "categoria_membro"]]
        df_docentes_centro = df_docentes_centro.drop_duplicates(subset=["id_pessoa_membro_datageracao", "id_projeto"])
        
        df_docentes_centro = df_docentes_centro[df_docentes_centro['categoria_membro'] == 'DOCENTE']
        df_docentes = df_docentes_centro.groupby('centro')['categoria_membro'].count().reset_index()

        df_docentes['quantidade'] = (
            df_docentes['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_docente = (
            alt.Chart(df_docentes)
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

        texto = graf_docente.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "quantidade:N"
            )
        )

        graf_docente_centro = (
            (graf_docente + texto)
            .properties(
                height=360,
                title="Total de Coordenadores envolvidos por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_docente_centro
    

    def acao_coordenador(self, df):
        df_acao_coordenador = df[
            [
                "id_projeto", 
                "coordenador"
            ]
        ]

        df_acao_coordenador = df_acao_coordenador.drop_duplicates(subset="id_projeto")

        df_acao_coordenador = df_acao_coordenador.groupby(["coordenador"], as_index=False)["id_projeto"].count()

        altura_linha = 25

        altura_grafico = len(df_acao_coordenador) * altura_linha

        graf_acao_coordenador = (
            alt.Chart(df_acao_coordenador)
            .mark_bar(color=self.grafico_verde)
            .encode(
                y=alt.Y(
                    "coordenador:N",
                    sort="-x",
                    title=None
                ),

                x=alt.X(
                    "id_projeto:Q",
                    title=None
                ),

                tooltip=[
                    alt.Tooltip(
                        "coordenador:N",
                        title="Coordenador"
                    ),

                    alt.Tooltip(
                        "id_projeto:N",
                        title="Quantidade"
                    )
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_acao_coordenador.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "id_projeto:N"
            )
        )

        graf_barra_acao_coordenador = (
            (graf_acao_coordenador + texto)
            .properties(
                height=altura_grafico,
                title="Ações por Coordenador"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_barra_acao_coordenador