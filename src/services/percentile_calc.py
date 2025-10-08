# Percentile calculator

# Imports
import pandas as pd

# Custom modules
from utils import load_csv, map_player_positions, get_team_name


# ----------------------------------------------------------------------------------
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
    else:
        data_groups = [
            "Shooting",
            "Chance creating",
            "Distributing",
            "Dead-ball distributing",
            "Possession",
            "Defending",
            "Discipline",
        ]

    for group in data_groups:
        data[group] = percentiles_calculator(
            data_group=group,
            selected_player=selected_player,
            selected_team=selected_team,
            player_position=player_position,
        )

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
    file_name: str = ""
    file_paths: list[str] = []
    if data_group == "Goalkeeping":
        file_name = "Goalkeeping"
    elif data_group == "Advanced GK" or data_group == "Distribution (GK)":
        file_name = "AdvancedGK"
    elif data_group == "Shooting":
        file_name = "Shooting"
    # Chance creating (Passing + GCA-SCA)
    elif data_group == "Chance creating":
        file_paths = ["Passing", "GCASCA"]
    # Distributing (Passing + PassTypes)
    elif data_group == "Distributing":
        file_paths = ["Passing", "PassTypes"]
    # Dead-ball distributing (PassTypes + GCA-SCA)
    elif data_group == "Dead-ball distributing":
        file_paths = ["PassTypes", "GCASCA"]
    elif data_group == "Possession":
        file_name = "Possession"
    # Defending (DefActions + Misc (just for the aerial duels lol))
    elif data_group == "Defending":
        file_paths = ["DefActions", "Misc"]
    elif data_group == "Discipline":
        file_name = "Misc"

    # Load data
    if player_position == "GK":
        data: pd.DataFrame = load_csv(file_name, display=False)
    else:
        if data_group in ["Shooting", "Possession", "Discipline"]:
            data: pd.DataFrame = map_player_positions(file_name)
        else:
            # Get data from two files and then merge them together
            file1: pd.DataFrame = map_player_positions(file_paths[0])
            file2: pd.DataFrame = map_player_positions(file_paths[1])

            data: pd.DataFrame = pd.merge(
                left=file1,
                right=file2,
                how="inner",
                on=["Player", "Squad", "90s", "Main Pos", "Other Pos"],
                suffixes=(None, "_y"),
            )

            data = data.drop([col for col in data.columns if "_y" in col], axis=1)

    metrics: list = sorted_metrics(data_group)

    # For possession-adjusted stats
    # if data_group == "Defending":
    #     teamPossession: pd.DataFrame = load_csv(
    #         "data/TeamPossession.csv", display=False
    #     )

    #     # Calculate opposition's possession time
    #     teamPossession["oppPoss"] = 100 - teamPossession["Possession %"]

    # Get raw per 90s stats
    selected_stats: pd.DataFrame = data.loc[
        ((data["Player"] == selected_player) & (data["Squad"] == selected_team)),
        metrics,
    ]

    # Preprocessing for percentile rank
    if player_position in ["LW", "LM"]:
        main_pos_1 = "LW" if player_position == "LW" else "LM"
        main_pos_2 = "LM" if player_position == "LW" else "LW"
        filtered_stats = data.loc[
            (
                (
                    (data["Main Pos"] == main_pos_1)
                    | data["Other Pos"].astype(str).str.contains(main_pos_1)
                )
                | (
                    (data["Main Pos"] == main_pos_2)
                    | data["Other Pos"].astype(str).str.contains(main_pos_2)
                )
            )
            & (data["90s"] >= min_90s)
        ].reset_index(drop=True)
    elif player_position in ["RW", "RM"]:
        main_pos_1 = "RW" if player_position == "RW" else "RM"
        main_pos_2 = "RM" if player_position == "RW" else "RW"
        filtered_stats = data.loc[
            (
                (
                    (data["Main Pos"] == main_pos_1)
                    | data["Other Pos"].astype(str).str.contains(main_pos_1)
                )
                | (
                    (data["Main Pos"] == main_pos_2)
                    | data["Other Pos"].astype(str).str.contains(main_pos_2)
                )
            )
            & (data["90s"] >= min_90s)
        ].reset_index(drop=True)
    elif player_position == "GK":
        filtered_stats = data.loc[(data["90s"] >= min_90s)].reset_index(drop=True)
    else:
        filtered_stats = data.loc[
            (
                (data["Main Pos"] == player_position)
                | data["Other Pos"].astype(str).str.contains(player_position)
            )
            & (data["90s"] >= min_90s)
        ].reset_index(drop=True)

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
    elif data_group == "Possession":
        percentiles["Miscontrols"] = 1 - percentiles["Miscontrols"]
        percentiles["Dispossessed"] = 1 - percentiles["Dispossessed"]
    elif data_group == "Discipline":
        for col in metrics:
            percentiles[col] = 1 - percentiles[col]

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


