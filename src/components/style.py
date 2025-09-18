# Imports
import streamlit as st

# Custom style module
from styles import Styles

# Initialise style module
styles = Styles()


# Switch themes
def theme_switcher():
    """
    Theme switcher component, also a wrapper for Streamlit's segmented_control element.

    Returns:
        (None): 'theme' and 'refreshed' are passed through the session state.
    """
    # Theme switching logic goes here

    # Switcher component
    options: dict = {
        "light": ":material/light_mode:",
        "dark": ":material/dark_mode:",
        "tokyo": ":material/location_city:",
    }
    default_option: str = "dark"

    if "theme" not in st.session_state:
        st.session_state.theme = default_option

    style = st.segmented_control(
        label="Theme",
        options=options.keys(),
        format_func=lambda option: options[option],
        default=(
            st.session_state.theme
            if st.session_state.theme is not None
            else default_option
        ),
        selection_mode="single",
        help="Change between light, dark modes, and a custom Tokyo Night/Cyberpunk theme.",
    )

    # Change styling
    st.session_state.theme = style if style is not None else default_option
    styles.set_style(st.session_state.theme)
