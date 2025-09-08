# Percentile calculator

# Imports
import pandas as pd
import numpy as np

# Custom modules
from utils import load_csv, map_player_positions


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

    data: dict = {}

    if player_position == "GK":
        # Load data
        standard_gk: pd.DataFrame = load_csv("data/Goalkeeping.csv", display=False)
        advanced_gk: pd.DataFrame = load_csv("data/AdvancedGK.csv", display=False)

        # Standard GK stats
        ## Get per 90s stats
        selected_standard: pd.DataFrame = standard_gk.loc[
            (
                (standard_gk["Player"] == selected_player)
                & (standard_gk["Squad"] == selected_team)
            ),
            standard_gk.columns.difference(
                [
                    "Player",
                    "Squad",
                    "Minutes played",
                    "90s",
                    "Clean sheets percentage",
                    "Penalties conceded",
                    "Penalties faced",
                    "Penalties missed by opponent",
                ]
            ),
        ]

        ## Preprocess to calculate percentiles
        filtered_standard = standard_gk.loc[standard_gk["90s"] >= 8].reset_index(
            drop=True
        )
        filtered_info = filtered_standard.loc[
            :,
            [
                "Player",
                "Squad",
                "Minutes played",
                "90s",
            ],
        ]
        filtered_standard = filtered_standard.drop(
            labels=[
                "Player",
                "Squad",
                "Minutes played",
                "90s",
                "Clean sheets percentage",
                "Penalties conceded",
                "Penalties faced",
                "Penalties missed by opponent",
            ],
            axis=1,
        )

        ## Calculate percentiles
        percentiles: pd.DataFrame = filtered_standard.rank(pct=True, na_option="bottom")
        ## Inverse data
        percentiles["Goals conceded"] = 1 - percentiles["Goals conceded"]
        percentiles["Shots on Target conceded"] = (
            1 - percentiles["Shots on Target conceded"]
        )
        ## Convert to 1-100 scale and round up
        percentiles = percentiles * 100
        percentiles = percentiles.round(1)
        ## Add player info
        percentiles["Player"] = filtered_info["Player"]
        percentiles["Squad"] = filtered_info["Squad"]
        percentiles["Minutes played"] = filtered_info["Minutes played"]
        percentiles["90s"] = filtered_info["90s"]

        ## Add data to dictionary
        goalkeeping: dict = {}
        for stat in selected_standard.columns:
            goalkeeping[stat] = (
                selected_standard.loc[:, stat].values[0],
                percentiles.loc[
                    (
                        (percentiles["Player"] == selected_player)
                        & (percentiles["Squad"] == selected_team)
                    ),
                    stat,
                ].values[0],
            )
        data["Goalkeeping"] = goalkeeping

    return data


# Role percentiles calculator
def role_percentiles():
    pass