# ----------------------------------------------------------------------------------
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
    elif data_group == "Chance creating":
        return [
            "Assists",
            "Expected Assists",
            "Assist overperformance",
            "Key passes",
            "Crosses into Penalty Area",
            "Goal-creating Actions",
            "Shot-creating Actions",
            "SCA Live-ball passes",
            "SCA Take-ons",
        ]
    elif data_group == "Distributing":
        return [
            "Passes attempted",
            "Pass completion percentage",
            "Short passes attempted",
            "Short pass completion percentage",
            "Long passes attempted",
            "Long pass completion percentage",
            "Passes into final third",
            "Passes into penalty box",
            "Through balls",
            "Progressive passes",
        ]
    elif data_group == "Dead-ball distributing":
        return [
            "Dead-ball Passes",
            "GCA Dead-ball passes",
            "SCA Dead-ball passes",
            "Corner kicks",
            "Inswinging corners",
            "Outswinging corners",
            "Straight corners",
            "Free-kick Passes",
            "Throw-ins",
        ]
    elif data_group == "Possession":
        return [
            "Passes received",
            "Progressive passes received",
            "Touches in attacking third",
            "Touches in attacking box",
            "Take-ons attempted",
            "Take-ons successful rate",
            "Carries made",
            "Progressive carries",
            "Carries into penalty box",
            "Miscontrols",
            "Dispossessed",
        ]
    elif data_group == "Defending":
        return [
            "Interceptions",
            "Tackles won",
            "Tackles in defensive third",
            "Tackles in middle third",
            "Tackles in attacking third",
            "Dribbles challenged",
            "Percentage of dribbles tackled",
            "Aerial duels won",
            "Aerial duels won percentage",
            "Blocked shots",
            "Blocked passes",
            "Clearances",
            "Ball recoveries",
        ]
    elif data_group == "Discipline":
        return ["Fouls committed", "Yellow cards", "Red cards"]


