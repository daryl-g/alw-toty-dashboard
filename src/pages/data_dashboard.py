""" """

# Imports
import streamlit as st
import pandas as pd

# Custom modules
from styles import Styles
from components import title_header
from utils import display_markdown

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Set up page
title_header(
    "Data Dashboard | ALW Recruitment Dashboard",
    "Data Dashboard",
    "",
)
with st.expander("Page description and guides"):
    st.markdown("Nothing here...just yet!")
#     display_markdown("src/assets/texts/squad_depth_desc.md")  # Page description
st.html(
    f"""
    <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 0em;' />
    """
)
