# Imports
import streamlit as st

# Custom modules
from utils import shorten_team_name


def dropdown(multiselect: bool) -> str | list | None:
    """
    Reusable team selection dropdown component.

    Args:
        multiselect (bool): If True, allows multiple team selections.

    Returns:
        (str | list | None): Selected team(s) from the dropdown. None if no selection is made.
    """

    team_options: list = list(shorten_team_name("all").keys())
    team_options.sort()

    if multiselect:
        selected_teams = st.multiselect(
            label="Select Team(s)",
            options=team_options,
            default=None,
            placeholder="Select one or more teams...",
        )
        return selected_teams
    else:
        selected_team: str | None = st.selectbox(
            label="Select team",
            options=team_options,
            index=None,
            placeholder="Select a team...",
        )
        return selected_team
