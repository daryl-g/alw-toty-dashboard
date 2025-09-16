# Percentile calculator

# Imports
import pandas as pd
import numpy as np

# Custom modules
from utils import load_csv, map_player_positions, get_team_name


# Stats percentiles calculator
def stats_percentiles(
    selected_player: str, selected_team: str, player_position: str
) -> dict:
    """
    Calculate percentile ranks from player Opta's stats.

    Args:
        selected_player (str): User selected player from the Dropdown option.
        selected_team (str): Only for filtering purpose if there are two players with the same name.
        player_position (str): Selected player's position.

    Returns:
        (dict): Dictionary storing all per 90s stats and percentile ranks.
    """
    if selected_player is None:
        raise ValueError(
            "No player is selected. Please select a player from the dropdown."
        )
    elif selected_team is None:
        raise ValueError("No team is selected. Please select a team from the dropdown.")
    elif player_position is None:
        raise ValueError(
            f"No position is detected for {selected_player}. Please double check the input data."
        )

    # Convert team name to Opta/FBRef's team name
    selected_team = get_team_name(selected_team, mode="full")

    data: dict = {}

    if player_position == "GK":
        data_groups = ["Goalkeeping", "Advanced GK", "Distribution (GK)"]

        for group in data_groups:
            data[group] = percentiles_calculator(
                data_group=group,
                selected_player=selected_player,
                selected_team=selected_team,
            )

    return data


# Percentiles calculation logic
def percentiles_calculator(
    data_group: str, selected_player: str, selected_team: str
) -> dict:
    """
    Main repetitive logic to calculate the percentiles.

    Args:
        data_group (str): Data group to identify the calculation logic.
        selected_player (str): User selected player from the Dropdown option.
        selected_team (str): Only for filtering purpose if there are two players with the same name.

    Returns:
        (dict): Dictionary of per 90 stats and percentiles.
    """
    info_cols: list = ["Player", "Squad", "Minutes played", "90s"]

    file_path: str = "data/"
    if data_group == "Goalkeeping":
        file_path += "Goalkeeping.csv"
    elif data_group == "Advanced GK" or data_group == "Distribution (GK)":
        file_path += "AdvancedGK.csv"

    # Load data
    data: pd.DataFrame = load_csv(file_path, display=False)
    metrics: list = sorted_metrics(data_group)

    # Get raw per 90s stats
    selected_stats: pd.DataFrame = data.loc[
        ((data["Player"] == selected_player) & (data["Squad"] == selected_team)),
        metrics,
    ]

    # Preprocessing for percentile rank
    filtered_stats = data.loc[data["90s"] >= 8].reset_index(drop=True)
    filtered_info = filtered_stats.loc[
        :,
        (
            [col for col in info_cols if col != "Minutes played"]
            if "Minutes played" not in data.columns
            else info_cols
        ),
    ]
    filtered_stats = filtered_stats.loc[:, metrics]

    # Calculate percentiles
    percentiles: pd.DataFrame = filtered_stats.rank(pct=True, na_option="bottom")

    # Inverse data
    if data_group == "Goalkeeping":
        percentiles["Goals conceded"] = 1 - percentiles["Goals conceded"]
        percentiles["Shots on Target conceded"] = (
            1 - percentiles["Shots on Target conceded"]
        )

    # Convert to 1-100 scale and round up
    percentiles = (percentiles * 100).round(1)
    # Add player info
    for col in (
        [col for col in info_cols if col != "Minutes played"]
        if "Minutes played" not in data.columns
        else info_cols
    ):
        percentiles[col] = filtered_info[col]

    # Add data to dictionary
    stats: dict = {}
    for stat in selected_stats.columns:
        stats[stat] = (
            selected_stats.loc[:, stat].values[0],
            percentiles.loc[
                (
                    (percentiles["Player"] == selected_player)
                    & (percentiles["Squad"] == selected_team)
                ),
                stat,
            ].values[0],
        )

    return stats


# Sorted metrics
def sorted_metrics(data_group: str) -> list:
    """
    Get a list of sorted metrics for display on the Plotly viz.

    Args:
        data_group (str): Data group to get the sorted list.

    Returns:
        (list): List of data metrics sorted in order.
    """
    if data_group == "Goalkeeping":
        return [
            "Clean sheets",
            "Goals conceded",
            "Shots on Target conceded",
            "Saves",
            "Save percentage",
            "Penalties saved",
            "Penalties save percentage",
        ]
    elif data_group == "Advanced GK":
        return [
            "Post-shot xG",
            "PSxG difference",
            "Crosses faced",
            "Cross stopped percentage",
            "Out-of-box defensive actions",
            "Average OPA distance",
        ]
    elif data_group == "Distribution (GK)":
        return [
            "Passes attempted",
            "Launch percentage",
            "Launched goal kicks percentage",
            "Launches attempted",
            "Launches completion percentage",
            "Throws attempted",
        ]


# Role standard_percentiles calculator
def role_percentiles():
    pass
