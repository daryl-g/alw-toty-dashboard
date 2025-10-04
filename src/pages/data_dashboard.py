""" """

# Imports
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Custom modules
from styles import Styles
from components import title_header, team_dropdown, player_dropdown
from services import scatter_data, role_calculator, positional_weighting
from utils import display_markdown, map_player_positions, get_team_name, plotly_config

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Get Plotly plot config
plot_config: dict = plotly_config()

# Set up page
title_header(
    "Data Dashboard | ALW Recruitment Dashboard",
    "Data Dashboard",
    "",
)
with st.expander("Page description and guides"):
    display_markdown("src/assets/texts/data_dashboard_desc.md")  # Page description
st.html(
    f"""
    <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 0em;' />
    """
)

# ----------------------------------------------------------------------------------

# Widgets
selected_team: str = team_dropdown(multiselect=False)
selected_player: str = player_dropdown(selected_team=selected_team, multiselect=False)

# Processing data
playing_time: pd.DataFrame = map_player_positions("PlayingTime")
player_mins = playing_time.loc[
    (playing_time["Player"] == selected_player.split("(")[0].strip())
    & (playing_time["Squad"] == get_team_name(selected_team, mode="full")),
    ["Minutes played", "90s"],
].values[0]

# ----------------------------------------------------------------------------------

# Set up grid
row1 = st.columns(3)
row2 = st.columns(3)

containers: list = []
for col in row1 + row2:
    tile = col.container(border=True, height="stretch")
    containers.append(tile)

figs: list[go.Figure] = [go.Figure() for _ in range(5)]

# Text elements
player_name: str = selected_player.split("(")[0].strip()
player_position: str = selected_player.split("(")[1].replace(")", "").strip()
mins_played: int = int(player_mins[0])
played_90s: float = player_mins[1]
min_90s: int = 5 if player_position == "GK" else 8

# ----------------------------------------------------------------------------------

# Get the weightings
weightings: dict = positional_weighting(player_position=player_position)

# Get the role ratings
if mins_played == 0 or played_90s < min_90s:
    pass
else:
    role_ratings: dict = role_calculator(
        selected_player=player_name,
        selected_position=player_position,
    )
    overall_ratings: dict = role_calculator(
        selected_player=player_name,
        selected_position=player_position,
        get_all=True,
    )

# Player info
with containers[0]:
    # Box title
    st.html(
        f"""
        <p style='font-size: 1.4rem; color: {palette["title-color"]}'><b>{selected_player}</b></p>
        <p style='font-size: 1.1rem; color: {palette["title-color"]}'><b>{selected_team}</b></p>
        <hr style='border-width: .5px; border-color: {palette["border-color"]}; margin-bottom: 1em;' />
        <p style='font-size: .9rem; color: {palette["title-color"]}'>Compared against players at <b>{"LW and LM" if player_position in ["LW", "LM"] else "RW and RM" if player_position in ["RW", "RM"] else player_position}</b> with {min_90s} or more 90s.</p>
        <p style='color: {palette["title-color"]}'>Minutes played: <b>{mins_played} mins</b></p>
        <p style='color: {palette["title-color"]}'>90s: <b>{played_90s} 90s</b></p>
        """
    )

# Ratings
with containers[1]:
    if mins_played == 0:
        st.warning(
            f"""{player_name} did not play last season and has no data available :disappointed:"""
        )
    elif played_90s < min_90s:
        st.warning(
            f"""{player_name} only played {mins_played} minutes last season and did not have enough data for comparison :disappointed:"""
        )
    else:
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
                marker_color="#1DB954",
                marker_line_color="white",
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
                textfont=dict(color="white", size=10),
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
            margin=dict(t=10, b=10, l=0, r=0),
            height=300,
        )

        figs[0] = fig
        st.plotly_chart(figs[0], config=plot_config)

