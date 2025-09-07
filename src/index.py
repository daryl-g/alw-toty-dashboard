## Main entry point of the dashboard

# Imports
import streamlit as st

# Custom modules
from styles import Styles
from components import navigation

# Initialize styles
with st.spinner("Loading page styling..."):
    styles = Styles()
    styles.style_init()

# Setup navigation
navigation()

# Dashboard configs
menu_items: dict = {
    "Get Help": "https://github.com/daryl-g/alw-toty-dashboard/issues",
    "Report a Bug": "mailto:daohoang.thai@gmail.com?subject=Feedback%20for%20your%20Streamlit%20app",
    "About": "Made with ❤️ by Daryl/Talking Tactics (https://www.talking-tactics.com), 2025",
}

st.set_page_config(
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=menu_items,
)
