# Wrapper and logic for the download button

# Imports
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from mplsoccer import PyPizza
from matplotlib.figure import Figure

from styles import Styles
from utils import import_fonts

# Get colour palette
styles: Styles = Styles()
palette: dict = styles.get_style(style=st.session_state.theme)


# Class wrapper for the download button
class Download:
    """
    Class wrapper for Streamlit's `download_button`.
    """

    # Class constructor
    def __init__(self, page: str):
        """
        Download class constructor.

        Args:
            page (str): Which page is calling the class?
        """
        self.page = page

    def button_init(self, figure: io.BytesIO, viz_name: str):
        """
        Initialise the button with the created figure.

        Args:
            figure (mpl.figure.Figure): Matplotlib viz created by one of the functions in the class.
            viz_name (str): Name to save the visualisation under.
        """
        with st.spinner("Crafting the visualisation..."):
            st.download_button(
                label="Save viz",
                data=figure,
                file_name=viz_name,
                icon=":material/analytics:",
                mime="image/png",
            )

    # Function that takes the Squad Depth viz, adds styling to the existing viz, and sends it to the user
    def squad_depth(self, figure: Figure, selected_team: str) -> Figure:
        # Set the fig's title
        figure.suptitle(
            y=0.9,
            t=f"{selected_team} | 2024-25 A-League Women Squad Depth",
            color=palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )

        # Set the fig's footnote
        figure.text(
            0.02,
            0.03,
            "Data from FBref\nCreated with ALW Recruitment Dashboard (alw-recruitment-dashboard.streamlit.app) | By Daryl/Talking Tactics",
            ha="left",
            color=palette["text-color"],
            fontsize=8,
            fontproperties=import_fonts(weight="regular"),
        )

        # Save the fig to a BytesIO object
        buf = io.BytesIO()
        figure.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        plt.close(figure)

        # Send the viz to the download button
        viz_name: str = f"{selected_team.replace(" ", "_").lower()}_squad_depth.png"
        self.button_init(buf, viz_name)

    # Function that creates the bar charts from the Similar Players page
    # Potentially has two modes: grids for all raw percentiles and single for similarity ranking

    # Function that uses PyPizza to create the Role Rating pizza chart

    # Function that creates the Data Dashboard using grid
