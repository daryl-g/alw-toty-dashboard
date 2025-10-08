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
        selected_team (str): Team name selected by the user.
        multiselect (bool): If True, allows multiple player selections.

    Returns:
        (str | list | None): Selected player(s) from the dropdown. None if no selection is made.
    """

    df = load_csv("PositionMap", display=False)
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
                if "selected_players" in st.session_state
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


def position_dropdown(
    multiselect: bool, default_position: str = None
) -> str | list | None:
    """
    Dropdown to select player position.

    Args:
        default_position (str): Player's default position from the DataFrame. If None, assume the chosen position is GK.
        multiselect (bool): If True, allows multiple player selections.

    Returns:
        (str | list | None): Selected player(s) from the dropdown. None if no selection is made.
    """
    positions: list = [
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
    ]

    if default_position is None:
        default_position = positions[0]

    # Check for session data
    if "selected_positions" not in st.session_state:
        st.session_state.selected_positions = [default_position]
    if "selected_position" not in st.session_state:
        st.session_state.selected_position = positions.index(default_position)

    if multiselect:
        selected_positions: list = st.sidebar.multiselect(
            label="Select position(s)",
            options=positions,
            default=(
                st.session_state.selected_positions
                if "selected_positions" in st.session_state
                else None
            ),
            placeholder="Select one or more positions...",
        )
        st.session_state.selected_positions = selected_positions
        return selected_positions
    else:
        selected_position: str | None = st.sidebar.selectbox(
            label="Select position",
            options=(
                positions if st.session_state.selected_position != "GK" else ["GK"]
            ),
            index=(
                positions.index(st.session_state.selected_position)
                if ("selected_position" in st.session_state)
                and (st.session_state.selected_position != "GK")
                else (
                    0
                    if ("selected_position" in st.session_state)
                    and (st.session_state.selected_position == "GK")
                    else positions.index(default_position)
                )
            ),
            placeholder="Select a position...",
        )
        try:
            st.session_state.selected_position = positions.index(selected_position)
        except ValueError:
            st.session_state.selected_position = positions.index(default_position)
        return selected_position
