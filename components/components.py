import streamlit as st


class Components:
    def __init__(self):
        ...

    def metric_card(self, label, value, delta, height="150px", bg_color=None, font_size="42px"):
        st.markdown(
            f"""
            <div style="
                background-color: {bg_color};
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                height: {height};
                display: flex;
                flex-direction: column;
                justify-content: center;
                gap: 0px;
            ">
                <p style="color: white; font-weight: bold; margin: 0; font-size: 16px;">{label}</p>
                <h1 style="color: white; font-size: {font_size};">{value}</h1>
                <p style="color: white; font-size: 12px;">{delta}</p>
            </div>
            """,
            unsafe_allow_html=True
        )