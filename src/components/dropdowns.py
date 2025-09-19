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

    # Check for session data
    if "selected_teams" not in st.session_state:
        st.session_state.selected_teams = [team_options[0]]
    if "selected_team" not in st.session_state:
        st.session_state.selected_team = 0

    if multiselect:
        selected_teams: list = st.sidebar.multiselect(
            label="Select team(s)",
            options=team_options,
            default=(
                st.session_state.selected_teams
                if "selected_teams" in st.session_state
                else None
            ),
            placeholder="Select one or more teams...",
        )
        st.session_state.selected_teams = selected_teams
        return selected_teams
    else:
        selected_team: str | None = st.sidebar.selectbox(
            label="Select team",
            options=team_options,
            index=(
                st.session_state.selected_team
                if "selected_team" in st.session_state
                else 0
            ),
            placeholder="Select a team...",
        )

        try:
            st.session_state.selected_team = team_options.index(selected_team)
        except ValueError:
            st.session_state.selected_team = 0

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

    slice_df = (
        df.loc[
            df["Squad"] == get_team_name(selected_team, mode="full"),
            ["Player", "Main Pos"],
        ]
        .sort_values(by="Main Pos")
        .reset_index(drop=True)
    )
    slice_df["Display"] = (
        slice_df["Player"] + " (" + slice_df["Main Pos"].astype(str) + ")"
    )

    # Check for session data
    if "selected_players" not in st.session_state:
        st.session_state.selected_players = [slice_df["Display"].loc[0]]
    if "selected_player" not in st.session_state:
        st.session_state.selected_player = 0

    if multiselect:
        selected_players: list = st.sidebar.multiselect(
            label="Select player(s)",
            options=slice_df["Display"],
            default=(
                st.session_state.selected_players
                if "selected_players" in st.session_players
                else None
            ),
            placeholder="Select one or more players...",
        )
        st.session_state.selected_players = selected_players
        return selected_players
    else:
        selected_player: str | None = st.sidebar.selectbox(
            label="Select player",
            options=slice_df["Display"],
            index=(
                st.session_state.selected_player
                if ("selected_player" in st.session_state)
                & (st.session_state.selected_player <= len(slice_df["Display"]) - 1)
                else 0
            ),
            placeholder="Select a player...",
        )
        try:
            st.session_state.selected_player = (
                slice_df["Display"].to_list().index(selected_player)
            )
        except ValueError:
            st.session_state.selected_player = 0
        return selected_player