# Beeswarm plot
with containers[2]:
    if mins_played == 0:
        st.warning(
            f"""{player_name} did not play last season and has no data available :disappointed:"""
        )
    elif played_90s < min_90s:
        st.warning(
            f"""{player_name} only played {mins_played} minutes last season and did not have enough data for comparison :disappointed:"""
        )
    else:
        jitter_amount = 1
        adjusted_x_positions = np.random.uniform(
            -jitter_amount, jitter_amount, size=len(overall_ratings)
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=[
                    overall_ratings[player] + adjusted_x_positions[i]
                    for i, player in enumerate(overall_ratings)
                ],
                y=[0] * len(overall_ratings),
                mode="markers",
                text=[
                    f"{player}: {round(overall_ratings[player], 1)}"
                    for player in overall_ratings
                ],
                marker=dict(color=palette["secondary-color"]),
                name="",
                hovertemplate="%{text}",
            )
        )
        # Highlight the selected player
        fig.add_trace(
            go.Scatter(
                x=[
                    overall_ratings[player] + adjusted_x_positions[i]
                    for i, player in enumerate(overall_ratings)
                ],
                y=[0],
                mode="markers",
                marker=dict(color=palette["primary-color"], size=10),
                text=[f"{player_name}: {round(overall_ratings[player_name], 1)}"],
                name="",
                hovertemplate="%{text}",
            )
        )

        fig.update_layout(
            xaxis=dict(title=dict(text="Overall role rating", font=dict(size=12))),
            yaxis=dict(range=[-0.2, 0.2], showticklabels=False),
            showlegend=False,
            font=dict(family="sans-serif", size=25, color=palette["text-color"]),
            paper_bgcolor=palette["bg-color"],
            plot_bgcolor=palette["bg-color"],
            margin=dict(t=10, b=10),
            height=300,
        )

        figs[1] = fig
        st.plotly_chart(figs[1], config=plot_config)

