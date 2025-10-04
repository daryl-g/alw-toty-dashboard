# Imports
import streamlit as st


# Custom navigation component
def navigation() -> None:
    """
    Custom wrapper for Streamlit's navigation element.

    Returns:
        (None): Renders the page with the navigation component on the left.
    """
    pages = {
        "Home": [
            st.Page(
                page="pages/home.py",
                title="Home",
                icon=":material/sports_and_outdoors:",
                default=True,
            )
        ],
        "Squad Planner": [
            st.Page(
                page="pages/squad_depth.py",
                title="Squad Depth",
                icon=":material/groups_2:",
                url_path="squad_depth",
            ),
            st.Page(
                page="pages/role_ratings.py",
                title="Position Rating",
                icon=":material/123:",
                url_path="role_rating",
            ),
        ],
        "Player Data": [
            st.Page(
                page="pages/similar_players.py",
                title="Similar Players",
                icon=":material/safety_divider:",
                url_path="player_similarity",
            ),
            st.Page(
                page="pages/data_dashboard.py",
                title="Data Dashboard",
                icon=":material/team_dashboard:",
                url_path="player_dashboard",
            ),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()
