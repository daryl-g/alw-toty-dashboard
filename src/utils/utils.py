# Utility functions

# Imports
import pandas as pd
import streamlit as st


def shorten_team_name(name: str) -> str | dict:
    """
    Get the three-letter abbreviation from FBRef's A-League team name.

    Args:
        name (str): Opta/FBRef's name of the A-League team.

    Returns:
        (str | dict): Three-letter abbreviation of the team name. Mapping of all team names to their abbreviations if `all` is passed.
    """
    team_name_map: dict = {
        "Adelaide Utd": "ADL",
        "Brisbane Roar": "BRR",
        "Canberra Utd": "CAN",
        "Central Coast Mariners": "CCM",
        "Melb City": "MCY",
        "Melb Victory": "VIC",
        "Newcastle Jets": "NEW",
        "Perth Glory": "PER",
        "Sydney FC": "SYD",
        "Wellington Phoenix": "WEL",
        "Western United": "WUN",
        "W Sydney": "WSW",
    }

    if name is None:
        raise ValueError("Team name cannot be None!")
    elif name not in team_name_map and name != "all":
        st.warning(
            f"Team name '{name}' not found in the mapping. Returning original name."
        )
        return name
    elif name == "all":
        return team_name_map
    else:
        return team_name_map.get(name, name)


def load_csv(
    file_path: str,
    display: bool = True,
):
    """
    Load a CSV file, return its content as a DataFrame, and display on the app.

    Args:
        file_path (str): Path to the CSV file.
        display (bool, optional): Whether to display the DataFrame in the app. Defaults to True.

    Returns:
        (pd.DataFrame)
            DataFrame containing the CSV file content.
    """

    # Load the CSV file
    df = pd.read_csv(file_path, delimiter=",", encoding="utf-8")

    # Display the DataFrame in the app
    if display:
        df = st.data_editor(
            df, use_container_width=True, hide_index=True, num_rows="dynamic"
        )

    # Return the DataFrame
    return df


def display_markdown(file_path: str):
    """
    Load and display a markdown file in the app.

    Args:
        file_path (str): Path to the markdown file.
    """

    # Load the markdown file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Display the content in the app
    st.markdown(content)
