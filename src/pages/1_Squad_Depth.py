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

from mplsoccer import Pitch, inset_axes
from matplotlib.axes import Axes

# Custom modules
from styles import Styles, get_team_colours
from components import title_header, dropdown, get_positions
from utils import *

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

col1, col2 = st.columns([0.5, 0.5])
with col1:
    # Dropdown
    selected_team = dropdown(multiselect=False)
with col2:
    # Sorting method
    sort_by = st.radio(
        label="Sorting method",
        options=["Minutes played", "Matches started"],
        index=0,
        captions=["Who played the most minutes?", "Who started the most matches?"],
    )

# Preparation
## Set up pitch
pitch = Pitch(pitch_type="opta", pitch_color="#060621", line_color="#004687")
fig, ax = pitch.draw(figsize=(10, 8))
fig.set_facecolor("#060621")

## Load team logo
pitch.inset_image(
    50,
    50,
    image=load_team_logo(selected_team),
    width=10,
    # height=180,
    alpha=0.2,
    ax=ax,
)

## Add legend
legend_x = 85
legend_y = 92
### Legend title
ax.text(
    legend_x + 2,
    legend_y + 3,
    "Legend (%)",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color="#ffffff",
    ha="left",
    va="bottom",
)
### Legend props
ax.scatter(legend_x, legend_y, marker="s", s=100, color="#ff4499")
ax.text(
    legend_x + 1.5,
    legend_y - 1.5,
    "Matches started",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color="#ffffff",
    ha="left",
    va="bottom",
)
ax.scatter(legend_x, legend_y - 4, marker="s", s=100, color="#4499ff")
ax.text(
    legend_x + 1.5,
    legend_y - 5.5,
    "Subs appearances",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color="#ffffff",
    ha="left",
    va="bottom",
)
ax.scatter(legend_x, legend_y - 8, marker="s", s=100, color="#3d3076")
ax.text(
    legend_x + 1.5,
    legend_y - 9.5,
    "Unused subs",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color="#ffffff",
    ha="left",
    va="bottom",
)

## Plot position nodes
positions: pd.DataFrame = get_positions(pitch=pitch, ax=ax, team=selected_team)
## Create inset axis for each position
axes: dict[Axes] = {}
for position in positions.index:
    axes[position] = inset_axes(
        x=positions.loc[position, "x"],
        y=positions.loc[position, "y"] - 9,
        width=15,
        height=13,
        ax=ax,
    )

    # Axes cosmetics
    ## Turn off spines
    for spine in axes[position].spines.values():
        spine.set_visible(False)

    ## Turn off x-axis
    axes[position].xaxis.set_visible(False)
    axes[position].yaxis.set_visible(False)

    ## Remove background color
    axes[position].set_facecolor("none")

## Load data
playing_time: pd.DataFrame = map_player_positions(file_name="PlayingTime")
selected_squad: pd.DataFrame = (
    playing_time.loc[playing_time["Squad"] == get_team_name(selected_team, mode="full")]
    .sort_values(by="Main Pos")
    .reset_index(drop=True)
)

## Get team colours
team_colours: dict = get_team_colours(team=get_team_name(selected_team, mode="short"))

with st.spinner("While waiting, remember to hydrate yourself!"):
    for position in positions.index:
        # Get the players with the corresponding main position
        # and retain the relevant columns
        selected_pos: pd.DataFrame = (
            selected_squad.loc[selected_squad["Main Pos"] == position]
            .rename(columns={"Starts": "Matches started"})
            .sort_values(by=sort_by)
            .reset_index(drop=True)
            .loc[
                :,
                [
                    "Player",
                    "Minutes played",
                    "Matches started",
                    "Subs appearances",
                    "Unused sub",
                ],
            ]
        )

        # Plot stacked bar chart if there are players in that position
        if not selected_pos.empty:
            selected_pos["Total"] = (
                selected_pos["Matches started"]
                + selected_pos["Subs appearances"]
                + selected_pos["Unused sub"]
            )
            selected_pos["Matches started (%)"] = (
                selected_pos["Matches started"] / selected_pos["Total"] * 100
            )
            selected_pos["Subs appearances (%)"] = (
                selected_pos["Subs appearances"] / selected_pos["Total"] * 100
            )
            selected_pos["Unused sub (%)"] = (
                selected_pos["Unused sub"] / selected_pos["Total"] * 100
            )

            # Plot stacked bar chart
            axes[position].barh(
                y=range(len(selected_pos)),
                width=selected_pos["Matches started (%)"],
                color="#ff4499",
                height=0.7,
            )
            axes[position].barh(
                y=range(len(selected_pos)),
                width=selected_pos["Subs appearances (%)"],
                color="#4499ff",
                left=selected_pos["Matches started (%)"],
                height=0.7,
            )
            axes[position].barh(
                y=range(len(selected_pos)),
                width=selected_pos["Unused sub (%)"],
                color="#3d3076",
                left=selected_pos["Matches started (%)"]
                + selected_pos["Subs appearances (%)"],
                height=0.7,
            )

            # Annotations
            # Annotate player names on the bars
            for i in range(len(selected_pos)):
                axes[position].text(
                    x=0.7,
                    y=i,
                    s=f"{selected_pos.loc[i, "Player"]} ({selected_pos.loc[i, "Minutes played"]} mins)",
                    ha="left",
                    va="center",
                    fontsize=7.3,
                    color="#ffffff",
                    fontproperties=import_fonts(weight="bold"),
                )

            # Cosmetics
            ## Set axes limits and labels
            axes[position].set_xlim(
                0,
                100 + 5,
            )
            axes[position].set_ylim(-0.5, len(selected_pos) - 0.5)

# Plot pitch
st.pyplot(fig)
