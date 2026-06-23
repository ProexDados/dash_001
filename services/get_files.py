import requests as rq
import pandas as pd
import streamlit as st


class Files:
    def __init__(self):
        self.TOKEN_PROJETO = st.secrets["file"]["TOKEN_PROJETO"]
        self.TOKEN_MEMBROS = st.secrets["file"]["TOKEN_MEMBRO"]
        self.URL = st.secrets["file"]["URL"]


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
        df["orcamento_consolidado_fundo"] = df["orcamento_consolidado_fundo"].astype(float)

        df = df[(df['ano_projeto'] > 2016) & (df['ano_projeto'] < 2030)]

        df = df[df["tipo_projeto"] == "EXTENSÃO"]

        return df


    @st.cache_data
    def participantes(_self):
        df_projeto = _self.projeto()
        df_membro  = _self.membro_projeto()

        df_projeto["id_projeto"] = df_projeto["id_projeto"].astype(int)

        df_membro["id_projeto"] = df_membro["id_projeto"].astype(int)

        df_participantes = pd.merge(
            df_projeto, 
            df_membro, 
            on="id_projeto", 
            how="left"
        )

        return df_participantes
