"""
Find similar players based on their stats and percentile ranks.
- Choose a player to see raw percentiles, displayed in Fotmob style.
- Calculate and show similar players with a bar chart in descending order.
"""

# Imports
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Custom modules
from styles import Styles
from components import title_header, team_dropdown, player_dropdown
from services import stats_percentiles, sorted_metrics, player_similarity
from utils import display_markdown, map_player_positions, get_team_name, plotly_config

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)

# Get Plotly plot config
plot_config: dict = plotly_config()

# Set up page
title_header(
    "Similar Players | ALW Recruitment Dashboard",
    "Similar Players",
    "",
)
with st.expander("Page description and guides"):
    display_markdown("src/assets/texts/similar_players_desc.md")

# ----------------------------------------------------------------------------------

# Dropdowns
selected_team: str = team_dropdown(multiselect=False)
selected_player: str = player_dropdown(selected_team=selected_team, multiselect=False)
min_similarity: int = st.sidebar.select_slider(
    label="Minimum similarity %", options=[i for i in range(0, 105, 5)], value=80
)

# Processing data
playing_time: pd.DataFrame = map_player_positions("PlayingTime")
player_mins = playing_time.loc[
    (playing_time["Player"] == selected_player.split("(")[0].strip())
    & (playing_time["Squad"] == get_team_name(selected_team, mode="full")),
    ["Minutes played", "90s"],
].values[0]

# ----------------------------------------------------------------------------------

# Display columns
col1, col2 = st.columns([3, 2], border=True)

# Raw percentiles
with col1:
    # Text elements
    player_name: str = selected_player.split("(")[0].strip()
    player_position: str = selected_player.split("(")[1].replace(")", "").strip()
    mins_played: int = int(player_mins[0])
    played_90s: float = player_mins[1]
    min_90s: int = 5 if player_position == "GK" else 8

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
        data: dict = stats_percentiles(
            selected_player=player_name,
            selected_team=selected_team,
            player_position=player_position,
        )

        figs: list[go.Figure] = [go.Figure() for _ in range(len(data))]

        for data_group in data.keys():
            # st.html(
            #     f"""
            #     <p style='font-size: 1.2rem; margin-bottom: -1rem; margin-top: -.5rem'><b>{data_group}</b></p>
            #     """
            # )

            # Flatten the dictionary
            raw_stats: list = [value[0] for value in data[data_group].values()]
            percentiles: list = [value[1] for value in data[data_group].values()]
            colours: list = [
                (
                    palette["low-value-color"]
                    if value < 31
                    else (
                        palette["med-value-color"]
                        if value < 81
                        else palette["high-value-color"]
                    )
                )
                for value in percentiles
            ]
            stats_category: list = list(data[data_group].keys())

            fig_counter: int = 0

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=percentiles,
                    y=stats_category,
                    orientation="h",
                    marker=dict(color=colours, cornerradius=30),
                )
            )

            annotations: list = [
                # Per 90s stats title
                dict(
                    xref="x1",
                    yref="y1",
                    y=-1.1,
                    x=-1,
                    text="p90",
                    font=dict(family="sans-serif", size=14, weight="bold"),
                    xanchor="right",
                    showarrow=False,
                ),
                # Percentile ranks title
                dict(
                    xref="x1",
                    yref="y1",
                    y=-1.1,
                    x=60,
                    text="Percentile ranks",
                    font=dict(family="sans-serif", size=14, weight="bold"),
                    xanchor="right",
                    showarrow=False,
                ),
            ]
            for cat, perc, stat in zip(stats_category, percentiles, raw_stats):
                annotations.append(
                    dict(
                        xref="x1",
                        yref="y1",
                        y=cat,
                        x=-1,
                        text=str(stat),
                        font=dict(family="sans-serif", size=12),
                        xanchor="right",
                        showarrow=False,
                    )
                )

            fig.update_layout(
                title=dict(
                    text=(
                        data_group
                        if data_group != "Defending"
                        else "Defending (Possession-adjusted)"
                    ),
                    font=dict(family="sans-serif", color=palette["text-color"]),
                ),
                xaxis=dict(
                    showgrid=False,
                    showline=False,
                    showticklabels=False,
                    zeroline=False,
                    range=[-10, 100],
                ),
                yaxis=dict(
                    showgrid=False,
                    showline=False,
                    zeroline=False,
                    categoryorder="array",
                    categoryarray=sorted_metrics(data_group),
                    autorange="reversed",
                    tickfont=dict(color=palette["text-color"]),
                ),
                font=dict(family="sans-serif", size=35, color=palette["text-color"]),
                annotations=annotations,
                paper_bgcolor=palette["bg-color"],
                plot_bgcolor=palette["bg-color"],
                margin=dict(t=30, b=10),
                height=300,
            )

            figs[fig_counter] = fig
            st.plotly_chart(figs[fig_counter], config=plot_config)
            fig_counter += 1

# Similar players
with col2:
    st.html(
        f"""
        <p>Similar players to <b>{player_name}</b> (Position: <b>{"LW and LM" if player_position in ["LW", "LM"] else "RW and RM" if player_position in ["RW", "RM"] else player_position}</b>)</p>
        <p style='font-size: .9rem;'>(Minimum similarity: {min_similarity}%)</p>
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
        similarity = player_similarity(
            selected_player=player_name,
            selected_team=selected_team,
            player_position=player_position,
        ).loc[lambda x: x >= min_similarity]

        similarity_fig = go.Figure()
        similarity_fig.add_trace(
            go.Bar(
                x=similarity,
                y=similarity.index,
                orientation="h",
                marker=dict(
                    color=similarity,
                    colorscale="RdBu",
                    cornerradius=30,
                ),
            )
        )

        similarity_fig.update_layout(
            xaxis=dict(
                showgrid=True,
                showline=True,
                range=[-1, 105],
                title=dict(text="Similarity Rating (%)"),
            ),
            yaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False,
                autorange="reversed",
                tickfont=dict(color=palette["text-color"]),
            ),
            font=dict(family="sans-serif", size=35, color=palette["text-color"]),
            paper_bgcolor=palette["bg-color"],
            plot_bgcolor=palette["bg-color"],
            margin=dict(t=3),
            height=1500 if player_position != "GK" else 750,
        )

        st.plotly_chart(similarity_fig, config=plot_config)
