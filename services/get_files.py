import requests as rq
import pandas as pd
import streamlit as st


class Files:
    def __init__(self):
        # self.path = "C:/workspace/01. documentos"
        self.TOKEN_PROJETO = "Bearer a5a9509b2441d3020afa7e55b5eb1494"
        self.TOKEN_MEMBROS = "Bearer b60781fd04476970b424556b23cc80ac"
        self.URL = "https://dados.sistemas.udesc.br/ResourceManager/DataAccessWs/getDataList"

    @st.cache_data
    def membro_projeto(_self):
        headers = {
            "Authorization": f"{_self.TOKEN_MEMBROS}"
        }
        resp = rq.get(_self.URL, headers=headers)

        dados = resp.json()

        return pd.DataFrame(dados['data'])

    @st.cache_data
    def projeto(_self):
        headers = {
            "Authorization": f"{_self.TOKEN_PROJETO}"
        }
        resp = rq.get(_self.URL, headers=headers)

        dados = resp.json()

        df = pd.DataFrame(dados['data'])

        df["ano_projeto"] = df["ano_projeto"].astype(int)

        df = df[(df['ano_projeto'] > 2016) & (df['ano_projeto'] < 2030)]

        return df