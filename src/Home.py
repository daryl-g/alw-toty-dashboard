## Main entry point of the dashboard

# Imports
import streamlit as st

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

# Load README file
readme = open("src/assets/title_readme.md", "r", encoding="utf-8").read()
st.markdown(readme)
