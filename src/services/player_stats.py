# Get individual player stats

# Imports
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Custom modules
from services import positional_weighting
from utils import load_csv, map_player_positions, get_team_name


# Functions to get data for the scatter plots
def scatter_data(
    data_group: str, metrics: list, player_position: str, min_90s: int
) -> pd.DataFrame:
    """
    Get data columns to plot a scatter plot.

    Args:
        data_group (str): Selected data group to plot the data.
        metrics (list): Tuple of two metrics to retrieve the data. First one is for the X axis, second one is for the Y axis.
        player_position (str): Selected player's position to filter the data.
        min_90s (int): Minimum 90s played to filter the data.

    Returns:
        pandas.DataFrame: DataFrame with the selected columns for the scatter plot.
    """
    # Input checking
    if (data_group is None) or (data_group == ""):
        raise ValueError(
            "data_group cannot be empty. Please specify a data group to retrieve data."
        )
    if metrics is None:
        raise ValueError(
            "No metrics received. Please choose two metrics to retrieve data."
        )
    elif len(metrics) < 2:
        raise ValueError(
            "Less than two metrics received. Please choose another metric to retrieve data."
        )
    elif len(metrics) > 2:
        raise ValueError(
            "More than two metrics received. Please evaluate the chosen metrics and remove some."
        )

    file_path: str = "data/"
    file_name: str = ""
    file_paths: list[str] = []
    if data_group == "Basic GK":
        file_name = "Goalkeeping.csv"
    elif data_group == "Advanced GK" or data_group == "Distributing":
        file_name = "AdvancedGK.csv"
    elif data_group == "Attacking":
        file_name = "Shooting"
    elif data_group == "Passing":
        file_paths = ["Passing", "PassTypes", "GCASCA"]
    elif data_group == "Defending":
        file_paths = ["DefActions", "Misc"]

    # Load data
    if data_group in ["Basic GK", "Advanced GK", "Distributing"]:
        data: pd.DataFrame = load_csv(file_path + file_name, display=False)
    else:
        if data_group == "Attacking":
            data: pd.DataFrame = map_player_positions(file_name)
        elif data_group == "Passing":
            # Get data from two files and then merge them together
            file1: pd.DataFrame = map_player_positions(file_paths[0])
            file2: pd.DataFrame = map_player_positions(file_paths[1])
            file3: pd.DataFrame = map_player_positions(file_paths[2])

            data: pd.DataFrame = pd.merge(
                left=file1,
                right=file2,
                how="inner",
                on=["Player", "Squad", "90s", "Main Pos", "Other Pos"],
                suffixes=(None, "_y"),
            )
            data: pd.DataFrame = pd.merge(
                left=data,
                right=file3,
                how="inner",
                on=["Player", "Squad", "90s", "Main Pos", "Other Pos"],
                suffixes=(None, "_y"),
            )

            data = data.drop([col for col in data.columns if "_y" in col], axis=1)
        elif data_group == "Defending":
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

    if player_position != "GK":
        if player_position in ["LM", "LW"]:
            main_pos_1 = "LW" if player_position == "LW" else "LM"
            main_pos_2 = "LM" if player_position == "LW" else "LW"
            return data.loc[
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
                & (data["90s"] >= min_90s),
                metrics + ["Player"],
            ].reset_index(drop=True)
        elif player_position in ["RM", "RW"]:
            main_pos_1 = "RW" if player_position == "RW" else "RM"
            main_pos_2 = "RM" if player_position == "RW" else "RW"
            return data.loc[
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
                & (data["90s"] >= min_90s),
                metrics + ["Player"],
            ].reset_index(drop=True)
        else:
            return data.loc[
                (
                    (data["Main Pos"] == player_position)
                    | data["Other Pos"].astype(str).str.contains(player_position)
                )
                & (data["90s"] >= min_90s)
            ].reset_index(drop=True)
    else:
        return data.loc[
            (data["90s"] >= min_90s),
            metrics + ["Player"],
        ].reset_index(drop=True)


# Player similarity calculator
def player_similarity(
    selected_player: str, selected_team: str, player_position: str
) -> pd.DataFrame:
    """
    Calculate player similarity.

    Logic for percentile calculation is similar to the `percentile_calculator` function, but is modified to fit the current purpose.

    Args:
        selected_player (str): User selected player from the Dropdown option.
        selected_team (str): Only for filtering purpose if there are two players with the same name.
        player_position (str): Selected player's position.

    Returns:
        pandas.DataFrame: DataFrame of cosine similarity.
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

    info_cols: list = ["Player", "Squad", "Minutes played", "90s"]

    min_90s: int = 0
    if player_position == "GK":
        min_90s = 5
    else:
        min_90s = 8

    # Get the metrics list
    metrics_dict: dict = positional_weighting(player_position=player_position)
    metrics: list = []
    for group in metrics_dict.keys():
        metrics = metrics + list(metrics_dict[group].keys())

    # Load data
    file_path: str = "data/"
    files: list = []
    merge_columns: list = []
    data: pd.DataFrame = pd.DataFrame()
    if player_position == "GK":
        files = ["Goalkeeping.csv", "AdvancedGK.csv"]
        merge_columns = ["Player", "Squad", "90s"]
    else:
        files = [
            "Shooting",
            "Passing",
            "GCASCA",
            "PassTypes",
            "Possession",
            "DefActions",
            "Misc",
        ]
        merge_columns = ["Player", "Squad", "90s", "Main Pos", "Other Pos"]
    for file in files:
        # Load data from file
        if player_position == "GK":
            from_file = load_csv(file_path + file, display=False)
        else:
            from_file = map_player_positions(file)
        # Merge with main file
        if len(data) == 0:
            data = from_file
        else:
            data = pd.merge(
                left=data,
                right=from_file,
                how="left",
                on=merge_columns,
                suffixes=(None, "_y"),
            )
        # Drop duplicate columns
        data = data.drop([col for col in data.columns if "_y" in col], axis=1)
        try:
            data = data.drop("Minutes played", axis=1)
        except KeyError:
            pass

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
    if player_position != "GK":
        inverse_metrics = [
            "Dispossessed",
            "Fouls committed",
            "Yellow cards",
            "Red cards",
        ]
        for col in inverse_metrics:
            try:
                percentiles[col] = 1 - percentiles[col]
            except KeyError:
                pass

    # Convert to 1-100 scale and round up
    percentiles = (percentiles * 100).round(1)

    # Add player info...
    for col in (
        [col for col in info_cols if col != "Minutes played"]
        if "Minutes played" not in data.columns
        else info_cols
    ):
        percentiles[col] = filtered_info[col]
    # ...then set it as index
    percentiles = percentiles.set_index(
        [col for col in info_cols if col != "Minutes played"]
    )

    # Calculate cosine similarity
    similarity: list = cosine_similarity(percentiles)
    similarity_df: pd.DataFrame = pd.DataFrame(
        data=similarity,
        index=filtered_info["Player"],
        columns=filtered_info["Player"],
    )
    similarity_df = (similarity_df * 100).round(1)

    return similarity_df.loc[
        selected_player,
        similarity_df.columns.difference([selected_player]),
    ].sort_values(ascending=False)


def role_calculator(selected_player: str, selected_position: str) -> dict:
    """
    Calculate position rating for selected player.

    Args:
        selected_player (str): Player selected by the user.
        selected_position (str): Position selected by the user.

    Returns:
        dict: Dictionary with metric group ratings and overall rating.
    """
    pass