# Scatter plots
with containers[3]:
    if mins_played == 0:
        st.warning(
            f"""{player_name} did not play last season and has no data available :disappointed:"""
        )
    elif played_90s < min_90s:
        st.warning(
            f"""{player_name} only played {mins_played} minutes last season and did not have enough data for comparison :disappointed:"""
        )
    else:
        data_group: str = "Attacking" if player_position != "GK" else "Basic GK"
        # Metrics selection
        dropdown_container = st.container(
            horizontal=False, horizontal_alignment="right"
        )
        dropdown_popover = dropdown_container.popover("Select metrics", disabled=False)
        metrics_selection: list = dropdown_popover.multiselect(
            label=(
                "Attacking metrics" if player_position != "GK" else "Basic GK metrics"
            ),
            options=(
                [
                    "Goals",
                    "Shots on Target percentage",
                    "Goals per Shot",
                    "Non-penalty xG",
                    "npxG per Shot",
                    "xG overperformance",
                ]
                if player_position != "GK"
                else [
                    "Goals conceded",
                    "Shots on Target conceded",
                    "Saves",
                    "Save percentage",
                    "Penalties saved",
                    "Penalties save percentage",
                ]
            ),
            default=(
                ["Goals", "Non-penalty xG"]
                if player_position != "GK"
                else ["Shots on Target conceded", "Save percentage"]
            ),
            max_selections=2,
        )

        if len(metrics_selection) < 2:
            st.error(
                f"Please choose {2 - len(metrics_selection)} more metrics to create the scatter plot."
            )
        else:
            # Get data
            data: pd.DataFrame = scatter_data(
                data_group=data_group,
                metrics=metrics_selection,
                player_position=player_position,
                min_90s=min_90s,
            )

            # Plot the data
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=data.loc[:, metrics_selection[0]],
                    y=data.loc[:, metrics_selection[1]],
                    mode="markers",
                    text=data.loc[:, "Player"],
                    marker=dict(color=palette["secondary-color"]),
                    name="",
                    hovertemplate="%{text}: (%{x} "
                    + metrics_selection[0].lower()
                    + ", %{y} "
                    + metrics_selection[1].lower()
                    + ")",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=data.loc[data["Player"] == player_name, metrics_selection[0]],
                    y=data.loc[data["Player"] == player_name, metrics_selection[1]],
                    mode="markers",
                    marker=dict(color=palette["primary-color"], size=10),
                    text=player_name,
                    name="",
                    hovertemplate=player_name
                    + ": (%{x} "
                    + metrics_selection[0].lower()
                    + ", %{y} "
                    + metrics_selection[1].lower()
                    + ")",
                )
            )
            ## Average lines
            # fig.add_trace(
            #     go.Scatter(
            #         x=[
            #             data.loc[:, metrics_selection[0]].mean()
            #             for _ in range(len(data))
            #         ],
            #         y=[
            #             (
            #                 0
            #                 if data.loc[:, metrics_selection[1]].min() >= 0
            #                 else data.loc[:, metrics_selection[1]].min() - 0.2
            #             ),
            #             data.loc[:, metrics_selection[1]].max() + 0.5,
            #         ],
            #         mode="lines",
            #         line=dict(color=palette["line-color"], dash="dash", width=2),
            #     )
            # )
            # fig.add_trace(
            #     go.Scatter(
            #         y=[
            #             data.loc[:, metrics_selection[1]].mean()
            #             for _ in range(len(data))
            #         ],
            #         x=[
            #             (
            #                 0
            #                 if data.loc[:, metrics_selection[0]].min() >= 0
            #                 else data.loc[:, metrics_selection[0]].min() - 0.2
            #             ),
            #             data.loc[:, metrics_selection[0]].max() + 0.5,
            #         ],
            #         mode="lines",
            #         line=dict(color=palette["line-color"], dash="dash", width=2),
            #     )
            # )

            fig.update_layout(
                title=dict(
                    text=data_group,
                    font=dict(family="sans-serif", color=palette["text-color"]),
                ),
                xaxis=dict(title=dict(text=metrics_selection[0], font=dict(size=12))),
                yaxis=dict(title=dict(text=metrics_selection[1], font=dict(size=12))),
                showlegend=False,
                font=dict(family="sans-serif", size=25, color=palette["text-color"]),
                paper_bgcolor=palette["bg-color"],
                plot_bgcolor=palette["bg-color"],
                margin=dict(t=30, b=10),
                height=300,
            )

            figs[2] = fig
            st.plotly_chart(figs[2], config=plot_config)

