"""
View squad depth for all ALW clubs with their players from the 2024-25 season.
- Players are grouped by generic positions.
- Players are sorted by minutes played in descending order.
- Players' contract expiry dates are displayed.
"""

# Imports
import streamlit as st
import pandas as pd

from mplsoccer import Pitch, inset_axes
from matplotlib.axes import Axes

# Custom modules
from styles import Styles, get_team_colours
from components import title_header, team_dropdown, get_positions, Download
from utils import *

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Initialise Download class
download: Download = Download(page="Squad Depth")

# Set up page
title_header(
    "Squad Depth | ALW Recruitment Dashboard",
    "2024-25 Squad Depth",
    "",
)
with st.expander("Page description and guides"):
    display_markdown("src/assets/texts/squad_depth_desc.md")  # Page description
st.html(
    f"""
    <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 0em;' />
    """
)

# ----------------------------------------------------------------------------------

# Dropdowns
# Team dropdown
selected_team = team_dropdown(multiselect=False)
## Data selection
data_selection = st.sidebar.radio(
    label="Data to display",
    options=["Playing time", "Contract expiry"],
    index=0,
    captions=[
        "Who played regularly last season?",
        "Whose contract is/was about to end?",
    ],
)
## Sorting method
sort_by = st.sidebar.radio(
    label="Sorting method",
    options=(
        ["Minutes played", "Matches started"]
        if data_selection == "Playing time"
        else ["Minutes played", "Contract expiry"]
    ),
    index=0,
    captions=(
        ["Who played the most minutes?", "Who started the most matches?"]
        if data_selection == "Playing time"
        else ["Who played the most minutes?", "Who was more important last season?"]
    ),
)
## Distribution
distribution = st.sidebar.radio(
    label="Display appearances in",
    options=(
        ["Raw numbers", "Percentage"]
        if data_selection == "Playing time"
        else ["Raw numbers"]
    ),
    index=1 if data_selection == "Playing time" else 0,
    captions=(
        [
            "How many matches did the player start/subbed on/unused?",
            "What is the percentage of matches started/subbed on/unused by the player?",
        ]
        if data_selection == "Playing time"
        else ["How many minutes did the player play last season?"]
    ),
)


# Preparation
## Set up pitch
pitch = Pitch(
    pitch_type="opta",
    pitch_color=palette["bg-color"],
    line_color=palette["line-color"],
    line_alpha=0.3,
)
fig, ax = pitch.draw(figsize=(10, 8))
fig.set_facecolor(palette["bg-color"])

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
    (legend_x - 1 if data_selection == "Contract expiry" else legend_x + 2),
    legend_y + 3,
    (
        "Legend (%)"
        if distribution == "Percentage"
        else "Contract expiry year" if data_selection == "Contract expiry" else "Legend"
    ),
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color=palette["text-color"],
    ha="left",
    va="bottom",
)
### Legend props
ax.scatter(legend_x, legend_y, marker="s", s=100, color=palette["primary-color"])
ax.text(
    legend_x + 1.5,
    legend_y - 1.5,
    "Matches started" if data_selection == "Playing time" else "2025 and before",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color=palette["text-color"],
    ha="left",
    va="bottom",
)
ax.scatter(legend_x, legend_y - 4, marker="s", s=100, color=palette["secondary-color"])
ax.text(
    legend_x + 1.5,
    legend_y - 5.5,
    "Subs appearances" if data_selection == "Playing time" else "2026",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color=palette["text-color"],
    ha="left",
    va="bottom",
)
ax.scatter(legend_x, legend_y - 8, marker="s", s=100, color=palette["third-color"])
ax.text(
    legend_x + 1.5,
    legend_y - 9.5,
    "Unused subs" if data_selection == "Playing time" else "2027 and beyond",
    fontsize=10,
    fontproperties=import_fonts(weight="bold"),
    color=palette["text-color"],
    ha="left",
    va="bottom",
)
if (data_selection == "Contract expiry") and (sort_by == "Minutes played"):
    ax.text(
        1.5,
        95.5,
        "Bar width represents minutes played",
        fontsize=10,
        fontproperties=import_fonts(weight="bold"),
        color=palette["text-color"],
        ha="left",
        va="bottom",
    )

## Plot position nodes
positions: pd.DataFrame = get_positions(_pitch=pitch, _ax=ax, team=selected_team)
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
playing_time: pd.DataFrame = map_player_positions(
    file_name="PlayingTime", position_sort=True
)
selected_squad: pd.DataFrame = playing_time.loc[
    playing_time["Squad"] == get_team_name(selected_team, mode="full")
]

## Get team colours
team_colours: dict = get_team_colours(team=get_team_name(selected_team, mode="short"))

