""" """

# Imports
import streamlit as st
import pandas as pd

# Custom modules
from styles import Styles

# Get colour palette
styles: Styles = Styles()
styles.set_style(st.session_state.theme)
palette: dict = styles.get_style(style=st.session_state.theme)
