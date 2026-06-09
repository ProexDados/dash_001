import streamlit as st


class Titulo:
    def __init__(self):
        self.dark  = "assets/marca_PROEX_2.png"
        self.light = "assets/marca_PROEX.png"
        

    def titulo(self, titulo, tema):
        with st.container():
            col_1, col_2 = st.columns((2, 8))

            with col_1:
                if tema == "dark":
                    st.write("")
                    st.image(self.dark)
                else:
                    st.write("")
                    st.image(self.light)

            with col_2:
                st.title(titulo)