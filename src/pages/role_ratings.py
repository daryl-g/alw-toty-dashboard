""" """

# Imports
import streamlit as st
import pandas as pd

# Custom modules
from styles import Styles
from components import title_header, team_dropdown, player_dropdown
from services import positional_weighting
from utils import display_markdown, map_player_positions, get_team_name

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Set up page
title_header(
    "Role Ratings | ALW Recruitment Dashboard",
    "Role Ratings",
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

# ----------------------------------------------------------------------------------

# Dropdowns
selected_team: str = team_dropdown(multiselect=False)
selected_player: str = player_dropdown(selected_team=selected_team, multiselect=False)

# Processing data
playing_time: pd.DataFrame = map_player_positions("PlayingTime")
player_mins = playing_time.loc[
    (playing_time["Player"] == selected_player.split("(")[0].strip())
    & (playing_time["Squad"] == get_team_name(selected_team, mode="full")),
    ["Minutes played", "90s"],
].values[0]

# Text elements
player_name: str = selected_player.split("(")[0].strip()
player_position: str = selected_player.split("(")[1].replace(")", "").strip()
mins_played: int = int(player_mins[0])
played_90s: float = player_mins[1]
min_90s: int = 5 if player_position == "GK" else 8

# ----------------------------------------------------------------------------------

# Display columns
col1, col2 = st.columns([3, 2], border=True)

# Role ratings pizza
with col1:
    # Box title
    st.html(
        f"""
        <p style='font-size: 1.5rem; color: {palette["title-color"]}'><b>{player_name}</b> - <b>{selected_team}</b></p>
        <p style='font-size: .9rem;'>Compared against players at <b>{"LW and LM" if player_position in ["LW", "LM"] else "RW and RM" if player_position in ["RW", "RM"] else player_position}</b> with {min_90s} or more 90s.</p>
        <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 1em;' />
        <p>Minutes played: <b>{mins_played} mins</b></p>
        <p>90s: <b>{played_90s} 90s</b></p>
        <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-top: 1em;'/>
        """
    )

    if mins_played == 0:
        st.warning(
            f"""{player_name} did not play last season and has no data available :disappointed:"""
        )
    elif played_90s < min_90s:
        st.warning(
            f"""{player_name} only played {mins_played} minutes last season and did not have enough data for comparison :disappointed:"""
        )
    else:
        pass

# Weightings
with col2:
    st.html(
        """
        <p style='font-size: 1.3rem;'><b>Weighting groups</b></p>
        """
    )

    # Get the weightings
    weightings: dict = positional_weighting(player_position=player_position)

    # Display the weighting groups
    for group in weightings:
        with st.expander(label=group):
            st.table(data=weightings[group])
