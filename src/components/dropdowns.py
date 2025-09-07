# Imports
import pandas as pd
import streamlit as st

# Custom modules
from utils import get_team_name, load_csv


def team_dropdown(multiselect: bool) -> str | list | None:
    """
    Reusable team selection dropdown component.

    Args:
        multiselect (bool): If True, allows multiple team selections.

    Returns:
        (str | list | None): Selected team(s) from the dropdown. None if no selection is made.
    """

    team_options: list = [name[1] for name in get_team_name("all").values()]
    team_options.sort()

    if multiselect:
        selected_teams: list = st.multiselect(
            label="Select team(s)",
            options=team_options,
            default=None,
            placeholder="Select one or more teams...",
        )
        return selected_teams
    else:
        selected_team: str | None = st.selectbox(
            label="Select team",
            options=team_options,
            index=0,
            placeholder="Select a team...",
        )
        return selected_team


def player_dropdown(selected_team: str, multiselect: bool) -> str | list | None:
    """
    Reusable player selection dropdown component.

    Args:
        multiselect (bool): If True, allows multiple player selections.

    Returns:
        (str | list | None): Selected player(s) from the dropdown. None if no selection is made.
    """

    df = load_csv("data/PositionMap.csv", display=False)
    df["Main Pos"] = pd.Categorical(
        df["Main Pos"],
        [
            "GK",
            "CB",
            "LB",
            "LWB",
            "RB",
            "RWB",
            "DM",
            "CM",
            "LM",
            "LW",
            "RM",
            "RW",
            "AM",
            "CF",
        ],
    )

    slice_df = df.loc[
        df["Squad"] == get_team_name(selected_team, mode="full"), ["Player", "Main Pos"]
    ].sort_values(by="Main Pos")
    slice_df["Display"] = (
        slice_df["Player"] + " (" + slice_df["Main Pos"].astype(str) + ")"
    )

    if multiselect:
        selected_players: list = st.multiselect(
            label="Select player(s)",
            options=slice_df["Display"],
            default=None,
            placeholder="Select one or more players...",
        )
        return selected_players
    else:
        selected_team: str | None = st.selectbox(
            label="Select player",
            options=slice_df["Display"],
            index=0,
            placeholder="Select a player...",
        )
        return selected_team
