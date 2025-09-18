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
    data_groups: list = []

    if player_position == "GK":
        data_groups = ["Goalkeeping", "Advanced GK", "Distribution (GK)"]

        # Will move this out of the current if condition
        # once the calculation logic is completed
        for group in data_groups:
            data[group] = percentiles_calculator(
                data_group=group,
                selected_player=selected_player,
                selected_team=selected_team,
                player_position=player_position,
            )
    else:
        data_groups = [
            "Shooting",
            "Chance creating",
            "Distributing",
            "Possession",
            "Defending",
            "Discipline",
        ]

    return data


# Percentiles calculation logic
def percentiles_calculator(
    data_group: str, selected_player: str, selected_team: str, player_position: str
) -> dict:
    """
    Main repetitive logic to calculate the percentiles.

    Args:
        data_group (str): Data group to identify the calculation logic.
        selected_player (str): User selected player from the Dropdown option.
        selected_team (str): Only for filtering purpose if there are two players with the same name.
        player_position (str): Selected player's position.

    Returns:
        (dict): Dictionary of per 90 stats and percentiles.
    """
    info_cols: list = ["Player", "Squad", "Minutes played", "90s"]

    min_90s: int = 0
    if player_position == "GK":
        min_90s = 5
    else:
        min_90s = 8

    file_path: str = "data/"
    if data_group == "Goalkeeping":
        file_path += "Goalkeeping.csv"
    elif data_group == "Advanced GK" or data_group == "Distribution (GK)":
        file_path += "AdvancedGK.csv"
    elif data_group == "Shooting":
        file_path += "Shooting.csv"
    # Chance creating (Passing + GCA-SCA)
    # Distributing (Passing + PassTypes)
    elif data_group == "Possession":
        file_path += "Possession.csv"
    # Defending (DefActions + Misc (just for the aerial duels lol))
    elif data_group == "Discipline":
        file_path += "Misc.csv"

    # Load data
    if player_position == "GK":
        data: pd.DataFrame = load_csv(file_path, display=False)
    else:
        if data_group in ["Shooting", "Possession", "Discipline"]:
            data: pd.DataFrame = map_player_positions(file_path.split(".")[0])
        else:
            # Get data from two files and then join them together
            pass
    metrics: list = sorted_metrics(data_group)

    # Get raw per 90s stats
    selected_stats: pd.DataFrame = data.loc[
        ((data["Player"] == selected_player) & (data["Squad"] == selected_team)),
        metrics,
    ]

    # Preprocessing for percentile rank
    if player_position != "GK":
        filtered_stats = data.loc[
            (
                (data["Main Pos"] == player_position)
                | data["Other Pos"].astype(str).str.contains(player_position)
            )
            & (data["90s"] >= min_90s)
        ].reset_index(drop=True)
    else:
        filtered_stats = data.loc[data["90s"] >= min_90s].reset_index(drop=True)
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
    elif data_group == "Shooting":
        return [
            "Goals",
            "Expected Goals",
            "Non-penalty xG",
            "xG overperformance",
            "Shots on Target percentage",
            "npxG per Shot",
            "Penalties scored",
            "Penalties attempted",
        ]
    elif data_group == "Discipline":
        return ["Fouls committed", "Yellow cards", "Red cards"]


# Role standard_percentiles calculator
def role_percentiles():
    pass
