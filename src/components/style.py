# Imports
import streamlit as st


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

    # Add theme to session state
    if "theme" not in st.session_state:
        st.session_state.theme = default_option

    st.segmented_control(
        label="Theme",
        options=options.keys(),
        format_func=lambda option: options[option],
        default=default_option,
        selection_mode="single",
        help="Change between light, dark modes, and a custom Tokyo Night theme.",
        on_change=force_selection,
    )


def force_selection() -> None:
    """
    Temporary replacement for the 'required' keyword of Streamlit's segmented_control element...until Streamlit implements it.

    Returns:
        Replace theme in session state if it is None.
    """
    default_option: str = "dark"

    if st.session_state.theme is None:
        st.session_state.theme = default_option
