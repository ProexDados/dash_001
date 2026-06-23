from st_aggrid import GridOptionsBuilder
from st_aggrid import AgGrid
import pandas as pd
from utils.formatacao import Formatacao


class Tabelas:
    def __init__(self):
        self.formatacao = Formatacao()

    
    # -- HISTÓRICO ---------------
    def dados_acao(self, df):
        df_tabela = df[
            [
                'titulo', 
                'coordenador', 
                'orcamento_consolidado_fundo', 
                'data_inicio', 
                'centro', 
                'id_projeto', 
                'linha_pesquisa_area_tematica'
            ]
        ]

        df_tabela = df_tabela.drop_duplicates(subset='id_projeto')

        df_tabela['orcamento_consolidado_fundo'] = (
            "R$ " + 
            df_tabela['orcamento_consolidado_fundo']
            .apply(self.formatacao.formatar_valor_float)
        )

        df_tabela = df_tabela.sort_values(by=['data_inicio', 'id_projeto'])

        df_tabela['data_inicio'] = (
            pd.to_datetime(
                df_tabela['data_inicio'],
                format="%Y-%m-%d"
            )
            .dt.strftime("%d/%m/%Y")
        )

        df_tabela = df_tabela.rename(
            columns={
                'titulo': 'Título', 
                'coordenador': 'Coordenador', 
                'orcamento_consolidado_fundo': 'Orçamento',
                'data_inicio': 'Data', 
                'centro': 'Centro', 
                'id_projeto': 'ID Projeto', 
                'linha_pesquisa_area_tematica': 'Área Temática'
            }
        )

        gb = GridOptionsBuilder.from_dataframe(df_tabela)

        gb.configure_column(
            "Título",
            width=600
        )

        gb.configure_column(
            "Centro",
            width=130
        )

        gb.configure_column(
            "Data",
            width=130
        )

        gb.configure_column(
            "ID Projeto",
            width=130
        )

        return AgGrid(
            df_tabela,
            gridOptions=gb.build(),
            height=200,
            width="100%",
            fit_columns_on_grid_load=False,
            theme="streamlit",  # alpine | balham | material
            enable_enterprise_modules=False
        )