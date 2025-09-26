# Get individual player stats

# Imports
import pandas as pd

# Custom modules
from utils import load_csv, map_player_positions


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
