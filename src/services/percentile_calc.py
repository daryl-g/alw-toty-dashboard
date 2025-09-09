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
    info_cols: list = ["Player", "Squad", "Minutes played", "90s"]

    if player_position == "GK":
        # Load data
        standard_gk: pd.DataFrame = load_csv("data/Goalkeeping.csv", display=False)
        advanced_gk: pd.DataFrame = load_csv("data/AdvancedGK.csv", display=False)

        # ----------------------------------------------------------------------------------
        # Standard GK stats
        ## Get per 90s stats
        selected_standard: pd.DataFrame = standard_gk.loc[
            (
                (standard_gk["Player"] == selected_player)
                & (standard_gk["Squad"] == selected_team)
            ),
            standard_gk.columns.difference(
                info_cols
                + [
                    "Clean sheets percentage",
                    "Penalties conceded",
                    "Penalties faced",
                    "Penalties missed by opponent",
                ]
            ),
        ]

        ## Preprocess to calculate standard_percentiles
        filtered_standard = standard_gk.loc[standard_gk["90s"] >= 8].reset_index(
            drop=True
        )
        filtered_info = filtered_standard.loc[
            :,
            info_cols,
        ]
        filtered_standard = filtered_standard.drop(
            labels=info_cols
            + [
                "Clean sheets percentage",
                "Penalties conceded",
                "Penalties faced",
                "Penalties missed by opponent",
            ],
            axis=1,
        )

        ## Calculate percentiles
        standard_percentiles: pd.DataFrame = filtered_standard.rank(
            pct=True, na_option="bottom"
        )
        ## Inverse data
        standard_percentiles["Goals conceded"] = (
            1 - standard_percentiles["Goals conceded"]
        )
        standard_percentiles["Shots on Target conceded"] = (
            1 - standard_percentiles["Shots on Target conceded"]
        )
        ## Convert to 1-100 scale and round up
        standard_percentiles = (standard_percentiles * 100).round(1)
        ## Add player info
        for col in info_cols:
            standard_percentiles[col] = filtered_info[col]

        ## Add data to dictionary
        standard_stats: dict = {}
        for stat in selected_standard.columns:
            standard_stats[stat] = (
                selected_standard.loc[:, stat].values[0],
                standard_percentiles.loc[
                    (
                        (standard_percentiles["Player"] == selected_player)
                        & (standard_percentiles["Squad"] == selected_team)
                    ),
                    stat,
                ].values[0],
            )
        # ----------------------------------------------------------------------------------
        ## Same steps so no need to comment here
        advanced_gk_stats = advanced_gk.loc[
            :,
            (
                [col for col in info_cols if col != "Minutes played"]
                if "Minutes played" not in advanced_gk.columns
                else info_cols
            )
            + [
                "Post-shot xG",
                "PSxG difference",
                "Crosses faced",
                "Cross stopped percentage",
                "Out-of-box defensive actions",
                "Average OPA distance",
            ],
        ]
        distribution_gk = advanced_gk.loc[
            :,
            (
                [col for col in info_cols if col != "Minutes played"]
                if "Minutes played" not in advanced_gk.columns
                else info_cols
            )
            + [
                "Passes attempted",
                "Launch percentage",
                "Launched goal kicks percentage",
                "Launches attempted",
                "Launches completion percentage",
                "Throws attempted",
            ],
        ]

        # ----------------------------------------------------------------------------------
        selected_advanced_gk: pd.DataFrame = advanced_gk_stats.loc[
            (
                (advanced_gk_stats["Player"] == selected_player)
                & (advanced_gk_stats["Squad"] == selected_team)
            ),
            advanced_gk_stats.columns.difference(info_cols),
        ]

        selected_distribution_gk: pd.DataFrame = distribution_gk.loc[
            (
                (distribution_gk["Player"] == selected_player)
                & (distribution_gk["Squad"] == selected_team)
            ),
            distribution_gk.columns.difference(info_cols),
        ]

        # ----------------------------------------------------------------------------------
        filtered_advanced = advanced_gk_stats.loc[
            advanced_gk_stats["90s"] >= 8
        ].reset_index(drop=True)
        filtered_info = filtered_advanced.loc[
            :,
            (
                [col for col in info_cols if col != "Minutes played"]
                if "Minutes played" not in advanced_gk.columns
                else info_cols
            ),
        ]
        filtered_advanced = filtered_advanced.drop(
            labels=(
                [col for col in info_cols if col != "Minutes played"]
                if "Minutes played" not in advanced_gk.columns
                else info_cols
            ),
            axis=1,
        )

        advanced_gk_percentiles: pd.DataFrame = filtered_advanced.rank(
            pct=True, na_option="bottom"
        )
        advanced_gk_percentiles = (advanced_gk_percentiles * 100).round(1)
        for col in (
            [col for col in info_cols if col != "Minutes played"]
            if "Minutes played" not in advanced_gk.columns
            else info_cols
        ):
            advanced_gk_percentiles[col] = filtered_info[col]

        advanced_stats: dict = {}
        for stat in selected_advanced_gk.columns:
            advanced_stats[stat] = (
                selected_advanced_gk.loc[:, stat].values[0],
                advanced_gk_percentiles.loc[
                    (
                        (advanced_gk_percentiles["Player"] == selected_player)
                        & (advanced_gk_percentiles["Squad"] == selected_team)
                    ),
                    stat,
                ].values[0],
            )

        # ----------------------------------------------------------------------------------
        filtered_distribution = distribution_gk.loc[
            distribution_gk["90s"] >= 8
        ].reset_index(drop=True)
        filtered_info = filtered_distribution.loc[
            :,
            (
                [col for col in info_cols if col != "Minutes played"]
                if "Minutes played" not in distribution_gk.columns
                else info_cols
            ),
        ]
        filtered_distribution = filtered_distribution.drop(
            labels=(
                [col for col in info_cols if col != "Minutes played"]
                if "Minutes played" not in distribution_gk.columns
                else info_cols
            ),
            axis=1,
        )

        distribution_gk_percentiles: pd.DataFrame = filtered_distribution.rank(
            pct=True, na_option="bottom"
        )
        distribution_gk_percentiles = (distribution_gk_percentiles * 100).round(1)
        for col in (
            [col for col in info_cols if col != "Minutes played"]
            if "Minutes played" not in distribution_gk.columns
            else info_cols
        ):
            distribution_gk_percentiles[col] = filtered_info[col]

        distribution_gk_stats: dict = {}
        for stat in selected_distribution_gk.columns:
            distribution_gk_stats[stat] = (
                selected_distribution_gk.loc[:, stat].values[0],
                distribution_gk_percentiles.loc[
                    (
                        (distribution_gk_percentiles["Player"] == selected_player)
                        & (distribution_gk_percentiles["Squad"] == selected_team)
                    ),
                    stat,
                ].values[0],
            )
        # ----------------------------------------------------------------------------------
        # Merge everything into a single dict
        data["Goalkeeping"] = standard_stats
        data["Advanced GK"] = advanced_stats
        data["Distribution GK"] = distribution_gk_stats

    return data


# Percentiles calculation logic
def percentiles_calculator(data_group: str) -> dict:
    """
    Main repetitive logic to calculate the percentiles.

    Args:
        data_group (str): Data group to identify the calculation logic.

    Returns:
        (dict): Dictionary of per 90 stats and percentiles.
    """
    info_cols: list = ["Player", "Squad", "Minutes played", "90s"]

    pass


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
    elif data_group == "Distribution GK":
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
