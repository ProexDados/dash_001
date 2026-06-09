from st_aggrid import GridOptionsBuilder
from st_aggrid import AgGrid
import pandas as pd
from utils.formatacao import Formatacao


class Tabelas:
    def __init__(self):
        self.formatacao = Formatacao()

    
    # -- HISTÓRICO 1 -------------
    def ano_titulo(self, df):
        df_titulos = df[['ano_projeto', 'titulo']]

        df_titulos = df_titulos.sort_values("ano_projeto")

        df_titulos = df_titulos.rename(
            columns={
                "ano_projeto": "Ano Projeto", 
                "titulo": "Título"
            }
        )

        gb = GridOptionsBuilder.from_dataframe(df_titulos)

        gb.configure_column(
            "Ano Projeto",
            width=50
        )

        gb.configure_column(
            "Título",
            width=500
        )

        return AgGrid(
            df_titulos,
            gridOptions=gb.build(),
            height=195,
            width="100%",
            fit_columns_on_grid_load=False,
            theme="streamlit",  # alpine | balham | material
            enable_enterprise_modules=False
        )


    def membro_categoria(self, df):
        df_lista = df[
            [
                "nome_membro", 
                "funcao_membro", 
                "data_inicio_membro", 
                "categoria_membro"
            ]
        ]

        df_lista["data_inicio_membro"] = pd.to_datetime(
            df_lista["data_inicio_membro"],
            errors="coerce"
        )

        df_lista["data_inicio_membro"] = df_lista["data_inicio_membro"].dt.year

        df_lista = df_lista.rename(
            columns={
                "nome_membro": "Nome membro",
                "funcao_membro": "Função membro",
                "data_inicio_membro": "Ano",
                "categoria_membro": "Categoria"
            }
        )

        return df_lista.drop_duplicates().dropna()
    

    def unidades_ensino(self, df):
        df_lista = df[
            [
                "titulo", 
                "coordenador", 
                "orcamento_consolidado_fundo", 
                "data_inicio",
                "unidade_execucao",
                "id_projeto",
                "linha_pesquisa_area_tematica"
            ]
        ]

        df_lista["data_inicio"] = pd.to_datetime(
            df_lista["data_inicio"],
            errors="coerce",
            format="%Y-%m-%d"
        ).dt.strftime("%d/%m/%Y")

        df_lista = self.formatacao.formatar_valor_float(df_lista)

        df_lista = df_lista[
            [
                "titulo",
                "coordenador",
                "valor_formatado",
                "data_inicio",
                "unidade_execucao",
                "id_projeto",
                "linha_pesquisa_area_tematica"
            ]
        ]

        df_lista = df_lista.rename(
            columns={
                "titulo": "Título do Projeto",
                "coordenador": "Coordenador",
                "valor_formatado": "Orçamento Consolidado",
                "data_inicio": "Data de Início",
                "unidade_execucao": "Unidade Execução",
                "id_projeto": "ID Projeto",
                "linha_pesquisa_area_tematica": "Área Temática"
            }
        )

        return df_lista.drop_duplicates().dropna()