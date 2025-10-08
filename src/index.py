## Main entry point of the dashboard

# Imports
import streamlit as st

# Set default theme
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Custom modules
from components import navigation

# Setup navigation
navigation()

# Dashboard configs
menu_items: dict = {
    "Get Help": "https://github.com/daryl-g/alw-toty-dashboard/issues",
    "Report a Bug": "mailto:daohoang.thai@gmail.com?subject=Feedback%20for%20your%20Streamlit%20app",
    "About": "Made with ❤️ by Daryl/Talking Tactics (https://daryldao.com & https://www.talking-tactics.com), 2025",
}

st.set_page_config(
    page_icon=":soccer:",
    layout="wide",
    menu_items=menu_items,
)
