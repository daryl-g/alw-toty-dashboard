# CSS-imitated code for styling the Streamlit app

# Import necessary libraries
import streamlit as st


# Class to manage the CSS styles
class Styles:

    # Class constructor
    def __init__(self):
        pass

    # Return the CSS styles
    def style_init(self):
        """
        Initialize the CSS styles for the Streamlit app.

        Returns
        -------
        st.markdown
            CSS styles as a string.
        """
        return st.html(
            f"""
        <style>
        
        /* Set global background and text color */
        {self.global_bg_text()}

        /* Header banner (top section) */
        {self.header()}

        /* Input boxes */
        {self.input_boxes()}

        /* Buttons */
        {self.buttons()}

        /* Collapsed sidebar button */
        {self.sidebar_button()}

        /* Progress bar */
        {self.progress_bar()}

        /* Header text */
        {self.header_text()}

        /* List items */
        {self.list_items()}

        /* Link text */
        {self.link_text()}

        /* Sidebar */
        {self.sidebar()}

        /* Alert box */
        {self.alert_box()}

        /* Spinner */
        {self.spinner()}

        /* Other UI elements */
        {self.others()}

        /* Add new styles here as needed */

        </style>
        """,
        )

    # Set global background and text color
    def global_bg_text(
        self,
        body_bg: str = "#060621",
        body_text: str = "#ffffff",
        p_text: str = "#ffffff",
        main_bg: str = "#060621",
    ) -> str:
        """
        Set global background and text color.

        Args:
            body_bg (str): Body background color. Default is dark blue (#060621).
            body_text (str): Body text color. Default is white (#ffffff).
            p_text (str): Paragraph text color. Default is white (#ffffff).
            main_bg (str): Main container background color. Default is dark blue (#060621).
        """
        return """
        body {
            background-color: %s !important;  /* Main background */
            color: %s !important;  /* Global text color */
        }

        .stMarkdown > div > p {
            color: %s !important;  /* Global text color */
        }

        .stMain {
            background-color: %s !important;  /* Main container background */
        }
        """ % (
            body_bg,
            body_text,
            p_text,
            main_bg,
        )

    # Header banner styles
    def header(self) -> str:
        return """
        header {
            background-color: #060621 !important;  /* Header background */
            color: white !important;  /* Header text color */
        }
        """

    # Input boxes styles
    def input_boxes(self) -> str:
        return """
        .stTextInput, .stTextArea, .stNumberInput, .stDateInput {
            background-color: white !important;  /* Input box background */
            color: black !important;  /* Input box text color */
        }
        """

    # Buttons styles
    def buttons(self) -> str:
        return """
        .stButton > button {
            color: white !important;  /* Button text color */
            background-color: #11523d !important;  /* Button background */
            border-color: #11523d !important;  /* Button border color */
        }
        .stButton > button:hover {
            background-color: #0d3f2f !important;  /* Button hover background */
            border-color: #0d3f2f !important;  /* Button hover border color */
        }
        """

    # Sidebar styles
    def sidebar(self) -> str:
        return """
        .stSidebar {
            background-color: #11073c !important;  /* Sidebar background */
            color: #ff8e03 !important;  /* Sidebar text color */
        }

        .stSidebar > div > div > ul > div > li > div > a > span {
            color: #00ffd2 !important;  /* Sidebar link color */
        }
        """

    # Collapsed sidebar button styles
    def sidebar_button(self) -> str:
        return """
        .stAppViewContainer > div > div > button {
            background-color: #11523d !important;  /* Sidebar collapsed button background */
            border-color: #11523d !important;  /* Sidebar collapsed button border color */
        }
        .stAppViewContainer > div > div > button:hover {
            background-color: #ff8e03 !important;  /* Sidebar collapsed button hover background */
            border-color: #0d3f2f !important;  /* Sidebar collapsed button hover border color */ 
        }
        """

    # Progress bar styles
    def progress_bar(self) -> str:
        return """
        .stProgress > div > div > div > div {
            background-color: #ff9d09 !important;  /* Progress bar color */
        }
        """

    # Header text styles
    def header_text(self) -> str:
        return """
        h1, h2, h3, h4 {
            color: #ff4499 !important;  /* Header text color */
        }
        """

    # List item styles
    def list_items(self) -> str:
        return """
        .stMarkdown > div > ul {
            color: white !important;  /* List item text color */
        }
        """

    # Link text styles
    def link_text(self) -> str:
        return """
        .stMarkdown > div > a, .stMarkdown > div > ul > a {
            color: #ff8e03 !important;  /* Link text color */
        }
        """

    # Alert box styles
    def alert_box(self) -> str:
        return """
        .stAlert {
            background-color: #11523d !important;  /* Alert box background */
            color: white !important;  /* Alert box text color */
            border-radius: 10px;  /* Alert box border radius */
        }
        """

    # Spinner styles
    def spinner(self) -> str:
        return """
        .stSpinner > div > div > p {
            color: #11523d !important;  /* Spinner text color */
        }
        """

    # Other UI elements styles
    def others(self) -> str:
        return """
        .stToolbar {
            background-color: #11523d !important;  /* Sidebar and toolbar background */
            color: #ff8e03 !important;  /* Sidebar and toolbar text color */
        }

        .stDateInput > label {
            color: #ff8e03 !important;  /* Date input label color */
        }
        """