with containers[4]:
    if mins_played == 0:
        st.warning(
            f"""{player_name} did not play last season and has no data available :disappointed:"""
        )
    elif played_90s < min_90s:
        st.warning(
            f"""{player_name} only played {mins_played} minutes last season and did not have enough data for comparison :disappointed:"""
        )
    else:
        data_group: str = "Passing" if player_position != "GK" else "Advanced GK"
        # Metrics selection
        dropdown_container = st.container(
            horizontal=False, horizontal_alignment="right"
        )
        dropdown_popover = dropdown_container.popover("Select metrics", disabled=False)
        metrics_selection: list = dropdown_popover.multiselect(
            label=(
                "Passing metrics" if player_position != "GK" else "Advanced GK metrics"
            ),
            options=(
                [
                    "Shot-creating Actions",
                    "Goal-creating Actions",
                    "Passes attempted",
                    "Assists",
                    "Expected Assists",
                    "Assist overperformance",
                    "Key passes",
                    "Passes into final third",
                    "Passes into penalty box",
                    "Crosses into Penalty Area",
                    "Progressive passes",
                    "Through balls",
                    "Switch-plays",
                ]
                if player_position != "GK"
                else [
                    "Post-shot xG",
                    "PSxG difference",
                    "Crosses faced",
                    "Cross stopped percentage",
                    "Out-of-box defensive actions",
                    "Average OPA distance",
                ]
            ),
            default=(
                ["Assists", "Assist overperformance"]
                if player_position != "GK"
                else ["Post-shot xG", "PSxG difference"]
            ),
            max_selections=2,
        )

        if len(metrics_selection) < 2:
            st.error(
                f"Please choose {2 - len(metrics_selection)} more metrics to create the scatter plot."
            )
        else:
            # Get data
            data: pd.DataFrame = scatter_data(
                data_group=data_group,
                metrics=metrics_selection,
                player_position=player_position,
                min_90s=min_90s,
            )

            # Plot the data
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=data.loc[:, metrics_selection[0]],
                    y=data.loc[:, metrics_selection[1]],
                    mode="markers",
                    text=data.loc[:, "Player"],
                    marker=dict(color=palette["secondary-color"]),
                    name="",
                    hovertemplate="%{text}: (%{x} "
                    + metrics_selection[0].lower()
                    + ", %{y} "
                    + metrics_selection[1].lower()
                    + ")",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=data.loc[data["Player"] == player_name, metrics_selection[0]],
                    y=data.loc[data["Player"] == player_name, metrics_selection[1]],
                    mode="markers",
                    marker=dict(color=palette["primary-color"], size=10),
                    text=player_name,
                    name="",
                    hovertemplate=player_name
                    + ": (%{x} "
                    + metrics_selection[0].lower()
                    + ", %{y} "
                    + metrics_selection[1].lower()
                    + ")",
                )
            )
            ## Average lines
            # fig.add_trace(
            #     go.Scatter(
            #         x=[
            #             data.loc[:, metrics_selection[0]].mean()
            #             for _ in range(len(data))
            #         ],
            #         y=[
            #             (
            #                 0
            #                 if data.loc[:, metrics_selection[1]].min() >= 0
            #                 else data.loc[:, metrics_selection[1]].min() - 0.2
            #             ),
            #             data.loc[:, metrics_selection[1]].max() + 0.5,
            #         ],
            #         mode="lines",
            #         line=dict(color=palette["line-color"], dash="dash", width=2),
            #     )
            # )
            # fig.add_trace(
            #     go.Scatter(
            #         y=[
            #             data.loc[:, metrics_selection[1]].mean()
            #             for _ in range(len(data))
            #         ],
            #         x=[
            #             (
            #                 0
            #                 if data.loc[:, metrics_selection[0]].min() >= 0
            #                 else data.loc[:, metrics_selection[0]].min() - 0.2
            #             ),
            #             data.loc[:, metrics_selection[0]].max() + 0.5,
            #         ],
            #         mode="lines",
            #         line=dict(color=palette["line-color"], dash="dash", width=2),
            #     )
            # )

            fig.update_layout(
                title=dict(
                    text=data_group,
                    font=dict(family="sans-serif", color=palette["text-color"]),
                ),
                xaxis=dict(title=dict(text=metrics_selection[0], font=dict(size=12))),
                yaxis=dict(title=dict(text=metrics_selection[1], font=dict(size=12))),
                showlegend=False,
                font=dict(family="sans-serif", size=25, color=palette["text-color"]),
                paper_bgcolor=palette["bg-color"],
                plot_bgcolor=palette["bg-color"],
                margin=dict(t=30, b=10),
                height=300,
            )

            figs[3] = fig
            st.plotly_chart(figs[3], config=plot_config)