# Weighting
def positional_weighting(player_position: str) -> dict:
    """
    Retrieve metric groups weighting for each position.

    Args:
        player_position (str): Selected player's position.

    Returns:
        (dict): Dictionary with the weighting for each metric group.
    """
    # Input checking
    if player_position not in [
        "GK",
        "CB",
        "LB",
        "LWB",
        "RB",
        "RWB",
        "DM",
        "CM",
        "AM",
        "LM",
        "LW",
        "RM",
        "RW",
        "CF",
    ]:
        raise ValueError(
            "Unknown player position. Please only choose from the available positions."
        )

    # Positional weighting
    # Goalkeeper
    if player_position == "GK":
        return {
            "Shot stopping": {
                "Post-shot xG": 0.9,
                "PSxG difference": 0.9,
                "Save percentage": 0.7,
                "Cross stopped percentage": 0.6,
                "Penalties save percentage": 0.5,
            },
            "Sweeping": {
                "Out-of-box defensive actions": 0.6,
                "Average OPA distance": 0.5,
            },
            "Distributing": {
                "Passes attempted": 0.6,
                "Launched goal kicks percentage": 0.5,
                "Launches completion percentage": 0.4,
                "Throws attempted": 0.4,
            },
        }
    # Centre-back
    elif player_position == "CB":
        return {
            "Chance creating": {"Key passes": 0.4, "Shot-creating Actions": 0.3},
            "Distributing": {
                "Short pass completion percentage": 0.6,
                "Long pass completion percentage": 0.6,
                "Progressive passes": 0.5,
                "Passes into final third": 0.4,
            },
            "Possession": {
                "Carries made": 0.5,
                "Progressive carries": 0.4,
            },
            "Defending": {
                "Tackles won": 0.9,
                "Interceptions": 0.8,
                "Percentage of dribbles tackled": 0.7,
                "Aerial duels won percentage": 0.7,
                "Blocked shots": 0.6,
                "Blocked passes": 0.6,
                "Clearances": 0.6,
            },
            "Discipline": {
                "Fouls committed": 0.6,
                "Yellow cards": 0.5,
                "Red cards": 0.5,
            },
        }
    # Full-back/Wing-back
    elif player_position in ["LB", "LWB", "RB", "RWB"]:
        return {
            "Chance creating": {
                "Crosses into Penalty Area": 0.8,
                "Assists": 0.7,
                "Expected Assists": 0.7,
                "Shot-creating Actions": 0.7,
                "Key passes": 0.6,
            },
            "Distributing": {
                "Passes into final third": 0.6,
                "Passes into penalty box": 0.6,
                "Progressive passes": 0.6,
                "Through balls": 0.5,
            },
            "Possession": {
                "Take-ons successful rate": 0.8,
                "Carries made": 0.6,
                "Progressive carries": 0.6,
                "Carries into penalty box": 0.5,
            },
            "Defending": {
                "Interceptions": 0.8,
                "Tackles won": 0.7,
                "Percentage of dribbles tackled": 0.7,
                "Blocked passes": 0.6,
                "Aerial duels won percentage": 0.5,
                "Clearances": 0.5,
            },
            "Discipline": {
                "Fouls committed": 0.6,
                "Yellow cards": 0.4,
                "Red cards": 0.4,
            },
        }
    # Defensive/central midfielder
    elif player_position in ["DM", "CM"]:
        return {
            "Chance creating": {
                "Expected Assists": 0.6,
                "Key passes": 0.7,
                "Shot-creating Actions": 0.6,
            },
            "Distributing": {
                "Passes attempted": 0.9,
                "Short pass completion percentage": 0.8,
                "Long pass completion percentage": 0.7,
                "Passes into final third": 0.7,
                "Through balls": 0.7,
                "Progressive passes": 0.7,
                "Passes into penalty box": 0.6,
            },
            "Possession": {
                "Passes received": 0.7,
                "Progressive passes received": 0.6,
                "Dispossessed": 0.5,
                "Carries made": 0.4,
                "Progressive carries": 0.4,
            },
            "Defending": {
                "Interceptions": 0.8,
                "Tackles won": 0.7,
                "Tackles in middle third": 0.7,
                "Blocked passes": 0.6,
                "Percentage of dribbles tackled": 0.5,
                "Clearances": 0.3,
            },
            "Discipline": {
                "Fouls committed": 0.4,
                "Yellow cards": 0.3,
                "Red cards": 0.3,
            },
        }
    # Attacking midfielder
    elif player_position == "AM":
        return {
            "Shooting": {
                "Goals": 0.7,
                "Non-penalty xG": 0.7,
                "xG overperformance": 0.5,
                "npxG per Shot": 0.5,
            },
            "Chance creating": {
                "Expected Assists": 0.9,
                "Assist overperformance": 0.9,
                "Key passes": 0.8,
                "Goal-creating Actions": 0.8,
                "Shot-creating Actions": 0.8,
            },
            "Distributing": {
                "Passes attempted": 0.8,
                "Passes into final third": 0.7,
                "Passes into penalty box": 0.7,
                "Through balls": 0.6,
                "Progressive passes": 0.6,
            },
            "Possession": {
                "Take-ons successful rate": 0.7,
                "Carries made": 0.7,
                "Passes received": 0.6,
                "Progressive passes received": 0.6,
                "Touches in attacking third": 0.6,
                "Progressive carries": 0.6,
                "Dispossessed": 0.6,
            },
            "Defending": {
                "Tackles in attacking third": 0.5,
                "Blocked passes": 0.4,
            },
        }
    # Winger/Wide midfielder
    elif player_position in ["LM", "LW", "RM", "RW"]:
        return {
            "Shooting": {
                "Goals": 0.7,
                "Non-penalty xG": 0.6,
                "xG overperformance": 0.6,
                "npxG per Shot": 0.6,
            },
            "Chance creating": {
                "Expected Assists": 0.9,
                "Assist overperformance": 0.8,
                "Goal-creating Actions": 0.8,
                "Shot-creating Actions": 0.8,
                "Crosses into Penalty Area": 0.8,
                "Key passes": 0.7,
            },
            "Distributing": {
                "Passes into penalty box": 0.8,
                "Through balls": 0.7,
                "Progressive passes": 0.7,
                "Long pass completion percentage": 0.6,
            },
            "Possession": {
                "Touches in attacking third": 0.8,
                "Take-ons attempted": 0.8,
                "Take-ons successful rate": 0.8,
                "Passes received": 0.7,
                "Progressive passes received": 0.7,
                "Dispossessed": 0.7,
                "Carries made": 0.6,
                "Progressive carries": 0.6,
            },
            "Defending": {
                "Tackles in attacking third": 0.5,
                "Blocked passes": 0.4,
            },
        }
    # Striker
    elif player_position == "CF":
        return {
            "Shooting": {
                "Goals": 0.9,
                "Non-penalty xG": 0.9,
                "xG overperformance": 0.9,
                "Shots on Target percentage": 0.9,
                "npxG per Shot": 0.9,
            },
            "Chance creating": {
                "Expected Assists": 0.7,
                "Goal-creating Actions": 0.7,
                "Shot-creating Actions": 0.7,
                "Assist overperformance": 0.6,
                "Key passes": 0.6,
            },
            "Possession": {
                "Touches in attacking third": 0.8,
                "Take-ons successful rate": 0.7,
                "Passes received": 0.6,
                "Progressive passes received": 0.6,
                "Carries made": 0.5,
                "Progressive carries": 0.5,
            },
            "Defending": {
                "Tackles in attacking third": 0.4,
                "Blocked passes": 0.3,
            },
        }
