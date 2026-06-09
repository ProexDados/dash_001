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
        self.formatacao = Formatacao()
        self.config     = Configuracoes()
        self.tema       = self.config.tema()


    # -- HISTÓRICO 1 -------------

    def graf_acoes(self, df):
        # Agrupa os dados
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
                height=465,
                title="Total de Ações Anuais por situação do Projeto"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_acoes
    

    def graf_categoria(self, df):
        # categorias
        dados_categoria = df.groupby(["categoria"], as_index=False)["numero_projeto"].count()

        graf_categoria = (
            alt.Chart(dados_categoria)
            .mark_bar(color="#009553")
            .encode(
                y=alt.Y(
                    "numero_projeto:Q",
                    title=None
                ),
                x=alt.X(
                    "categoria:N",
                    sort="-y",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("categoria:N", title="Categoria"),
                    alt.Tooltip("numero_projeto:Q", title="Quantidade")
                ]
            )
        )

        cor_texto = "white" if self.tema == "dark" else "black"

        texto = graf_categoria.mark_text(
            align="center", 
            dy=-5,
            color=cor_texto
        ).encode(
            text=alt.Text(
                "numero_projeto:Q"
            )
        )

        graf_final_categoria = (
            (graf_categoria + texto)
            .properties(
                height=465,
                title="Quantidade de Ações por tipo de Atividade"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_categoria
    

    # -- HISTÓRICO 2 -------------

    def acoes_aporte(self, df):
        financiamento = df.groupby(["data_inicio", "orcamento_consolidado_fundo"], dropna=False, as_index=False).agg(qtd_projetos=('id_projeto', 'count'))
        financiamento["sem_financiamento"] = np.where(financiamento["orcamento_consolidado_fundo"].isna(), financiamento["qtd_projetos"], 1)
        financiamento["com_financiamento"] = np.where(financiamento["orcamento_consolidado_fundo"].notna(), financiamento["qtd_projetos"], None)
        financiamento["ano"] = financiamento["data_inicio"].str[:4]

        df_long = financiamento.melt(
            id_vars="ano",
            value_vars=["com_financiamento", "sem_financiamento"],
            var_name="serie",
            value_name="valor"
        )

        df_long['ano'] = pd.to_datetime(df_long['ano'], format="%Y")
        df_finan = df_long.groupby(["ano", "serie"], as_index=False)["valor"].sum()

        graf = (
            alt.Chart(df_finan)
            .mark_line(point=alt.OverlayMarkDef(
                    color="#EF4136"
                )
            )
            .encode(
                x=alt.X(
                    "ano:T", 
                    title=None
                ),
                y=alt.Y(
                    "valor:Q", 
                    title=None
                ),
                color=alt.Color(
                    "serie:N", 
                    scale=alt.Scale(
                        range=["#b41f1f", "#067722"]
                    ),title="Série"
                ),
                tooltip=[
                    alt.Tooltip("ano:T"),
                    alt.Tooltip("serie:N"),
                    alt.Tooltip("valor:Q")
                ]
            )
            .properties(
                height=300,
                title="Quantidade de Ações por Aporte Financeiro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf
    

    def acoes_tematica(self, df):
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
                    scale=alt.Scale(scheme="greens")
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


    def acoes_centro(self, df):
        df_centro = df[
            [
                'id_projeto', 
                'centro'
            ]
        ]

        df_centro = df_centro.drop_duplicates(subset=['id_projeto'])

        df_acoes_centro = (
            df_centro
            .groupby(df_centro["centro"])
            ["id_projeto"]
            .count()
            .reset_index()
        )

        graf_acoes_centro = (
            alt.Chart(df_acoes_centro)
            .mark_bar(color="#EF4136")
            .encode(
                x=alt.X(
                    "centro:N",
                    sort="-y",  # ordena pela medida do eixo Y em ordem decrescente
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
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

        cor_texto = "white" if self.tema == "dark" else "black"

        texto = graf_acoes_centro.mark_text(
            align="center", 
            dy=-5,
            color=cor_texto
        ).encode(
            text=alt.Text(
                "id_projeto:Q"
            )
        )

        graf_final_acoes = (
            (graf_acoes_centro + texto)
            .properties(
                height=335,
                title="Total de Ações por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_acoes


    # -- PARTICIPANTE 1 ----------

    def discente_ano(self, df):
        df_ano = df[['id_projeto', 'ano_projeto', 'total_discentes_envolvidos']]
        df_ano = df_ano.drop_duplicates(subset=['id_projeto'])
        df_ano = df_ano.drop_duplicates()
        df_ano["total_discentes_envolvidos"] = (
            df_ano["total_discentes_envolvidos"]
            .fillna(0)
            .astype(int)
        )


        df_discentes_ano = df_ano.groupby(["ano_projeto"], as_index=False)["total_discentes_envolvidos"].sum()

        graf_discente_ano = (
            alt.Chart(df_discentes_ano)
            .mark_bar(color="#009553")
            .encode(
                x=alt.X(
                    "ano_projeto:N",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
                    "total_discentes_envolvidos:Q",
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano_projeto:N", title="Ano"),
                    alt.Tooltip("total_discentes_envolvidos:Q", title="Quantidade")
                ],
                order=alt.Order("ano_projeto:N")
            )
        )

        texto = graf_discente_ano.mark_text(
            align="center", dy=-5
        ).encode(
            text=alt.Text(
                "total_discentes_envolvidos:Q"
            )
        )

        graf_final_discente = (
            (graf_discente_ano + texto)
            .properties(
                height=315,
                title="Total de Discentes envolvidos por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_discente
    

    def extensionistas(self, df):
        df_membros = df[['categoria_membro', 'id_projeto']]
        df_membros = df_membros.drop_duplicates()

        qtd_membro = (
            df_membros
            .groupby('categoria_membro', as_index=False)['id_projeto']
            .count()
        )

        total = qtd_membro['id_projeto'].sum()
        qtd_membro['percentual'] = (qtd_membro['id_projeto'] / total)

        base = alt.Chart(qtd_membro)

        # Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
        pizza = base.mark_arc().encode(
            # 'stack=True' garante que as fatias sejam empilhadas proporcionalmente
            theta=alt.Theta("percentual:Q", stack=True),
            color=alt.Color("categoria_membro:N", title="Tipo vínculo"),
            tooltip=[
                alt.Tooltip("categoria_membro:N", title="Tipo vínculo"),
                alt.Tooltip("id_projeto:Q", title="Quantidade"),
                alt.Tooltip("percentual:Q", format=".2%", title="Porcentagem")
            ],
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
        )

        # Texto centralizado nas fatias
        texto = base.mark_text(
            radius=90,  # Distância do centro. Aumente para afastar do meio.
            size=14, 
            fontWeight="bold",
            fill="black" # Ou "white" se a fatia for muito escura
        ).encode(
            # O theta DEVE ser idêntico ao da pizza para o alinhamento funcionar
            theta=alt.Theta("percentual:Q", stack=True),
            text=alt.Text("percentual:Q", format=".2%"), # format=".0f" remove casas decimais
            detail="categoria_membro:N",  # Garante que o texto se alinhe corretamente à fatia
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que os textos sigam a mesma ordem
        )

        graf_membro = (pizza + texto).properties(
            width=315,
            height=315,
            title="Tipo de vínculo do extensionista"
        ).configure_view(
            strokeWidth=0  # Remove a borda externa do gráfico
        ).configure_title(
            fontSize=20
        )

        return graf_membro
    

    def discentes_centro(self, df):
        df_discentes_centro = df[["centro", "total_discentes_envolvidos"]]
        df_discentes_centro = df_discentes_centro.drop_duplicates()
        df_discentes_centro["total_discentes_envolvidos"] = (
            df_discentes_centro["total_discentes_envolvidos"]
            .fillna(0)
            .astype(int)
        )

        df_discentes = df_discentes_centro.groupby(["centro"], as_index=False)["total_discentes_envolvidos"].sum()

        graf_discente = (
            alt.Chart(df_discentes)
            .mark_bar(color="#EF4136")
            .encode(
                y=alt.Y(
                    "centro:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "total_discentes_envolvidos:Q",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Categoria"),
                    alt.Tooltip("total_discentes_envolvidos:Q", title="Quantidade")
                ]
            )
        )

        texto = graf_discente.mark_text(
            align="left",
            dx=5
        ).encode(
            text=alt.Text(
                "total_discentes_envolvidos:Q"
            )
        )

        graf_discente_centro = (
            (graf_discente + texto)
            .properties(
                height=350,
                title="Total de Discentes envolvidos por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_discente_centro
    

    def bolsas(self, df):
        df_bolsa = df[['tipo_bolsa', 'categoria_bolsa']]

        qtd_bolsa = (
            df_bolsa[df_bolsa['tipo_bolsa'].notna()]
            .groupby('tipo_bolsa', as_index=False)['categoria_bolsa']
            .count()
        )

        total = qtd_bolsa['categoria_bolsa'].sum()
        qtd_bolsa['percentual'] = (qtd_bolsa['categoria_bolsa'] / total)

        base = alt.Chart(qtd_bolsa)

        # Ordenar os dados pela categoria ou valor, garantindo que as fatias e textos coincidam
        pizza = base.mark_arc(innerRadius=70).encode(
            # 'stack=True' garante que as fatias sejam empilhadas proporcionalmente
            theta=alt.Theta("percentual:Q", stack=True),
            color=alt.Color("tipo_bolsa:N", title="Tipo bolsa"),
            tooltip=[
                alt.Tooltip("tipo_bolsa:N", title="Tipo bolsa"),
                alt.Tooltip("categoria_bolsa:Q", title="Quantidade"),
                alt.Tooltip("percentual:Q", format=".2%", title="Porcentagem")
            ],
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que as fatias sejam ordenadas
        )

        # Texto centralizado nas fatias
        texto = base.mark_text(
            radius=100,  # Distância do centro. Aumente para afastar do meio.
            size=14, 
            fontWeight="bold",
            fill="black" # Ou "white" se a fatia for muito escura
        ).encode(
            # O theta DEVE ser idêntico ao da pizza para o alinhamento funcionar
            theta=alt.Theta("percentual:Q", stack=True),
            text=alt.Text("percentual:Q", format=".2%"), # format=".0f" remove casas decimais
            detail="tipo_bolsa:N",  # Garante que o texto se alinhe corretamente à fatia
            order=alt.Order("percentual:Q", sort="descending")  # Garantir que os textos sigam a mesma ordem
        )

        graf_bolsa = (pizza + texto).properties(
            width=315,
            height=315,
            title="Tipo de bolsa"
        ).configure_view(
            strokeWidth=0  # Remove a borda externa do gráfico
        ).configure_title(
            fontSize=20
        )

        return graf_bolsa
    

    # -- PARTICIPANTE 2 ----------

    def extencionista_centro(self, df):
        df_extensionistas = df[
            [
                'id_projeto_datageracao', 
                'id_pessoa_membro_datageracao', 
                'categoria_membro', 
                'centro'
            ]
        ]

        df_extensionistas = df_extensionistas.drop_duplicates().dropna()

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

        graf_extensionistas = (
            alt.Chart(df_extensionistas_agrupado)
            .mark_bar(color="#009553")
            .encode(
                y=alt.Y(
                    "centro:N",
                    sort="-x",
                    title="Centro"
                ),
                x=alt.X(
                    "percentual:Q",
                    axis=alt.Axis(
                        format=".2%", 
                        labelAngle=45
                    ),
                    title=None

                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("percentual:Q", title="Percentual", format=".2%"),
                    alt.Tooltip("categoria_membro:Q", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_extensionistas.mark_text(
            align="left",
            dx=5  # deslocamento à direita
        ).encode(
            text=alt.Text(
                "percentual:Q",
                format=".2%"
            )
        )

        graf_final = (
            (graf_extensionistas + texto)
            .properties(
                height=400,
                title="Taxa de extensionistas por centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final
    

    def bolsas_ano(self, df):
        df_bolsas = df[['id_projeto', 'data_inicio', 'bolsas_concedidas']]
        df_bolsas = df_bolsas.drop_duplicates(subset='id_projeto')
        df_bolsas['bolsas_concedidas'] = df_bolsas['bolsas_concedidas'].fillna(0)

        df_bolsas['ano'] = df_bolsas['data_inicio'].astype(str).str[:4]
        df_bolsas['bolsas_concedidas'] = df_bolsas['bolsas_concedidas'].astype(int)

        df_bolsas_agrupadas = (
            df_bolsas.groupby('ano')['bolsas_concedidas']
            .sum()
            .reset_index()
        )

        graf_bolsas = (
            alt.Chart(df_bolsas_agrupadas)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color="#EF4136"
                ),
                color="#EF4136"
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
                    "bolsas_concedidas:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("bolsas_concedidas:Q", title="Quantidade")
                ]
            )
            .properties(
                height=245,
                title="Total de bolsas concedidas por ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_bolsas
    

    def extencionista_area(self, df):
        df_extensionistas_tematico = df[
            [
                'id_projeto_datageracao', 
                'id_pessoa_membro_datageracao', 
                'categoria_membro', 
                'linha_pesquisa_area_tematica'
            ]
        ]

        df_extensionistas_tematico = df_extensionistas_tematico.drop_duplicates().dropna()

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

        graf_extensionistas_tematica = (
            alt.Chart(df_extensionistas_tematico_agrupado)
            .mark_bar(color="#009553")
            .encode(
                y=alt.Y(
                    "linha_pesquisa_area_tematica:N",
                    sort="-x",
                    title=None
                ),
                x=alt.X(
                    "percentual:Q",
                    axis=alt.Axis(
                        format=".2%", 
                        labelAngle=45
                    ),
                    title=None

                ),
                tooltip=[
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
                    alt.Tooltip("percentual:Q", title="Percentual", format=".2%"),
                    alt.Tooltip("categoria_membro:Q", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_extensionistas_tematica.mark_text(
            align="left",
            dx=5  # deslocamento à direita
        ).encode(
            text=alt.Text(
                "percentual:Q",
                format=".2%"
            )
        )

        graf_final_tematica = (
            (graf_extensionistas_tematica + texto)
            .properties(
                height=245,
                title="Taxa de extensionistas por área temática"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final_tematica
    

    # -- ÁREA TEMÁTICA 1 ---------

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
            .sort_values(ascending=False)
            .reset_index()
        )

        fig_radar = px.line_polar(
            df_spider_agrupado,
            r='id_projeto',
            theta='linha_pesquisa_area_tematica',
            line_close=True
        )

        fig_radar.update_layout(
            width=470,
            height=470,
            title="Quantidade de ações por área temática",
            title_font=dict(
                size=20
            ),
            margin=dict(
                b=40,
                l=40,
                r=40
            )
        )

        fig_radar.update_traces(
            fill='toself',
            line=dict(color="#009553"),
            mode='lines+markers',  # <- importante
            marker=dict(size=6),
            hovertemplate=
                "<b>%{theta}</b><br>" +
                "Valor: %{r}<br>" +
                "<extra></extra>"
        )

        return fig_radar
    

    def area_atividade(self, df):
        acoes_tematica_atividade = df[
            [
                'id_projeto',
                'categoria',
                'linha_pesquisa_area_tematica'
            ]
        ]

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
                    title="Área Temática"
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
                height=335,
                title="Ações de extensão por área temática e tipo de atividade de extensão"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_tematica
    

    def categoria_abrangencia(self, df):
        dados_abrangencia = df[
            [
                'abrangencia',
                'categoria',
                'linha_pesquisa_area_tematica'
            ]
        ]

        abrangencia_agrupada = (
            dados_abrangencia
            .groupby(['abrangencia', 'categoria'])['linha_pesquisa_area_tematica']
            .count()
            .reset_index()
        )

        abrangencia_agrupada = abrangencia_agrupada[abrangencia_agrupada['linha_pesquisa_area_tematica'] > 0]

        graf_abrangencia = (
            alt.Chart(abrangencia_agrupada)
            .mark_rect()
            .encode(
                x=alt.X(
                    "abrangencia:N",
                    axis=alt.Axis(labelAngle=45),
                    title=None
                ),
                y=alt.Y(
                    "categoria:N",
                    title="Categoria"
                ),
                color=alt.Color(
                    "linha_pesquisa_area_tematica:Q",
                    title="Quantidade",
                    scale=alt.Scale(scheme="greens"),
                    legend=alt.Legend(
                        format="~s"
                    )
                ),
                tooltip=[
                    alt.Tooltip("abrangencia:N", title="Abrangência"),
                    alt.Tooltip("categoria:N", title="Categoria"),
                    alt.Tooltip("linha_pesquisa_area_tematica:Q", title="Quantidade")
                ]
            )
            .properties(
                height=335,
                title="Ações por abrangência e tipo de atividade de extensão"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_abrangencia
    

    # -- ÁREA TEMÁTICA 2 ---------
    
    def orcamento_area_atividade(self, df):
        orcamento_tematica_atividade = df[
            [
                'orcamento_consolidado_fundo',
                'categoria',
                'linha_pesquisa_area_tematica'
            ]
        ]

        orcamento_tematica_atividade['orcamento_consolidado_fundo'] = (
            orcamento_tematica_atividade['orcamento_consolidado_fundo']
            .astype(float)
        )

        dados_tematica = (
            orcamento_tematica_atividade
            .groupby(['categoria', 'linha_pesquisa_area_tematica'])['orcamento_consolidado_fundo']
            .sum()
            .reset_index()
        )

        dados_tematica['orcamento_consolidado_fundo'] = np.where(dados_tematica['orcamento_consolidado_fundo'] == 0, None, dados_tematica['orcamento_consolidado_fundo'])
        dados_tematica['orcamento_consolidado_fundo'] = dados_tematica["orcamento_consolidado_fundo"].astype(float)

        dados_tematica = self.formatacao.formatar_valor_float(dados_tematica)

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
                    title="Área Temática"
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
                    alt.Tooltip("categoria:N", title="Categoria"),
                    alt.Tooltip("linha_pesquisa_area_tematica:N", title="Área Temática"),
                    alt.Tooltip("valor_formatado:N", title="Valor")
                ]
            )
            .properties(
                height=335,
                title="Orçamento por Área Temática e tipo de Atividade de Extensão"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_tematica
    

    def nuvem_tematica(self, df):
        texto = " ".join(df["palavras_chave"].dropna().astype(str))

        stopwords = STOPWORDS.union({
            "de", "da", "do", "em", "para", "com", "por", "na", "no", "das", "dos", "nos", "nas", "a", "o", "as", "os", "e", "es"
        })

        wordcloud = WordCloud(
            width=1200,
            height=500,
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
    

    def acoes_atuacao(self, df):
        df_atuacoes_acoes = df[["linha_atuacao", "id_projeto"]]
        df_atuacoes_acoes = df_atuacoes_acoes.drop_duplicates()

        df_atuacoes = df_atuacoes_acoes.groupby(["linha_atuacao"], as_index=False)["id_projeto"].count()

        graf_atuacoes = (
            alt.Chart(df_atuacoes)
            .mark_bar(color="#009553")
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
            .properties(
                height=715,
                title="Ações por Linha de Atuação"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_atuacoes


    # -- ORÇAMENTO ---------------

    def orcamento_ano(self, df):
        df_ano = df[['id_projeto', 'data_inicio', 'orcamento_consolidado_fundo']]
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

        return graf_final_orcamento
    

    def orcamento_centro(self, df):
        orcamento_centro = df[
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

        dados_centro = self.formatacao.formatar_valor_float(dados_centro)

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

        return graf_centro
    

    def orcamento_area(self, df):
        df_spider = (
            df[
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

        df_spider_agrupado = self.formatacao.formatar_valor_float(df_spider_agrupado)

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

        return fig_radar
    

    def orcamento_atuacao(self, df):
        df_orcamento_atuacoes = df[["linha_atuacao", "orcamento_consolidado_fundo"]]
        df_orcamento_atuacoes = df_orcamento_atuacoes.drop_duplicates()

        df_orcamento = df_orcamento_atuacoes.groupby(["linha_atuacao"], as_index=False)["orcamento_consolidado_fundo"].sum()

        df_orcamento = self.formatacao.formatar_valor_float(df_orcamento)

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

        return graf_barra_orcamento
    

    def projetos_financiados(self, df):
        df_orcamento = df[
            [
                'id_projeto', 
                'orcamento_consolidado_fundo'
            ]
        ]

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

        return graf_financiamento
    

    # -- UNIDADE DE ENSINO -------

    def acao_centro(self, df):
        df_acao_centro = df[
            [
                "id_projeto", 
                "centro", 
                "data_inicio"
            ]
        ]

        df_acao_centro = df_acao_centro.drop_duplicates(subset="id_projeto")

        df_acao_centro = df_acao_centro.groupby(["centro"], as_index=False)["data_inicio"].count()

        graf_acao_centro = (
            alt.Chart(df_acao_centro)
            .mark_bar(color="#009553")
            .encode(
                y=alt.Y(
                    "centro:N",
                    sort="-x",
                    title=None
                ),

                x=alt.X(
                    "data_inicio:Q",
                    title=None
                ),

                tooltip=[
                    alt.Tooltip(
                        "centro:N",
                        title="Centro"
                    ),

                    alt.Tooltip(
                        "data_inicio:N",
                        title="Quantidade"
                    )
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_acao_centro.mark_text(
            align="left",
            dx=5
        ).encode(
            text=alt.Text(
                "data_inicio:N"
            )
        )

        graf_barra_acao_centro = (
            (graf_acao_centro + texto)
            .properties(
                height=335,
                title="Ações por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_barra_acao_centro
    

    def coordenador_centro(self, df):
        df_coordenador_centro = df[
            [
                'centro', 
                'coordenador'
            ]
        ]

        df_coordenador_centro = df_coordenador_centro.drop_duplicates(subset="coordenador").dropna()

        df_coordenador_centro_agrupado = (
            df_coordenador_centro.groupby(
                [
                    'centro'
                ]
            )['coordenador']
            .count()
            .reset_index()
        )

        total = df_coordenador_centro_agrupado['coordenador'].sum()

        df_coordenador_centro_agrupado['percentual'] = (
            df_coordenador_centro_agrupado['coordenador'] / total
        )

        graf_coordenador_centro = (
            alt.Chart(df_coordenador_centro_agrupado)
            .mark_bar(color="#EF4136")
            .encode(
                y=alt.Y(
                    "centro:N",
                    sort="-x",
                    title="Centro"
                ),
                x=alt.X(
                    "percentual:Q",
                    axis=alt.Axis(
                        format=".2%", 
                        labelAngle=45
                    ),
                    title=None

                ),
                tooltip=[
                    alt.Tooltip("centro:N", title="Centro"),
                    alt.Tooltip("percentual:Q", title="Percentual", format=".2%"),
                    alt.Tooltip("coordenador:Q", title="Quantidade")
                ]
            )
        )

        # camada de texto (percentual no fim da barra)
        texto = graf_coordenador_centro.mark_text(
            align="left",
            dx=5  # deslocamento à direita
        ).encode(
            text=alt.Text(
                "percentual:Q",
                format=".2%"
            )
        )

        graf_final = (
            (graf_coordenador_centro + texto)
            .properties(
                height=335,
                title="Percentual de Coordenador por Centro"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_final

    # -- INICIATIVAS POR CENTRO --

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
            .mark_bar(color="#009553")
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
            dx=5
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
    

    # def acoes_centro(self, df):
    #     ...
    #     df_centro = df[
    #         [
    #             'id_projeto', 
    #             'centro'
    #         ]
    #     ]

    #     df_centro = df_centro.drop_duplicates(subset=['id_projeto'])

    #     df_acoes_centro = (
    #         df_centro
    #         .groupby(df_centro["centro"])
    #         ["id_projeto"]
    #         .count()
    #         .reset_index()
    #     )

    #     graf_acoes_centro = (
    #         alt.Chart(df_acoes_centro)
    #         .mark_bar(color="#EF4136")
    #         .encode(
    #             x=alt.X(
    #                 "centro:N",
    #                 sort="-y",  # ordena pela medida do eixo Y em ordem decrescente
    #                 axis=alt.Axis(labelAngle=45),
    #                 title=None
    #             ),
    #             y=alt.Y(
    #                 "id_projeto:Q",
    #                 title=None
    #             ),
    #             tooltip=[
    #                 alt.Tooltip("centro:N", title="Centro"),
    #                 alt.Tooltip("id_projeto:Q", title="Quantidade")
    #             ],
    #             order=alt.Order("id_projeto:Q")
    #         )
    #     )

    #     cor_texto = "white" if self.tema == "dark" else "black"

    #     texto = graf_acoes_centro.mark_text(
    #         align="center", 
    #         dy=-5,
    #         color=cor_texto
    #     ).encode(
    #         text=alt.Text(
    #             "id_projeto:Q"
    #         )
    #     )

    #     graf_final_acoes = (
    #         (graf_acoes_centro + texto)
    #         .properties(
    #             height=335,
    #             title="Total Ações por Centro"
    #         )
    #         .configure_title(
    #             fontSize=20
    #         )
    #     )

    #     return graf_final_acoes
    

    def participantes_ano(self, df):
        df_participantes = df[
            [
                'id_projeto', 
                'id_pessoa_membro_datageracao', 
                'data_inicio'
            ]
        ]

        df_participantes['ano'] = df_participantes['data_inicio'].astype(str).str[:4]

        df_participantes_agrupadas = (
            df_participantes.groupby('ano')['id_pessoa_membro_datageracao']
            .count()
            .reset_index()
        )

        graf_participantes = (
            alt.Chart(df_participantes_agrupadas)
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
                    "id_pessoa_membro_datageracao:Q", 
                    title=None
                ),
                tooltip=[
                    alt.Tooltip("ano:N", title="Ano"),
                    alt.Tooltip("id_pessoa_membro_datageracao:Q", title="Quantidade")
                ]
            )
            .properties(
                height=335,
                title="Total Participantes por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_participantes
    

    def acoes_ano(self, df):
        df_acoes = df[
            [
                'id_projeto', 
                'data_inicio'
            ]
        ]

        df_acoes = df_acoes.drop_duplicates(subset='id_projeto')

        df_acoes['ano'] = df_acoes['data_inicio'].astype(str).str[:4]

        df_acoes_agrupadas = (
            df_acoes.groupby('ano')['id_projeto']
            .count()
            .reset_index()
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
                    alt.Tooltip("id_projeto:Q", title="Quantidade")
                ]
            )
            .properties(
                height=335,
                title="Ações por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_acoes
    

    def discentes_ano(self, df):
        df_discentes = df[
            [
                'categoria_membro', 
                'data_inicio'
            ]
        ]

        df_discentes = df_discentes[df_discentes['categoria_membro'] == 'DISCENTE']

        df_discentes['ano'] = df_discentes['data_inicio'].astype(str).str[:4]

        df_discentes_agrupadas = (
            df_discentes.groupby('ano')['categoria_membro']
            .count()
            .reset_index()
        )

        graf_discentes = (
            alt.Chart(df_discentes_agrupadas)
            .mark_line(
                point=alt.OverlayMarkDef(
                    color="#EF4136"
                ),
                color="#EF4136"
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
                    alt.Tooltip("categoria_membro:Q", title="Quantidade")
                ]
            )
            .properties(
                height=335,
                title="Total Discentes por Ano"
            )
            .configure_title(
                fontSize=20
            )
        )

        return graf_discentes

    # -- PÚBLICO -----------------

    def estimado_interno(self, df):
        df_interno = df[
            [
                'id_projeto', 
                'publico_estimado_interno', 
                'data_inicio'
            ]
        ]

        df_interno = df_interno.drop_duplicates(subset='id_projeto')

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
                    color="#EF4136"
                ),
                color="#EF4136"
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
        df_externo = df[
            [
                'id_projeto', 
                'publico_estimado_externo', 
                'data_inicio'
            ]
        ]

        df_externo = df_externo.drop_duplicates(subset='id_projeto')

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
        df_atendido = df[
            [
                'id_projeto', 
                'publico_atendido', 
                'data_inicio'
            ]
        ]

        df_atendido = df_atendido.drop_duplicates(subset='id_projeto')

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
                    color="#EF4136"
                ),
                color="#EF4136"
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
    