with containers[5]:
    if mins_played == 0:
        st.warning(
            f"""{player_name} did not play last season and has no data available :disappointed:"""
        )
    elif played_90s < min_90s:
        st.warning(
            f"""{player_name} only played {mins_played} minutes last season and did not have enough data for comparison :disappointed:"""
        )
    else:
        data_group: str = "Defending" if player_position != "GK" else "Distributing"
        # Metrics selection
        dropdown_container = st.container(
            horizontal=False, horizontal_alignment="right"
        )
        dropdown_popover = dropdown_container.popover("Select metrics", disabled=False)
        metrics_selection: list = dropdown_popover.multiselect(
            label=(
                "Defending metrics"
                if player_position != "GK"
                else "Distributing metrics"
            ),
            options=(
                [
                    "Tackles attempted",
                    "Tackles in defensive third",
                    "Tackles in middle third",
                    "Tackles in attacking third",
                    "Dribbles tackled",
                    "Blocks attempted",
                    "Interceptions",
                    "Clearances",
                    "Errors",
                ]
                if player_position != "GK"
                else [
                    "Passes attempted",
                    "Average pass length",
                    "Throws attempted",
                    "Launch percentage",
                    "Launched goal kicks percentage",
                    "Average goal kick length",
                ]
            ),
            default=(
                ["Tackles attempted", "Interceptions"]
                if player_position != "GK"
                else ["Launched goal kicks percentage", "Average goal kick length"]
            ),
            max_selections=2,
        )

        if len(metrics_selection) < 2:
            st.error(
                f"Please choose {2 - len(metrics_selection)} more metrics to create the scatter plot."
            )
        else:
            # Get data
            data: pd.DataFrame = scatter_data(
                data_group=data_group,
                metrics=metrics_selection,
                player_position=player_position,
                min_90s=min_90s,
            )

            # Plot the data
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=data.loc[:, metrics_selection[0]],
                    y=data.loc[:, metrics_selection[1]],
                    mode="markers",
                    text=data.loc[:, "Player"],
                    marker=dict(color=palette["secondary-color"]),
                    name="",
                    hovertemplate="%{text}: (%{x} "
                    + metrics_selection[0].lower()
                    + ", %{y} "
                    + metrics_selection[1].lower()
                    + ")",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=data.loc[data["Player"] == player_name, metrics_selection[0]],
                    y=data.loc[data["Player"] == player_name, metrics_selection[1]],
                    mode="markers",
                    marker=dict(color=palette["primary-color"], size=10),
                    text=player_name,
                    name="",
                    hovertemplate=player_name
                    + ": (%{x} "
                    + metrics_selection[0].lower()
                    + ", %{y} "
                    + metrics_selection[1].lower()
                    + ")",
                )
            )
            ## Average lines
            # fig.add_trace(
            #     go.Scatter(
            #         x=[
            #             data.loc[:, metrics_selection[0]].mean()
            #             for _ in range(len(data))
            #         ],
            #         y=[
            #             (
            #                 0
            #                 if data.loc[:, metrics_selection[1]].min() >= 0
            #                 else data.loc[:, metrics_selection[1]].min() - 0.2
            #             ),
            #             data.loc[:, metrics_selection[1]].max() + 0.5,
            #         ],
            #         mode="lines",
            #         line=dict(color=palette["line-color"], dash="dash", width=2),
            #     )
            # )
            # fig.add_trace(
            #     go.Scatter(
            #         y=[
            #             data.loc[:, metrics_selection[1]].mean()
            #             for _ in range(len(data))
            #         ],
            #         x=[
            #             (
            #                 0
            #                 if data.loc[:, metrics_selection[0]].min() >= 0
            #                 else data.loc[:, metrics_selection[0]].min() - 0.2
            #             ),
            #             data.loc[:, metrics_selection[0]].max() + 0.5,
            #         ],
            #         mode="lines",
            #         line=dict(color=palette["line-color"], dash="dash", width=2),
            #     )
            # )

            fig.update_layout(
                title=dict(
                    text=data_group,
                    font=dict(family="sans-serif", color=palette["text-color"]),
                ),
                xaxis=dict(title=dict(text=metrics_selection[0], font=dict(size=12))),
                yaxis=dict(title=dict(text=metrics_selection[1], font=dict(size=12))),
                showlegend=False,
                font=dict(family="sans-serif", size=25, color=palette["text-color"]),
                paper_bgcolor=palette["bg-color"],
                plot_bgcolor=palette["bg-color"],
                margin=dict(t=30, b=10),
                height=300,
            )

            figs[4] = fig
            st.plotly_chart(figs[4], config=plot_config)
