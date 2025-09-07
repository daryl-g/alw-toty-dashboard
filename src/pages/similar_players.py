"""
Find similar players based on their stats and percentile ranks.
- Choose a player to see raw percentiles, displayed in Fotmob style.
- Calculate and show similar players with a bar chart in descending order.
"""

# Imports
import streamlit as st
import pandas as pd
import plotly.express as px

# Custom modules
from styles import Styles
from components import title_header, team_dropdown, player_dropdown
from utils import display_markdown, map_player_positions, get_team_name

# Set up page
title_header(
    "Similar Players | ALW Recruitment Dashboard",
    "Similar Players",
    "",
    image_path="src/assets/imgs/ALW_logo.png",
    image_width=75,
)
display_markdown("src/assets/texts/similar_players_desc.md")

# ----------------------------------------------------------------------------------

# Dropdowns
selected_team: str = team_dropdown(multiselect=False)
selected_player: str = player_dropdown(selected_team=selected_team, multiselect=False)

st.markdown("---")

# ----------------------------------------------------------------------------------

# Display columns
col1, col2 = st.columns([3, 2], border=True)

# Raw percentiles
with col1:
    # Box title
    st.markdown(
        f"""
        ### {selected_player.split("(")[0].strip()}
        #### {selected_team}
        <p style='font-size: .9rem;'>Compared against players at <b>{selected_player.split("(")[1].replace(")", "").strip()}</b> with 10 or more 90s.</p>
        """,
        unsafe_allow_html=True,
    )

    ## Potential to utilise cache/session data here?
    playing_time: pd.DataFrame = map_player_positions("PlayingTime")
    player_mins = playing_time.loc[
        (playing_time["Player"] == selected_player.split("(")[0].strip())
        & (playing_time["Squad"] == get_team_name(selected_team, mode="full")),
        ["Minutes played", "90s"],
    ].values[0]

    st.html(
        f"""
        <hr style='border-width: .5px; border-color: {"#00ffff"}; margin-bottom: 1em;' />
        <p>Minutes played: <b>{int(player_mins[0])} mins</b></p>
        <p>90s: <b>{player_mins[1]} 90s</b></p>
        <hr style='border-width: .5px; border-color: {"#00ffff"}; margin-top: 1em;'/>
        """
    )

# Similar players
with col2:
    st.markdown("Bleh")
