# Imports
import streamlit as st

# Custom modules
from styles import Styles
from components import title_header, theme_switcher
from utils import display_markdown

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Set up app header
title_header(
    "A-League Women Recruitment Dashboard",
    "A-League Women",
    "Recruitment Dashboard",
    image_path="src/assets/imgs/ALW_logo.png",
    image_width=90,
)
st.markdown(" ")
theme_switcher()
st.html(
    f"""
    <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 0em;' />
    """
)

with st.expander("Disclaimer and notes"):
    display_markdown("src/assets/texts/title_readme.md")

with st.expander("Known bugs and issues"):
    display_markdown("src/assets/texts/known_bugs.md")
