# Utility functions

# Imports
import pandas as pd
import streamlit as st
import matplotlib.font_manager as fm  # Import fonts

from PIL import Image


def get_team_name(name: str, mode: str = "short") -> str | dict:
    """
    Get the three-letter abbreviation from FBRef's A-League team name.

    Args:
        name (str): Opta/FBRef's name of the A-League team. Use 'all' to get all team names.
        mode (str): 'short' for abbreviated team name, 'full' for full, displayable team name.

    Returns:
        (str | dict): Three-letter abbreviation of the team name. Mapping of all team names to their abbreviations if `all` is passed.
    """
    if mode not in ["short", "full"]:
        raise ValueError(
            "Unknown text mode. Please choose between 'short' for abbreviated names and 'full' for full team names."
        )

    # Key: Opta-formatted team name
    # Value[0]: Abbreviated team name for getting colours (I might change this later cause this was supposed to be the universal mapping for the code)
    # Value[1]: Full team name for display purposes
    team_name_map: dict = {
        "Adelaide Utd": ("ADL", "Adelaide United"),
        "Brisbane Roar": ("BRR", "Brisbane Roar"),
        "Canberra Utd": ("CAN", "Canberra United"),
        "Central Coast Mariners": ("CCM", "Central Coast Mariners"),
        "Melb City": ("MCY", "Melbourne City"),
        "Melb Victory": ("VIC", "Melbourne Victory"),
        "Newcastle Jets": ("NEW", "Newcastle Jets"),
        "Perth Glory": ("PER", "Perth Glory"),
        "Sydney FC": ("SYD", "Sydney FC"),
        "Wellington Phoenix": ("WEL", "Wellington Phoenix"),
        "Western United": ("WUN", "Western United"),
        "W Sydney": ("WSW", "Western Sydney Wanderers"),
    }

    if name is None:
        raise ValueError("Team name cannot be None!")
    # If the input is neither an Opta-formatted team name nor the full team name
    elif (
        (name not in team_name_map.keys())
        and (name not in [name[1] for name in team_name_map.values()])
    ) and (name != "all"):
        st.warning(
            f"Team name '{name}' not found in the mapping. Returning original name."
        )
        return name
    elif name == "all":
        return team_name_map
    else:
        # If the input is an Opta-formatted team name
        if name in team_name_map.keys():
            return (
                team_name_map.get(name, name)[0]
                if mode == "short"
                else team_name_map.get(name, name)[1]
            )
        # If the input is the full team name
        else:
            # Flatten the dictionary
            full_names = [name[1] for name in team_name_map.values()]
            short_names = [name[0] for name in team_name_map.values()]
            opta_names = list(team_name_map.keys())

            # Reverse look
            for i in range(len(full_names)):
                if name == full_names[i]:
                    return short_names[i] if mode == "short" else opta_names[i]


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


def import_fonts(
    weight: str = "regular",
) -> fm.FontProperties | list[fm.FontProperties, fm.FontProperties, fm.FontProperties]:
    """
    This function imports the Roboto Regular and/or Roboto Bold fonts from the same folder as this code.

    Args:
        weight (str): Single font weight ('regular', 'light', 'bold'). Use 'all' to get all fonts.

    Returns:
        Single font properties or tuple containing the Roboto Regular and Roboto Bold fonts.
    """
    if weight.lower() not in ["regular", "light", "bold", "all"]:
        raise ValueError(
            "Unknown font weight. Please choose from 'regular', 'light', 'bold', or 'all' to get all fonts."
        )

    # Import the fonts from the same folder as this code
    robotoRegular = fm.FontProperties(fname="src/assets/fonts/Roboto-Regular.ttf")
    robotoLight = fm.FontProperties(fname="src/assets/fonts/Roboto-Light.ttf")
    robotoBold = fm.FontProperties(fname="src/assets/fonts/Roboto-Bold.ttf")

    if weight == "all":
        return robotoRegular, robotoLight, robotoBold
    elif weight == "regular":
        return robotoRegular
    elif weight == "light":
        return robotoLight
    elif weight == "bold":
        return robotoBold
    else:
        raise ValueError(
            "Unknown font weight. Please choose from 'regular', 'light', 'bold', or 'all' to get all fonts."
        )


def load_team_logo(team: str):
    """
    Map team name with the locally-stored team logo.

    Args:
        team (str): Opta/FBRef or full, displayed team name (aka 'Melb City' or 'Melbourne City').

    Returns:
        (PIL.Image.ImageFile): Image file loaded by PIL.
    """
    folder_path = "src/assets/imgs/"
    file_extension = ".png"

    team_logo_map: dict = {
        "Adelaide Utd": folder_path + "Adelaide_United" + file_extension,
        "Brisbane Roar": folder_path + "Brisbane_Roar" + file_extension,
        "Canberra Utd": folder_path + "Canberra_United" + file_extension,
        "Central Coast Mariners": folder_path + "CC_Mariners" + file_extension,
        "Melb City": folder_path + "Melb_City" + file_extension,
        "Melb Victory": folder_path + "Melb_Victory" + file_extension,
        "Newcastle Jets": folder_path + "Newcastle_Jets" + file_extension,
        "Perth Glory": folder_path + "Perth_Glory" + file_extension,
        "Sydney FC": folder_path + "Sydney" + file_extension,
        "Wellington Phoenix": folder_path + "Wellington_Phoenix" + file_extension,
        "Western United": folder_path + "Western_United" + file_extension,
        "W Sydney": folder_path + "WSydney_Wanderers" + file_extension,
    }

    if team not in team_logo_map.keys():
        team = get_team_name(team, mode="full")

    return Image.open(team_logo_map.get(team, team))


def map_player_positions(file_name: str, position_sort: bool = False) -> pd.DataFrame:
    """
    Map Opta/FBRef's player data with each player's correct positions.

    Args:
        file_name (str): Name of the CSV data file without the folder path at the front and the file extension at the end.
        position_sort (bool, optional): Sort joined DataFrame by position? Default is False.

    Returns:
        (pd.DataFrame): Loaded data with mapped positions.
    """
    folder_name = "data/"
    file_extension = ".csv"

    # Load the files
    data_file = load_csv(
        file_path=folder_name + file_name + file_extension, display=False
    )
    position_map = load_csv(
        file_path=folder_name + "PositionMap" + file_extension, display=False
    )

    # Map positions to match data
    position_map.loc[position_map["Main Pos"] == "LW", "Main Pos"] = "LM"
    position_map.loc[position_map["Main Pos"] == "RW", "Main Pos"] = "RM"

    joined = pd.merge(
        data_file,
        position_map,
        left_on=["Player", "Squad"],
        right_on=["Player", "Squad"],
        how="left",
    )

    if position_sort == True:
        joined["Main Pos"] = pd.Categorical(
            joined["Main Pos"],
            [
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
            ],
        ).astype(str)
        joined = joined.sort_values(by="Main Pos").reset_index(drop=True)

    return joined
