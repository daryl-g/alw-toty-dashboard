# Imports
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Custom modules
from styles import Styles
from components import (
    title_header,
    team_dropdown,
    player_dropdown,
    position_dropdown,
    Download,
)
from services import positional_weighting, role_calculator
from utils import display_markdown, map_player_positions, get_team_name, plotly_config

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Initialise the Download class
download: Download = Download(page="Role Ratings")

# Get Plotly plot config
plot_config: dict = plotly_config()

# Set up page
title_header(
    "Role Ratings | ALW Recruitment Dashboard",
    "Role Ratings",
    "",
)
with st.expander("Page description and guides"):
    display_markdown("src/assets/texts/role_ratings_desc.md")  # Page description
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

# Set player position
st.session_state.selected_position = player_position
selected_position: str = position_dropdown(multiselect=False)

# ----------------------------------------------------------------------------------

# Display columns
col1, col2 = st.columns([3, 2], border=True)

# Get the weightings
weightings: dict = positional_weighting(player_position=selected_position)

# Get the role ratings
if mins_played == 0 or played_90s < min_90s:
    pass
else:
    role_ratings: dict = role_calculator(
        selected_player=player_name,
        selected_position=selected_position,
    )

# Role ratings pizza
with col1:
    # Box title
    st.html(
        f"""
        <p style='font-size: 1.5rem; color: {palette["title-color"]}'><b>{player_name}</b> - <b>{selected_team}</b></p>
        <p style='font-size: .9rem; color: {palette["text-color"]}'>Compared against players at <b>{"LW and LM" if selected_position in ["LW", "LM"] else "RW and RM" if selected_position in ["RW", "RM"] else selected_position}</b> with {min_90s} or more 90s.</p>
        <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 1em;' />
        <p style='color: {palette["text-color"]}'>Minutes played: <b>{mins_played} mins</b></p>
        <p style='color: {palette["text-color"]}'>90s: <b>{played_90s} 90s</b></p>
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
        if not role_ratings:
            st.error(
                f"""There was an error calculating the role ratings for {player_name} :disappointed:"""
            )

        download.pizza_baker(
            role_ratings=role_ratings,
            player_name=player_name,
            selected_team=selected_team,
            player_position=(
                "LM and LW"
                if selected_position in ["LM", "LW"]
                else (
                    "RM and RW"
                    if selected_position in ["RM", "RW"]
                    else selected_position
                )
            ),
            min_90s=min_90s,
        )

        # Display the overall rating
        overall_rating: float = role_ratings["Overall"]
        st.html(
            f"""
            <p style='font-size: 1.3rem; text-align: center; color: {palette["title-color"]}'><b>Overall rating: {overall_rating:.1f}/100</b></p>
            """
        )

        # Calculate theta value, width, and offset of the bar
        metrics_groups: list = list(weightings.keys())
        num_stats: int = len(metrics_groups)
        thetas = np.linspace(0, 360, num_stats + 1)
        bar_width = thetas[1] - thetas[0]
        bar_offset = -bar_width / 2

        fig = go.Figure()
        fig.add_trace(
            go.Barpolar(
                r=list(role_ratings[metric] for metric in metrics_groups),
                theta=thetas[:-1],
                width=bar_width,
                offset=0,
                marker_color=palette["primary-color"],
                marker_line_color=palette["border-color"],
                marker_line_width=1,
                opacity=0.8,
                customdata=metrics_groups,
                hovertemplate="<b>%{customdata}</b><br>Rating: %{r}<extra></extra>",
            )
        )
        # Manually add metric labels
        fig.add_trace(
            go.Scatterpolar(
                r=[128] * num_stats,
                theta=thetas[:-1] + bar_width / 2,
                mode="text",
                text=metrics_groups,
                textfont=dict(color=palette["text-color"], size=15),
                hoverinfo="none",
            )
        )

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 130],
                    tickvals=[25, 50, 75, 100],
                    showticklabels=False,
                    showline=False,
                    ticks="",
                    gridcolor="darkgrey",
                ),
                angularaxis=dict(
                    # Set the positions for the labels (metric names)
                    tickvals=thetas,
                    showticklabels=False,
                    showline=False,
                    # Set the positions for the grid lines
                    rotation=90,
                    direction="clockwise",
                ),
                bgcolor=palette["bg-color"],
            ),
            showlegend=False,
            font=dict(family="sans-serif", color=palette["text-color"]),
            paper_bgcolor=palette["bg-color"],
            plot_bgcolor=palette["bg-color"],
            margin=dict(t=5, b=20, l=10, r=10),
            height=500,
        )

        st.plotly_chart(fig, config=plot_config)

# Weightings
with col2:
    st.html(
        f"""
        <p style='font-size: 1.3rem; color: {palette["text-color"]}'><b>Metrics significance</b></p>
        """
    )

    # Display the weighting groups
    for group in weightings:
        with st.expander(label=group):
            st.dataframe(
                data=pd.DataFrame(
                    data=weightings[group].values(),
                    index=weightings[group].keys(),
                    columns=["Significance"],
                )
                .style.background_gradient(cmap="YlGn", low=0.3, high=0.9)
                .format(precision=1),
                column_config=st.column_config.NumberColumn("Significance"),
            )
