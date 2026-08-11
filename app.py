"""
Fluid Flow & Heat Transfer Engineering Suite
Main entry point for the Streamlit multi-page app.
"""

import streamlit as st

st.set_page_config(page_title="Fluid Flow & Heat Transfer Suite", layout="wide")

st.title("Fluid Flow & Heat Transfer Engineering Suite")
st.write(
    "A multi-page engineering tool for petroleum engineering coursework, covering:"
)
st.markdown(
    """
    - **Pipe Flow Analyser** — velocity, Reynolds number, friction factor, pressure drop
    - **Heat Transfer Calculator** — conduction and Newton's Law of Cooling
    - **Rock & Fluid Data Dashboard** — upload and explore rock/fluid datasets

    Use the sidebar to navigate between modules.
    """
)