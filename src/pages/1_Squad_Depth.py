"""
View squad depth for all ALW clubs with their players from the 2024-25 season.
- Players are grouped by generic positions.
- Players are sorted by minutes played in descending order.
- Players' contract expiry dates are displayed.
"""

# Imports
import streamlit as st
import pandas as pd

from mplsoccer import Pitch

# Custom modules
from styles import Styles
from components import title_header, dropdown
from utils import display_markdown

# Initialize styles
styles = Styles()
styles.style_init()

# Set up page
st.set_page_config(
    page_title="Squad Depth | ALW Recruitment Dashboard",
    page_icon="⚽",
)
title_header(text_1="2024-25", text_2="Squad Depth")
display_markdown("src/assets/texts/squad_depth_desc.md")  # Page description

# Dropdown
selected_team = dropdown(multiselect=False)
