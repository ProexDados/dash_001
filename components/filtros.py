import streamlit as st

class Filtros:
    def __init__(self):
        ...

    # -- ANO -------------
    def filtro_ano(self, df, coluna, df_filtrado):
        if "filtro_ano" not in st.session_state:
            st.session_state.filtro_ano = None

        ano_filtro = st.multiselect(
            "Filtrar por Ano:",
            sorted(df[coluna].unique()),
            default=st.session_state.filtro_ano,
        )
        
        if len(ano_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(ano_filtro)]
        
        return df_filtrado
    
    # -- CENTRO ----------
    def filtro_centro(self, df, coluna, df_filtrado):
        if "filtro_centro" not in st.session_state:
            st.session_state.filtro_centro = None

        centro_filtro = st.multiselect(
            "Filtrar por Centro:",
            sorted(df[coluna].dropna().unique()),
            default=st.session_state.filtro_centro
        )

        if len(centro_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(centro_filtro)]
        
        return df_filtrado

    # -- CATEGORIA ---------
    def filtro_categoria(self, df, coluna, df_filtrado):
        if "filtro_categoria" not in st.session_state:
            st.session_state.filtro_categoria = None

        categoria_filtro = st.multiselect(
            "Filtrar por categoria:",
            sorted(df[coluna].unique()),
            default=st.session_state.filtro_categoria
        )

        if len(categoria_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(categoria_filtro)]
        
        return df_filtrado
    
    # -- SITUACAO --------
    def filtro_situacao(self, df, coluna, df_filtrado):
        if "filtro_situacao" not in st.session_state:
            st.session_state.filtro_situacao = None

        situacao_filtro = st.multiselect(
            "Filtrar por situacao:",
            sorted(df[coluna].unique()),
            default=st.session_state.filtro_situacao
        )

        if len(situacao_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(situacao_filtro)]
        
        return df_filtrado

    # -- PARTICIPANTE ----
    def filtro_participante(self, df, coluna, df_filtrado):
        if "filtro_participante" not in st.session_state:
            st.session_state.filtro_participante = None

        categoria_filtro = st.multiselect(
            "Filtrar por participante:",
            sorted(df[coluna].dropna().unique()),
            default=st.session_state.filtro_participante
        )

        if len(categoria_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(categoria_filtro)]
        
        return df_filtrado
    
    # -- TITULO ----------
    def filtro_titulo(self, df, coluna, df_filtrado):
        if "filtro_titulo" not in st.session_state:
            st.session_state.filtro_titulo = None

        titulo_filtro = st.multiselect(
            "Filtrar por Título:",
            sorted(df[coluna].astype(str).unique()),
            default=st.session_state.filtro_titulo,
        )

        if len(titulo_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(titulo_filtro)]
        
        return df_filtrado

    # -- ID PROJETO ------
    def filtro_id_projeto(self, df, coluna, df_filtrado):
        if "filtro_id_projeto" not in st.session_state:
            st.session_state.filtro_id_projeto = None

        id_projeto_filtro = st.multiselect(
            "Filtrar por ID Projeto:",
            sorted(df[coluna].dropna().unique()),
            default=st.session_state.filtro_id_projeto
        )

        if len(id_projeto_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(id_projeto_filtro)]
        
        return df_filtrado

    # -- COORDENADOR -----
    def filtro_coordenador(self, df, coluna, df_filtrado):
        if "filtro_coordenador" not in st.session_state:
            st.session_state.filtro_coordenador = None

        coordenador_filtro = st.multiselect(
            "Filtrar por Coordenador:",
            sorted(df[coluna].dropna().unique()),
            default=st.session_state.filtro_coordenador
        )

        if len(coordenador_filtro) > 0:
            return df_filtrado[df_filtrado[coluna].isin(coordenador_filtro)]
        
        return df_filtrado