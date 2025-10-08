# Imports
import streamlit as st
from pandas import DataFrame
from mplsoccer import Pitch, VerticalPitch
from matplotlib.axes import Axes

# Custom modules
from styles import get_team_colours
from utils import get_team_name, import_fonts


@st.cache_resource
def get_positions(
    _pitch: Pitch | VerticalPitch,
    second_striker: bool = False,
    line: int = 5,
) -> DataFrame:
    """
    Get positions coordinates on the pitch.

    Args:
        pitch (mplsoccer.Pitch | mplsoccer.VerticalPitch): mplsoccer Pitch object with specified pitch type.
        second_striker (bool, optional): Whether to include the second striker position. Defaults to False.
        line (int, optional): Number of lines in the formation (4 or 5). Defaults to 4.

    Returns:
        pd.DataFrame: Coordinates of the positions on the pitch, along with position nodes being plotted.
    """
    temp_pos = _pitch.get_positions(second_striker=second_striker, line=line)

    loc_list = [
        "GK",
        "RB",
        "CB",
        "LB",
        "RWB",
        "CDM",
        "LWB",
        "RM",
        "RW",
        "CM",
        "LM",
        "CAM",
        "ST",
    ]
    loc_list = loc_list if second_striker == False else loc_list + ["SS"]

    positions = temp_pos.loc[
        loc_list,
        ["x", "y"],
    ]

    # Push the x coordinate of LM and RM up a bit higher
    positions.loc[["LM", "RM"], "x"] = positions.loc[["RM", "RW"], "x"].mean()

    positions = positions.drop(["RW"])

    # Rename positions to match the data
    positions = positions.rename(
        index={
            "CDM": "DM",
            "CAM": "AM",
            "ST": "CF",
        }
    )

    return positions


def plot_positions(
    pitch: Pitch | VerticalPitch,
    ax: Axes,
    team: str,
    second_striker: bool = False,
    line: int = 5,
    node_size: float = 500,
    text_size: int = 8,
) -> None:
    """
    Plot the positions on the pitch

    Args:
        pitch (mplsoccer.Pitch | mplsoccer.VerticalPitch): mplsoccer Pitch object with specified pitch type.
        ax (matplotlib.axes.Axes): The axis to plot on.
        team (str): Name of team selected by the user.
        second_striker (bool, optional): Whether to include the second striker position. Defaults to False.
        line (int, optional): Number of lines in the formation (4 or 5). Defaults to 4.
        node_size (float, optional): Size of the position nodes. Defaults to 1500.
        text_size (int, optional): Font size of the position text. Defaults to 14.

    Returns:
        pd.DataFrame: Coordinates of the positions on the pitch, along with position nodes being plotted.
    """

    colours = get_team_colours(team=get_team_name(team, mode="short"))
    # Get the position coordinates
    positions = get_positions(_pitch=pitch, second_striker=second_striker, line=line)

    # Plot the position nodes on the pitch
    for i in range(len(positions.index)):
        positions_coords = (
            positions.loc[positions.index[i], "x"],
            positions.loc[positions.index[i], "y"],
        )

        pitch.scatter(
            positions_coords[0],
            positions_coords[1],
            s=node_size,
            color=colours["primary"],
            edgecolors=colours["secondary"],
            zorder=1,
            ax=ax,
        )

        pitch.annotate(
            positions.index[i],
            xy=positions_coords,
            xytext=positions_coords,
            ha="center",
            va="center",
            fontproperties=import_fonts(weight="bold"),
            fontsize=text_size,
            color=colours["secondary"],
            ax=ax,
        )
