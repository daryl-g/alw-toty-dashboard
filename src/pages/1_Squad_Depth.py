"""
View squad depth for all ALW clubs with their players from the 2024-25 season.
- Players are grouped by generic positions.
- Players are sorted by minutes played in descending order.
- Players' contract expiry dates are displayed.
"""

# Imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import Pitch

# Custom modules
from styles import Styles
from components import title_header, dropdown, get_positions
from utils import display_markdown, load_team_logo

# Initialize styles
styles = Styles()
styles.style_init()

# Set up page
st.set_page_config(
    page_title="Squad Depth | ALW Recruitment Dashboard",
    page_icon="⚽",
)
title_header(
    "2024-25",
    "Squad Depth",
    image_path="src/assets/imgs/ALW_logo.png",
    image_width=75,
)
display_markdown("src/assets/texts/squad_depth_desc.md")  # Page description

# Dropdown
selected_team = dropdown(multiselect=False)

with st.spinner("While waiting, remember to hydrate yourself!"):
    # Set up pitch
    pitch = Pitch(pitch_type="opta", pitch_color="#060621", line_color="#c7d5cc")
    fig, axs = pitch.grid(
        grid_width=0.9,
        grid_height=0.9,
        title_height=0,
        endnote_height=0.02,
        figheight=14,
        axis=False,
    )
    fig.set_facecolor("#060621")

    # Load team logo
    pitch.inset_image(
        50,
        50,
        image=load_team_logo(selected_team),
        width=10,
        # height=180,
        alpha=0.2,
        ax=axs["pitch"],
    )

    get_positions(pitch=pitch, ax=axs, team=selected_team)

    # Plot pitch
    st.pyplot(fig)
