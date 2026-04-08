import streamlit as st


class Components:
    def __init__(self):
        ...

    def metric_card(self, label, value, delta, bg_color):
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                height: 200px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            ">
                <p style="color: white; font-weight: bold;">{label}</p>
                <h2 style="color: white;">{value}</h2>
                <p style="color: white;">{delta}</p>
            </div>
            """,
            unsafe_allow_html=True
        )