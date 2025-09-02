## Main entry point of the dashboard

# Imports
import streamlit as st

# Custom modules
from styles import Styles
from components import title_header
from utils import display_markdown

# Custom styling
styles = Styles()
styles.style_init()

# Dashboard configs
menu_items: dict = {
    "Get Help": "https://github.com/daryl-g/alw-toty-dashboard/issues",
    "Report a Bug": "mailto:daohoang.thai@gmail.com?subject=Feedback%20for%20your%20Streamlit%20app",
    "About": "Made with ❤️ by Daryl/Talking Tactics (https://www.talking-tactics.com), 2025",
}

st.set_page_config(
    page_title="A-League Women Recruitment Dashboard",
    page_icon=":soccer:",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=menu_items,
)

# Set up app header
title_header(
    "A-League Women",
    "Recruitment Dashboard",
    image_path="src/assets/imgs/ALW_logo.png",
    image_width=75,
)
st.markdown("---")

display_markdown("src/assets/texts/title_readme.md")
