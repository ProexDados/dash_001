import streamlit as st
import altair as alt


# ===============================================
# CONFIGURAÇÃO DA PÁGINA
# ===============================================
alt.themes.enable("dark")

# ===============================================
# NAVEGAÇÃO
# ===============================================
def navegacao():
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"]::before {
            content: "Índice de navegação";
            display: block;
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 10px;
            padding-left: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    page_1 = st.Page("pages/historico_1.py", title="Histórico Geral 1")
    page_2 = st.Page("pages/historico_2.py", title="Histórico Geral 2")
    page_3 = st.Page("pages/participantes_1.py", title="Participantes 1")

    pg = st.navigation([
        page_1,
        page_2,
        page_3
    ],
    position="sidebar")

    pg.run()

if __name__ == "__main__":
    navegacao()


# def metric_card(label, value, delta, bg_color):
#     st.markdown(
#         f"""
#         <div style="
#             background-color: {bg_color};
#             padding: 10px;
#             border-radius: 10px;
#             text-align: center;
#         ">
#             <p style="color: white; font-weight: bold;">{label}</p>
#             <h3 style="color: white;">{value}</h3>
#             <p style="color: white;">{delta}</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# df = pd.DataFrame(
#     {
#         'nome': ['Pedro', 'Ana', 'Caio', 'Bianca', 'José', 'Laura'], 
#         'idade': [25, 22, 33, 27, 14, 10], 
#         'peso': [75.5, 54.3, 97.8, 63.9, 33.5, 30.8], 
#         'altura': [1.75, 1.50, 1.83, 1.65, 1.35, 1.12]
#         }
# )

# df['imc'] = df['peso'] / (df['altura'] * df['altura'])

# st.write("OLÁ!!! TESTE DE DASHBOARD.")

# selecao = alt.selection_point(fields=["nome"], on="click")

# grafico = (
#     alt.Chart(df)
#     .mark_bar()
#     .encode(
#         x="nome:N",
#         y="imc:Q",
#         color=alt.condition(
#             selecao,
#             alt.Color("nome:N"),
#             alt.value("lightgray")
#         )
#     )
#     .add_params(selecao)
# )

# eventos = st.altair_chart(grafico, use_container_width=True)

# pesos_medio = df['peso'].sum() / len(df['peso'])
# alturas_media = df['altura'].sum() / len(df['altura'])
# imc_medio = pesos_medio / (alturas_media * alturas_media)

# with st.container():
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         metric_card("Peso Médio", f"{pesos_medio:.2f}", "", "#2b5797")
#     with col2:
#         metric_card("Altura Média", f"{alturas_media:.2f}", "", "#c00000")
#     with col3:
#         metric_card("IMC Médio", f"{imc_medio:.2f}", "", "#21BDC9")

# with st.container():
#     st.dataframe(df, use_container_width=True, hide_index=True)

# # grafico