# ----------------------------------------------------------------------------------

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
                (
                    [
                        "Player",
                        "Minutes played",
                        "Matches started",
                        "Subs appearances",
                        "Unused sub",
                    ]
                    if data_selection == "Playing time"
                    else ["Player", "Born", "Minutes played", "Contract expiry"]
                ),
            ]
        )

        # Plot stacked bar chart if there are players in that position
        if not selected_pos.empty:
            if data_selection == "Playing time":
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
                    width=(
                        selected_pos["Matches started (%)"]
                        if distribution == "Percentage"
                        else selected_pos["Matches started"]
                    ),
                    color=palette["primary-color"],
                    height=0.7,
                )
                axes[position].barh(
                    y=range(len(selected_pos)),
                    width=(
                        selected_pos["Subs appearances (%)"]
                        if distribution == "Percentage"
                        else selected_pos["Subs appearances"]
                    ),
                    color=palette["secondary-color"],
                    left=(
                        selected_pos["Matches started (%)"]
                        if distribution == "Percentage"
                        else selected_pos["Matches started"]
                    ),
                    height=0.7,
                )
                axes[position].barh(
                    y=range(len(selected_pos)),
                    width=(
                        selected_pos["Unused sub (%)"]
                        if distribution == "Percentage"
                        else selected_pos["Unused sub"]
                    ),
                    color=palette["third-color"],
                    left=(
                        selected_pos["Matches started (%)"]
                        + selected_pos["Subs appearances (%)"]
                        if distribution == "Percentage"
                        else selected_pos["Matches started"]
                        + selected_pos["Subs appearances"]
                    ),
                    height=0.7,
                )
            elif (data_selection == "Contract expiry") and (
                sort_by == "Minutes played"
            ):
                colours = []
                for expiry_year in selected_pos["Contract expiry"]:
                    if expiry_year >= 2027:
                        colours.append(palette["third-color"])
                    elif expiry_year == 2026:
                        colours.append(palette["secondary-color"])
                    else:
                        colours.append(palette["primary-color"])

                axes[position].barh(
                    y=range(len(selected_pos)),
                    width=(selected_pos["Minutes played"]),
                    color=colours,
                    height=0.7,
                )
            elif (data_selection == "Contract expiry") and (
                sort_by == "Contract expiry"
            ):
                colours = []
                for expiry_year in selected_pos["Contract expiry"]:
                    if expiry_year >= 2027:
                        colours.append(palette["third-color"])
                    elif expiry_year == 2026:
                        colours.append(palette["secondary-color"])
                    else:
                        colours.append(palette["primary-color"])

                axes[position].barh(
                    y=range(len(selected_pos)),
                    width=100,
                    color=colours,
                    height=0.7,
                )

            # Annotations
            # Annotate player names on the bars
            for i in range(len(selected_pos)):
                axes[position].text(
                    x=(
                        0.7
                        if (distribution == "Percentage")
                        else (
                            50
                            if (data_selection == "Contract expiry")
                            and (sort_by == "Contract expiry")
                            else 0.3
                        )
                    ),
                    y=i,
                    s=(
                        f"{selected_pos.loc[i, "Player"]} ({selected_pos.loc[i, "Minutes played"]} mins)"
                        if data_selection == "Playing time"
                        else (
                            f"{selected_pos.loc[i, "Player"]} (born {selected_pos.loc[i, "Born"]})"
                            if (data_selection == "Contract expiry")
                            and (sort_by == "Minutes played")
                            else f"{selected_pos.loc[i, "Player"]}"
                        )
                    ),
                    ha=(
                        "center"
                        if (data_selection == "Contract expiry")
                        and (sort_by == "Contract expiry")
                        else "left"
                    ),
                    va="center",
                    fontsize=7.3,
                    color=palette["text-color"],
                    fontproperties=import_fonts(weight="bold"),
                )

            # Cosmetics
            ## Set axes limits and labels
            axes[position].set_xlim(
                0,
                (
                    100 + 5
                    if (distribution == "Percentage")
                    and (data_selection == "Playing time")
                    else (
                        max(
                            selected_pos["Matches started"]
                            + selected_pos["Subs appearances"]
                            + selected_pos["Unused sub"]
                            + 1
                        )
                        if (distribution == "Raw numbers")
                        and (data_selection == "Playing time")
                        else (
                            100 + 5
                            if (data_selection == "Contract expiry")
                            and (sort_by == "Contract expiry")
                            else max(selected_pos["Minutes played"] + 1)
                        )
                    )
                ),
            )
            axes[position].set_ylim(-0.5, len(selected_pos) - 0.5)

# Plot pitch
st.pyplot(fig)

# Download button
download.squad_depth(figure=fig, selected_team=selected_team)
