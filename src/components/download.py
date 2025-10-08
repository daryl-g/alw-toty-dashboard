# Wrapper and logic for the download button

# Imports
import io
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.patches as patches

from mplsoccer import PyPizza
from matplotlib.figure import Figure

from services import scatter_data
from styles import Styles
from utils import import_fonts


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
        # Initially intended to control the switch between the functions that create the viz
        # but can't find a place for this to be used anymore.
        # Will delete it at some point.
        self.page = page

        # Get colour palette
        styles: Styles = Styles()
        self.palette: dict = styles.get_style(style=st.session_state.theme)
        self.buf: io.BytesIO = io.BytesIO()

    def button_init(self, figure: io.BytesIO, viz_name: str) -> None:
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
    def squad_depth(self, figure: Figure, selected_team: str) -> None:
        """ """
        # Input checking

        # Set the fig's title
        figure.suptitle(
            y=0.9,
            t=f"{selected_team} | 2024-25 A-League Women Squad Depth",
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )

        # Set the fig's footnote
        figure.text(
            0.02,
            0.03,
            "Data from FBref\nCreated with ALW Recruitment Dashboard (alw-recruitment-dashboard.streamlit.app) | By Daryl/Talking Tactics",
            ha="left",
            color=self.palette["text-color"],
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
    ) -> None:
        """ """
        # Input checking

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
                color=self.palette["text-color"],
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
        ax.tick_params(labelcolor=self.palette["text-color"])
        for label in ax.get_xticklabels():
            label.set_fontproperties(import_fonts(weight="light"))
        for label in ax.get_yticklabels():
            label.set_fontsize(18)
            label.set_fontproperties(import_fonts(weight="bold")),
        # Turn off top and right spines
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        # Change color of the spines
        ax.spines["bottom"].set_color(self.palette["border-color"])
        ax.spines["left"].set_color(self.palette["border-color"])
        # Add x gridlines
        ax.xaxis.grid(
            True,
            color=self.palette["border-color"],
            linestyle="--",
            alpha=0.3,
            which="major",
        )

        # Set x-axis label
        ax.set_xlabel(
            "Similarity Rating (%)",
            fontdict={
                "fontsize": 14,
                "color": self.palette["text-color"],
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
                "color": self.palette["text-color"],
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
                "color": self.palette["text-color"],
            },
            fontproperties=import_fonts(weight="regular"),
        )
        # Set the fig's footnote
        ax.text(
            105,
            len(similarity_df.index) + 2,
            "Data from FBref\nCreated with ALW Recruitment Dashboard (alw-recruitment-dashboard.streamlit.app) | By Daryl/Talking Tactics",
            ha="right",
            color=self.palette["text-color"],
            fontsize=8,
            fontproperties=import_fonts(weight="regular"),
        )

        # Set the background facecolor
        similarity_fig.set_facecolor(self.palette["bg-color"])
        ax.set_facecolor(self.palette["bg-color"])

        # Save the fig to a BytesIO object
        similarity_fig.savefig(self.buf, format="png", dpi=300, bbox_inches="tight")
        self.buf.seek(0)
        plt.close(similarity_fig)

        # Send the viz to the download button
        viz_name: str = f"{player_name.replace(" ", "_").lower()}_similar_players.png"
        self.button_init(self.buf, viz_name)

    # Function that uses PyPizza to create the Role Rating pizza chart
    def pizza_baker(
        self,
        role_ratings: dict,
        player_name: str,
        selected_team: str,
        player_position: str,
        min_90s: int,
    ) -> None:
        # Input checking

        # Extract data from the role_ratings dict
        metrics_group: list = list(role_ratings.keys())
        metrics_group.remove("Overall")
        num_stats: int = len(metrics_group)
        metrics_values: list = list(role_ratings.values())[:-1]
        overall_rating: float = role_ratings["Overall"]

        # Create the array for colours
        slice_colours = [self.palette["primary-color"]] * num_stats
        blank_colours = [self.palette["secondary-bg"]] * num_stats
        text_colours = [self.palette["text-color"]] * num_stats

        # Initiate the PyPizza class with the relevant metrics
        baker = PyPizza(
            params=metrics_group,
            background_color=self.palette["bg-color"],
            straight_line_color=self.palette["border-color"],
            straight_line_lw=1,
            last_circle_lw=0,
            other_circle_ls="--",
            other_circle_lw=1,
            inner_circle_size=20,
        )

        # Make the pizza chart with the given metrics and stylings
        pizza_fig, ax = baker.make_pizza(
            values=metrics_values,
            figsize=(12, 12),
            color_blank_space=blank_colours,
            slice_colors=slice_colours,
            value_colors=text_colours,
            blank_alpha=0.4,
            kwargs_slices=dict(
                edgecolor=self.palette["border-color"], zorder=2, linewidth=1
            ),
            kwargs_params=dict(
                color=self.palette["text-color"],
                fontsize=15,
                va="center",
                fontproperties=import_fonts(weight="bold"),
            ),
            kwargs_values=dict(
                color=self.palette["text-color"],
                fontsize=16,
                fontproperties=import_fonts(weight="bold"),
                zorder=3,
                bbox=dict(
                    edgecolor=self.palette["border-color"],
                    facecolor=self.palette["secondary-color"],
                    boxstyle="round,pad=0.2",
                    lw=1,
                ),
            ),
        )

        # Add overall rating to the middle of the radar chart
        pizza_fig.text(
            0.512,
            0.49,
            "Overall\nrating:\n{ovrRating}".format(ovrRating=overall_rating),
            ha="center",
            va="center",
            fontsize=20,
            color=self.palette["text-color"],
            fontproperties=import_fonts(weight="bold"),
        )

        # add title
        pizza_fig.text(
            0.515,
            1.00,
            f"{player_name} - {selected_team}",
            size=22,
            ha="center",
            fontproperties=import_fonts(weight="bold"),
            color=self.palette["title-color"],
        )

        # add subtitle
        pizza_fig.text(
            0.515,
            0.95,
            f"Position Rating vs {player_position} with minimum {min_90s} 90s played\n2024-25 A-League Women",
            size=16,
            ha="center",
            fontproperties=import_fonts(weight="bold"),
            color=self.palette["text-color"],
        )
        # Set the fig's footnote
        pizza_fig.text(
            0.93,
            0.05,
            "Data from FBref\nCreated with ALW Recruitment Dashboard (alw-recruitment-dashboard.streamlit.app) | By Daryl/Talking Tactics",
            ha="right",
            color=self.palette["text-color"],
            fontsize=8,
            fontproperties=import_fonts(weight="regular"),
        )

        # Save the fig to a BytesIO object
        pizza_fig.savefig(self.buf, format="png", dpi=300, bbox_inches="tight")
        self.buf.seek(0)
        plt.close(pizza_fig)

        # Send the viz to the download button
        viz_name: str = f"{player_name.replace(" ", "_").lower()}_role_ratings.png"
        self.button_init(self.buf, viz_name)

    # Function that creates the Data Dashboard using grid
    def data_dashboard(
        self,
        minutes_played: int,
        played_90s: float,
        role_ratings: dict,
        overall_ratings: dict,
        metrics_selections: list,
        player_name: str,
        selected_team: str,
        player_position: str,
        min_90s: int,
    ) -> None:
        # Create the figure
        dashboard_fig = plt.figure(figsize=(34, 20))

        # Player info (top left)
        info_ax = dashboard_fig.add_subplot(2, 3, 1)
        # Add border and remove axes
        info_ax.add_patch(
            patches.FancyBboxPatch(
                (0.1, 0.1),
                0.8,
                0.8,
                boxstyle="round,pad=0.1",
                edgecolor=self.palette["border-color"],
                facecolor="none",
                linewidth=2,
            )
        )
        info_ax.axis("off")

        # Add texts
        info_ax.text(
            x=0.05,
            y=0.75,
            s=f"{player_name} ({player_position})\n{selected_team}",
            color=self.palette["text-color"],
            fontsize=35,
            fontproperties=import_fonts(weight="bold"),
        )
        info_ax.plot(
            [0.05, 0.95],
            [0.7, 0.7],
            linestyle="-",
            linewidth=2,
            color=self.palette["border-color"],
        )
        info_ax.text(
            x=0.05,
            y=0.58,
            s=f"Compared against players at\n{"LW and LM" if player_position in ["LW", "LM"] else "RW and RM" if player_position in ["RW", "RM"] else player_position} with {min_90s} or more 90s.",
            color=self.palette["text-color"],
            fontsize=23,
            fontproperties=import_fonts(weight="regular"),
        )
        info_ax.text(
            x=0.05,
            y=0.5,
            s=f"Minutes played: {minutes_played} mins",
            color=self.palette["text-color"],
            fontsize=23,
            fontproperties=import_fonts(weight="regular"),
        )
        info_ax.text(
            x=0.05,
            y=0.43,
            s=f"90s: {played_90s} 90s",
            color=self.palette["text-color"],
            fontsize=23,
            fontproperties=import_fonts(weight="regular"),
        )
        # Set the fig's footnote
        info_ax.text(
            0.93,
            0.07,
            "Data from FBref\nCreated with ALW Recruitment Dashboard (alw-recruitment-dashboard.streamlit.app)\nBy Daryl/Talking Tactics",
            ha="right",
            color=self.palette["text-color"],
            fontsize=10,
            fontproperties=import_fonts(weight="regular"),
        )

        # Pizza chart (middle left)
        pizza_ax = dashboard_fig.add_subplot(2, 3, 2, projection="polar")

        # Extract data from the role_ratings dict
        metrics_group: list = list(role_ratings.keys())
        metrics_group.remove("Overall")
        num_stats: int = len(metrics_group)
        metrics_values: list = list(role_ratings.values())[:-1]

        # Create the array for colours
        slice_colours = [self.palette["primary-color"]] * num_stats
        blank_colours = [self.palette["secondary-bg"]] * num_stats
        text_colours = [self.palette["text-color"]] * num_stats

        # Initiate the PyPizza class with the relevant metrics
        baker = PyPizza(
            params=metrics_group,
            background_color=self.palette["bg-color"],
            straight_line_color=self.palette["border-color"],
            straight_line_lw=1,
            last_circle_lw=0,
            other_circle_ls="--",
            other_circle_lw=1,
            inner_circle_size=20,
        )

        baker.make_pizza(
            values=metrics_values,
            figsize=(12, 12),
            ax=pizza_ax,
            color_blank_space=blank_colours,
            slice_colors=slice_colours,
            value_colors=text_colours,
            blank_alpha=0.4,
            kwargs_slices=dict(
                edgecolor=self.palette["border-color"], zorder=2, linewidth=1
            ),
            kwargs_params=dict(
                color=self.palette["text-color"],
                fontsize=15,
                va="center",
                fontproperties=import_fonts(weight="bold"),
            ),
            kwargs_values=dict(
                color=self.palette["text-color"],
                fontsize=16,
                fontproperties=import_fonts(weight="bold"),
                zorder=3,
                bbox=dict(
                    edgecolor=self.palette["border-color"],
                    facecolor=self.palette["secondary-color"],
                    boxstyle="round,pad=0.2",
                    lw=1,
                ),
            ),
        )

        # Beeswarm plot (top right)
        beeswarm_ax = dashboard_fig.add_subplot(2, 3, 3)

        sns.swarmplot(
            x=list(overall_ratings.values()),
            color=self.palette["third-color"],
            size=20,
            alpha=0.4,
            ax=beeswarm_ax,
        )
        beeswarm_ax.scatter(
            overall_ratings[player_name] - 0.15,
            0,
            color=self.palette["primary-color"],
            s=300,
        )

        beeswarm_ax.set_facecolor(self.palette["bg-color"])
        beeswarm_ax.set_xlabel(
            "Overall Rating",
            color=self.palette["text-color"],
            fontsize=20,
            fontproperties=import_fonts(weight="bold"),
        )
        beeswarm_ax.tick_params(
            length=0,
            color=self.palette["text-color"],
            labelcolor=self.palette["text-color"],
        )
        for label in beeswarm_ax.get_xticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))

        for spine in beeswarm_ax.spines.values():
            if spine.spine_type != "bottom":
                spine.set_visible(False)
            else:
                spine.set_edgecolor(self.palette["border-color"])

        # Scatter plots (bottom row)
        ## Attacking/Basic GK scatter
        att_scatter_ax = dashboard_fig.add_subplot(2, 3, 4)
        attacking_group: str = "Attacking" if player_position != "GK" else "Basic GK"
        dashboard_fig.text(
            x=0.13,
            y=0.47,
            s=attacking_group,
            color=self.palette["text-color"],
            size=25,
            fontproperties=import_fonts(weight="bold"),
        )

        attacking_data: pd.DataFrame = scatter_data(
            data_group=attacking_group,
            metrics=[metrics_selections[0], metrics_selections[1]],
            player_position=player_position,
            min_90s=min_90s,
        )

        att_scatter_ax.scatter(
            attacking_data.loc[:, metrics_selections[0]],
            attacking_data.loc[:, metrics_selections[1]],
            color=self.palette["third-color"],
            alpha=0.3,
            s=100,
        )
        # Highlight selected player's stats
        att_scatter_ax.scatter(
            attacking_data.loc[
                attacking_data["Player"] == player_name, metrics_selections[0]
            ],
            attacking_data.loc[
                attacking_data["Player"] == player_name, metrics_selections[1]
            ],
            color=self.palette["primary-color"],
            s=100,
        )
        # Add average lines
        att_scatter_ax.axvline(
            attacking_data[metrics_selections[0]].mean(),
            color=self.palette["line-color"],
            linestyle="-",
            alpha=0.3,
            linewidth=2,
        )

        att_scatter_ax.axhline(
            attacking_data[metrics_selections[1]].mean(),
            color=self.palette["line-color"],
            linestyle="-",
            alpha=0.3,
            linewidth=2,
        )

        # Set the labels and title
        att_scatter_ax.set_xlabel(
            metrics_selections[0],
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )
        att_scatter_ax.set_ylabel(
            metrics_selections[1],
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )
        att_scatter_ax.tick_params(
            color=self.palette["text-color"], labelcolor=self.palette["text-color"]
        )
        for label in att_scatter_ax.get_xticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))
        for label in att_scatter_ax.get_yticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))

        # Set the spines color and remove the top and right spines
        for spine in att_scatter_ax.spines.values():
            if spine.spine_type == "bottom" or spine.spine_type == "left":
                spine.set_edgecolor(self.palette["border-color"])
            else:
                spine.set_visible(False)

        # Set axis facecolor
        att_scatter_ax.set_facecolor(self.palette["bg-color"])

        ## Passing/Advanced GK scatter
        dist_scatter_ax = dashboard_fig.add_subplot(2, 3, 5)
        passing_group: str = "Passing" if player_position != "GK" else "Advanced GK"
        dashboard_fig.text(
            x=0.4,
            y=0.47,
            s=passing_group,
            color=self.palette["text-color"],
            size=25,
            fontproperties=import_fonts(weight="bold"),
        )

        passing_data: pd.DataFrame = scatter_data(
            data_group=passing_group,
            metrics=[metrics_selections[2], metrics_selections[3]],
            player_position=player_position,
            min_90s=min_90s,
        )

        dist_scatter_ax.scatter(
            passing_data.loc[:, metrics_selections[2]],
            passing_data.loc[:, metrics_selections[3]],
            color=self.palette["third-color"],
            alpha=0.3,
            s=100,
        )
        # Highlight selected player's stats
        dist_scatter_ax.scatter(
            passing_data.loc[
                passing_data["Player"] == player_name, metrics_selections[2]
            ],
            passing_data.loc[
                passing_data["Player"] == player_name, metrics_selections[3]
            ],
            color=self.palette["primary-color"],
            s=100,
        )
        # Add average lines
        dist_scatter_ax.axvline(
            passing_data[metrics_selections[2]].mean(),
            color=self.palette["line-color"],
            linestyle="-",
            alpha=0.3,
            linewidth=2,
        )

        dist_scatter_ax.axhline(
            passing_data[metrics_selections[3]].mean(),
            color=self.palette["line-color"],
            linestyle="-",
            alpha=0.3,
            linewidth=2,
        )

        # Set the labels and title
        dist_scatter_ax.set_xlabel(
            metrics_selections[2],
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )
        dist_scatter_ax.set_ylabel(
            metrics_selections[3],
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )
        dist_scatter_ax.tick_params(
            color=self.palette["text-color"], labelcolor=self.palette["text-color"]
        )
        for label in dist_scatter_ax.get_xticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))
        for label in dist_scatter_ax.get_yticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))

        # Set the spines color and remove the top and right spines
        for spine in dist_scatter_ax.spines.values():
            if spine.spine_type == "bottom" or spine.spine_type == "left":
                spine.set_edgecolor(self.palette["border-color"])
            else:
                spine.set_visible(False)

        # Set axis facecolor
        dist_scatter_ax.set_facecolor(self.palette["bg-color"])

        # Defending/GK Distribution scatter
        def_scatter_ax = dashboard_fig.add_subplot(2, 3, 6)
        defending_group: str = (
            "Defending" if player_position != "GK" else "Distributing"
        )
        dashboard_fig.text(
            x=0.67,
            y=0.47,
            s=defending_group,
            color=self.palette["text-color"],
            size=25,
            fontproperties=import_fonts(weight="bold"),
        )

        defending_data: pd.DataFrame = scatter_data(
            data_group=defending_group,
            metrics=[metrics_selections[4], metrics_selections[5]],
            player_position=player_position,
            min_90s=min_90s,
        )

        def_scatter_ax.scatter(
            defending_data.loc[:, metrics_selections[4]],
            defending_data.loc[:, metrics_selections[5]],
            color=self.palette["third-color"],
            alpha=0.3,
            s=100,
        )
        # Highlight selected player's stats
        def_scatter_ax.scatter(
            defending_data.loc[
                defending_data["Player"] == player_name, metrics_selections[4]
            ],
            defending_data.loc[
                defending_data["Player"] == player_name, metrics_selections[5]
            ],
            color=self.palette["primary-color"],
            s=100,
        )
        # Add average lines
        def_scatter_ax.axvline(
            defending_data[metrics_selections[4]].mean(),
            color=self.palette["line-color"],
            linestyle="-",
            alpha=0.3,
            linewidth=2,
        )

        def_scatter_ax.axhline(
            defending_data[metrics_selections[5]].mean(),
            color=self.palette["line-color"],
            linestyle="-",
            alpha=0.3,
            linewidth=2,
        )

        # Set the labels and title
        def_scatter_ax.set_xlabel(
            metrics_selections[4],
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )
        def_scatter_ax.set_ylabel(
            metrics_selections[5],
            color=self.palette["text-color"],
            fontsize=16,
            fontproperties=import_fonts(weight="bold"),
        )
        def_scatter_ax.tick_params(
            color=self.palette["text-color"], labelcolor=self.palette["text-color"]
        )
        for label in def_scatter_ax.get_xticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))
        for label in def_scatter_ax.get_yticklabels():
            label.set_fontproperties(import_fonts(weight="regular"))

        # Set the spines color and remove the top and right spines
        for spine in def_scatter_ax.spines.values():
            if spine.spine_type == "bottom" or spine.spine_type == "left":
                spine.set_edgecolor(self.palette["border-color"])
            else:
                spine.set_visible(False)

        # Set axis facecolor
        def_scatter_ax.set_facecolor(self.palette["bg-color"])

        # Set overall fig facecolor
        dashboard_fig.set_facecolor(self.palette["bg-color"])

        # Save the fig to a BytesIO object
        dashboard_fig.savefig(self.buf, format="png", dpi=300, bbox_inches="tight")
        self.buf.seek(0)
        plt.close(dashboard_fig)

        # Send the viz to the download button
        viz_name: str = f"{player_name.replace(" ", "_").lower()}_data_dashboard.png"
        self.button_init(self.buf, viz_name)
