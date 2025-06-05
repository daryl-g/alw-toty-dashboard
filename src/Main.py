## Main entry point of the dashboard

# Imports
import streamlit as st

# Dashboard configs
menu_items: dict = {
    "Get Help": "https://github.com/daryl-g/alw-toty-dashboard/issues",
    "Report a Bug": "mailto:daohoang.thai@gmail.com&subject=Feedback%20for%20your%20Streamlit%20app",
    "About": "Made with ❤️ by Daryl/Talking Tactics, 2025",
    "Source Code": "https://github.com/daryl-g/alw-toty-dashboard",
}

st.set_page_config(
    page_title="A-League Women's 2025 TOTS Dashboard",
    page_icon=":trophy:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=menu_items,
)

# Load README file
readme = open("assets/title_readme.md", "r", encoding="utf-8").read()
st.markdown(readme)
