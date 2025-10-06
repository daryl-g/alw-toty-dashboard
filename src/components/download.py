# Wrapper and logic for the download button

# Imports
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

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
        self.buf: io.BytesIO = io.BytesIO()

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
        figure.savefig(self.buf, format="png", dpi=300, bbox_inches="tight")
        self.buf.seek(0)
        plt.close(figure)

        # Send the viz to the download button
        viz_name: str = f"{selected_team.replace(" ", "_").lower()}_squad_depth.png"
        self.button_init(self.buf, viz_name)

    # Function that creates the bar charts from the Similar Players page
    # Potentially has two modes: grids for all raw percentiles and single for similarity ranking
    def similarity_bar(
        self,
        similarity_df: pd.DataFrame,
        player_name: str,
        selected_team: str,
        player_position: str,
        min_90s: int,
    ) -> Figure:
        # Create the figure
        similarity_fig, ax = plt.subplots(figsize=(12, 15))

        # Normalize data to [0, 1] range for colormap
        norm = colors.Normalize(vmin=similarity_df.min(), vmax=similarity_df.max())
        # Get colormap
        cmap = plt.get_cmap("RdBu")

        # Draw the bar chart
        ax.barh(
            y=similarity_df.index,
            width=similarity_df,
            color=cmap(norm(similarity_df)),
        )
        # Display values at the end of each bar
        for i, v in enumerate(similarity_df):
            ax.text(
                v + 1,
                i,
                f"{v}%",
                color=palette["text-color"],
                fontproperties=import_fonts(weight="bold"),
                fontsize=12,
                va="center",
            )

        # Set axis limits
        ax.set_ylim(-1, len(similarity_df.index))
        ax.set_xlim(0, 105)
        # Invert y-axis for the highest values
        ax.invert_yaxis()
        # Change color and font of axis labels
        ax.tick_params(labelcolor=palette["text-color"])
        for label in ax.get_xticklabels():
            label.set_fontproperties(import_fonts(weight="light"))
        for label in ax.get_yticklabels():
            label.set_fontsize(18)
            label.set_fontproperties(import_fonts(weight="bold")),
        # Turn off top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        # Change color of the spines
        ax.spines["bottom"].set_color(palette["border-color"])
        ax.spines["left"].set_color(palette["border-color"])
        # Add x gridlines
        ax.xaxis.grid(
            True,
            color=palette["border-color"],
            linestyle="--",
            alpha=0.3,
            which="major",
        )

        # Set x-axis label
        ax.set_xlabel(
            "Similarity Rating (%)",
            fontdict={
                "fontsize": 14,
                "color": palette["text-color"],
            },
            fontproperties=import_fonts(weight="bold"),
        )
        # Set title
        ax.set_title(
            f"Similar Players to {player_name} ({selected_team})",
            loc="left",
            pad=30,
            fontdict={
                "fontsize": 25,
                "color": palette["text-color"],
            },
            fontproperties=import_fonts(weight="bold"),
        )
        # Set subtitle
        ax.text(
            0,
            1.02,
            f"Players with {min_90s} or more 90s at {player_position}",
            transform=ax.transAxes,
            fontdict={
                "fontsize": 10,
                "color": palette["text-color"],
            },
            fontproperties=import_fonts(weight="regular"),
        )
        # Set the fig's footnote
        ax.text(
            105,
            len(similarity_df.index) + 2,
            "Data from FBref\nCreated with ALW Recruitment Dashboard (alw-recruitment-dashboard.streamlit.app) | By Daryl/Talking Tactics",
            ha="right",
            color=palette["text-color"],
            fontsize=8,
            fontproperties=import_fonts(weight="regular"),
        )

        # Set the background facecolor
        similarity_fig.set_facecolor(palette["bg-color"])
        ax.set_facecolor(palette["bg-color"])

        # Save the fig to a BytesIO object
        similarity_fig.savefig(self.buf, format="png", dpi=300, bbox_inches="tight")
        self.buf.seek(0)
        plt.close(similarity_fig)

        # Send the viz to the download button
        viz_name: str = f"{player_name.replace(" ", "_").lower()}_similar_players.png"
        self.button_init(self.buf, viz_name)

    # Function that uses PyPizza to create the Role Rating pizza chart

    # Function that creates the Data Dashboard using grid
