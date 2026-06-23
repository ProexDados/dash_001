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


    def extensionistas(self, df):
        df_membros = df.drop_duplicates(subset='id_pessoa_membro_datageracao')

        qtd_membro = (
            df_membros
            .groupby('categoria_membro', as_index=False)['id_projeto']
            .count()
        )

        total = qtd_membro['id_projeto'].sum()
        qtd_membro['percentual'] = (qtd_membro['id_projeto'] / total)
        qtd_membro['percentual_formatado'] = (
            qtd_membro['percentual']
            .apply(lambda x: f"{x:.2%}".replace(".", ","))
        )

        qtd_membro['quantidade'] = (
            qtd_membro['id_projeto']
            .apply(self.formatacao.formatar_valor_integer)
        )

        base = alt.Chart(qtd_membro)

        # Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
        pizza = base.mark_arc().encode(
            # 'stack=True' garante que as fatias sejam empilhadas proporcionalmente
            theta=alt.Theta("percentual:Q", stack=True),
            color=alt.Color("categoria_membro:N", title="Tipo vínculo"),
            tooltip=[
                alt.Tooltip("categoria_membro:N", title="Tipo vínculo"),
                alt.Tooltip("quantidade:N", title="Quantidade"),
                alt.Tooltip("percentual_formatado:N", title="Porcentagem")
            ],
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
        )

        # Texto centralizado nas fatias
        texto = base.mark_text(
            radius=70,  # Distância do centro. Aumente para afastar do meio.
            size=14, 
            fontWeight="bold",
            fill="black" # Ou "white" se a fatia for muito escura
        ).encode(
            # O theta DEVE ser idêntico ao da pizza para o alinhamento funcionar
            theta=alt.Theta("percentual:Q", stack=True),
            text=alt.Text("percentual_formatado:N"), # format=".0f" remove casas decimais
            detail="categoria_membro:N",  # Garante que o texto se alinhe corretamente à fatia
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que os textos sigam a mesma ordem
        )

        graf_membro = (pizza + texto).properties(
            width=265,
            height=265,
            title="Tipo de Vínculo do Participante"
        ).configure_view(
            strokeWidth=0  # Remove a borda externa do gráfico
        ).configure_title(
            fontSize=20
        )

        return graf_membro
    

    def extencionista_centro(self, df):
        df_extensionistas = df.drop_duplicates(subset=['id_pessoa_membro_datageracao'])

        df_extensionistas_agrupado = (
            df_extensionistas.groupby(
                [
                    'centro'
                ]
            )['categoria_membro']
            .count()
            .reset_index()
        )

        total = df_extensionistas_agrupado['categoria_membro'].sum()

        df_extensionistas_agrupado['percentual'] = (
            df_extensionistas_agrupado['categoria_membro'] / total
        )
        df_extensionistas_agrupado['percentual_formatado'] = (
            df_extensionistas_agrupado['percentual']
            .apply(lambda x: f"{x:.2%}".replace(".", ","))
        )

        df_extensionistas_agrupado['quantidade'] = (
            df_extensionistas_agrupado['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_extensionistas = (
            alt.Chart(df_extensionistas_agrupado)
            .mark_bar(color=self.grafico_verde)
            .encode(
                y=alt.Y(
                    "centro:N",
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
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("percentual_formatado:N", title="Percentual"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_extensionistas.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "percentual_formatado:N"
            )
        )

        graf_final = (
            (graf_extensionistas + texto)
            .properties(
                height=465,
                title="Taxa de Participantes por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final
    

    def participantes_ano(self, df):
        df_participantes = df[
            [
                'id_projeto', 
                'id_pessoa_membro_datageracao', 
                'data_inicio'
            ]
        ]

        df_participantes = df_participantes.drop_duplicates(subset=['id_pessoa_membro_datageracao', 'data_inicio', 'id_projeto'])

        df_participantes['ano'] = df_participantes['data_inicio'].astype(str).str[:4]

        df_participantes_agrupadas = (
            df_participantes.groupby('ano')['id_pessoa_membro_datageracao']
            .count()
            .reset_index()
        )

        df_participantes_agrupadas['quantidade'] = (
            df_participantes_agrupadas['id_pessoa_membro_datageracao']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_participantes = (
            alt.Chart(df_participantes_agrupadas)
            .mark_bar(
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
                    "id_pessoa_membro_datageracao:Q", 
                    title=None,
                    axis=alt.Axis(
                        labelExpr="replace(datum.label, ',', '.')"
                    )
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
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

        graf_final_participantes = (
            (graf_participantes + texto)
            .properties(
                height=220,
                title="Total Participantes por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_participantes
    

    def extencionista_area(self, df):
        df_extensionistas_tematico = df[
            [
                'id_projeto', 
                'id_pessoa_membro_datageracao', 
                'categoria_membro', 
                'linha_pesquisa_area_tematica'
            ]
        ]

        df_extensionistas_tematico = df_extensionistas_tematico.drop_duplicates(subset=['id_pessoa_membro_datageracao', 'id_projeto'])

        df_extensionistas_tematico_agrupado = (
            df_extensionistas_tematico.groupby(
                [
                    'linha_pesquisa_area_tematica'
                ]
            )['categoria_membro']
            .count()
            .reset_index()
        )

        total = df_extensionistas_tematico_agrupado['categoria_membro'].sum()

        df_extensionistas_tematico_agrupado['percentual'] = (
            df_extensionistas_tematico_agrupado['categoria_membro'] / total
        )
        df_extensionistas_tematico_agrupado['percentual_formatado'] = (
            df_extensionistas_tematico_agrupado['percentual']
            .apply(lambda x: f"{x:.2%}".replace(".", ","))
        )

        df_extensionistas_tematico_agrupado['quantidade'] = (
            df_extensionistas_tematico_agrupado['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_extensionistas_tematica = (
            alt.Chart(df_extensionistas_tematico_agrupado)
            .mark_bar(
                color=self.grafico_vermelho
            )
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
        texto = graf_extensionistas_tematica.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "percentual_formatado:N"
            )
        )

        graf_final_tematica = (
            (graf_extensionistas_tematica + texto)
            .properties(
                height=220,
                title="Taxa de Participantes por Área Temática"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_tematica


    def volume_participante_centro(self, df):
        df_participante = df[
            [
                'id_projeto', 
                'id_pessoa_membro_datageracao', 
                'categoria_membro', 
                'centro'
            ]
        ]

        df_participante_agrupado = (
            df_participante.groupby(
                [
                    'centro'
                ]
            )['categoria_membro']
            .count()
            .reset_index()
        )

        total = df_participante_agrupado['categoria_membro'].sum()

        df_participante_agrupado['percentual'] = (
            df_participante_agrupado['categoria_membro'] / total
        )
        df_participante_agrupado['percentual_formatado'] = (
            df_participante_agrupado['percentual']
            .apply(lambda x: f"{x:.2%}".replace(".", ","))
        )

        df_participante_agrupado['quantidade'] = (
            df_participante_agrupado['categoria_membro']
            .apply(self.formatacao.formatar_valor_integer)
        )

        graf_participante = (
            alt.Chart(df_participante_agrupado)
            .mark_bar(color=self.grafico_vermelho)
            .encode(
                y=alt.Y(
                    "centro:N",
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
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("percentual_formatado:N", title="Percentual"),
                    alt.Tooltip("quantidade:N", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_participante.mark_text(
            align="left",
            dx=5,
            color=self.cor_texto
        ).encode(
            text=alt.Text(
                "percentual_formatado:N"
            )
        )

        graf_final = (
            (graf_participante + texto)
            .properties(
                height=465,
                title="Volume de Participação por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final
    

    def graf_participante_categoria(self, df):
        df_participantes_centro = df[["id_projeto", "id_pessoa_membro_datageracao", "categoria", "categoria_membro"]]
        df_participantes_centro = df_participantes_centro.drop_duplicates(subset=["id_pessoa_membro_datageracao", "id_projeto"])
        
        dados_categoria = df_participantes_centro.groupby('categoria')['categoria_membro'].count().reset_index()
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
                height=220,
                title="Total de Participantes por tipo de Atividade"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_categoria
