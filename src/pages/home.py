# Imports
import streamlit as st

# Custom modules
from styles import Styles
from components import title_header, theme_switcher
from utils import display_markdown

# Custom styling
styles = Styles()
styles.style_init()

# Set up app header
title_header(
    "A-League Women",
    "Recruitment Dashboard",
    image_path="src/assets/imgs/ALW_logo.png",
    image_width=75,
)
st.markdown(" ")
theme_switcher()
st.markdown("---")

display_markdown("src/assets/texts/title_readme.md")
