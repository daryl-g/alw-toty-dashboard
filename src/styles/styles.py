# CSS-imitated code for styling the Streamlit app

# Import necessary libraries
import streamlit as st


# Class to manage the CSS styles
class Styles:

    # Class constructor
    def __init__(self):
        pass

    # Return the CSS styles
    def style_init(self, style_dict: dict):
        """
        Initialize the CSS styles for the Streamlit app.

        Args:
            style_dict (dict): Dictionary with colour palette.
        Returns:
            st.html: CSS styles as a string.
        """
        return st.html(
            f"""
        <style>

        /* Reduce top padding of the main block */
        {self.main_block()}
        
        /* Set global background and text color */
        {self.global_bg_text(
            body_bg=style_dict["bg-color"],
            main_bg=style_dict["bg-color"],
            body_text=style_dict["text-color"],
            p_text=style_dict["text-color"]
        )}

        /* Header banner (top section) */
        {self.header(
            header_bg=style_dict["bg-color"],
            text_color=style_dict["text-color"]
        )}

        /* Input boxes */
        {self.input_boxes()}

        /* Buttons */
        {self.buttons()}

        /* Collapsed sidebar button */
        {self.sidebar_button()}

        /* Progress bar */
        {self.progress_bar()}

        /* Header text */
        {self.header_text(
            header_color=style_dict["title-color"]
        )}

        /* List items */
        {self.list_items(
            ul_text=style_dict["text-color"]
        )}

        /* Link text */
        {self.link_text()}

        /* Sidebar */
        {self.sidebar(
            sidebar_bg=style_dict["secondary-bg"],
            sidebar_text=style_dict["text-color"],
            sidebar_link=style_dict["text-color"]
        )}

        /* Alert box */
        /* {self.alert_box()} */

        /* Spinner */
        {self.spinner()}

        /* Expander */
        {self.expander(
            expander_text=style_dict["text-color"],
            summary_bg=style_dict['bg-color'],
            summary_border=style_dict["border-color"],
            focused_summary_bg=style_dict["secondary-bg"],
            focused_summary_text=style_dict["text-color"],
            hovered_summary_bg=style_dict['title-color'],
            hovered_summary_text=style_dict['bg-color']
        )}

        /* Other UI elements */
        {self.others(
            toolbar_bg=style_dict["bg-color"],
            toolbar_text=style_dict["text-color"],
            nav_text=style_dict["text-color"],
            widget_label_text=style_dict["text-color"],
            widget_help=style_dict["text-color"]
        )}

        /* Add new styles here as needed */

        </style>
        """,
        )

    # Get a dictionary of style elements
    def get_style(self, style: str) -> dict:
        """
        Get palette colours in a dictionary.

        Args:
            style (str): Which palette to return? Options are 'light', 'dark', 'tokyo'.

        Returns:
            (dict): Dictionary with colour palette elements.
        """

        if style.lower() not in ["light", "dark", "tokyo"]:
            raise ValueError(
                "Unknown style option. Please choose from 'light', 'dark', 'tokyo'."
            )

        if style == "light":
            return {
                "bg-color": "#e4e5f1",
                "secondary-bg": "#9394a5",
                "text-color": "#010101",
                "primary-color": "#a8e6cf",
                "secondary-color": "#ffd3b6",
                "third-color": "#ff8b94",
                "low-value-color": "#dd3636",
                "med-value-color": "#f08022",
                "high-value-color": "#33c771",
                "title-color": "#010101",
                "border-color": "#010101",
                "line-color": "#010101",
            }
        elif style == "dark":
            return {
                "bg-color": "#121212",
                "secondary-bg": "#252526",
                "text-color": "#fafafa",
                "primary-color": "#c40289",
                "secondary-color": "#133e7c",
                "third-color": "#493267",
                "low-value-color": "#dd3636",
                "med-value-color": "#ea7600",
                "high-value-color": "#33c771",
                "title-color": "#fafafa",
                "border-color": "#ffffff",
                "line-color": "#ffffff",
            }
        elif style == "tokyo":
            return {
                "bg-color": "#01011b",
                "secondary-bg": "#11073c",
                "primary-color": "#c40289",
                "secondary-color": "#133e7c",
                "third-color": "#493267",
                "low-value-color": "#ee138c",
                "med-value-color": "#ea7600",
                "high-value-color": "#00ffd2",
                "text-color": "#ffffff",
                "title-color": "#ff0091",
                "border-color": "#00ffff",
                "line-color": "#004687",
            }

    # Set the global style
    def set_style(self, style: str = "dark") -> None:
        """
        Set the global style based on the variable passed down.

        Args:
            style (str): User chosen style. Options include `light`, `dark`, `tokyo`. Default is "dark" for dark mode.

        Return:
            None: Style class receives global style variable.
        """
        if style.lower() not in ["light", "dark", "tokyo"]:
            raise ValueError(
                "Unknown style option. Please choose from 'light', 'dark', 'tokyo'."
            )

        style_dict: dict = self.get_style(style)
        self.style_init(style_dict)

    # Reduce padding of the main block container
    def main_block(self) -> str:
        return """
        .stMainBlockContainer {
            padding-top: 4.5rem;
        }
        """

    # Set global background and text colour
    def global_bg_text(
        self,
        body_bg: str = "#01011b",
        body_text: str = "#ffffff",
        p_text: str = "#ffffff",
        main_bg: str = "#01011b",
    ) -> str:
        """
        Set global background and text colour.

        Args:
            body_bg (str): Body background colour. Default is dark blue (#060621).
            body_text (str): Body text colour. Default is white (#ffffff).
            p_text (str): Paragraph text colour. Default is white (#ffffff).
            main_bg (str): Main container background colour. Default is dark blue (#060621).
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
    def header(self, header_bg: str = "#01011b", text_color: str = "#ffffff") -> str:
        return """
        header {
            background-color: %s !important;  /* Header background */
            color: %s !important;  /* Header text color */
        }
        """ % (
            header_bg,
            text_color,
        )

    # Input boxes styles
    def input_boxes(
        self, input_bg: str = "#ffffff", input_text: str = "#000000"
    ) -> str:
        return """
        .stTextInput, .stTextArea, .stNumberInput, .stDateInput {
            background-color: %s !important;  /* Input box background */
            color: %s !important;  /* Input box text color */
        }
        """ % (
            input_bg,
            input_text,
        )

    # Buttons styles
    def buttons(
        self,
        button_text: str = "#ffffff",
        button_bg: str = "#11523d",
        button_border: str = "#11523d",
        button_hover_bg: str = "#0d3f2f",
        button_hover_border: str = "#0d3f2f",
    ) -> str:
        return """
        .stButton > button {
            color: %s !important;  /* Button text color */
            background-color: %s !important;  /* Button background */
            border-color: %s !important;  /* Button border color */
        }
        .stButton > button:hover {
            background-color: %s !important;  /* Button hover background */
            border-color: %s !important;  /* Button hover border color */
        }
        """ % (
            button_text,
            button_bg,
            button_border,
            button_hover_bg,
            button_hover_border,
        )

    # Sidebar styles
    def sidebar(
        self,
        sidebar_bg: str = "#11073c",
        sidebar_text: str = "#ff8303",
        sidebar_link: str = "#00ffd2",
    ) -> str:
        return """
        .stSidebar {
            background-color: %s !important;  /* Sidebar background */
            color: %s !important;  /* Sidebar text color */
        }

        .stSidebar > div > div > ul > div > li > div > a > span {
            color: %s !important;  /* Sidebar link color */
        }
        """ % (
            sidebar_bg,
            sidebar_text,
            sidebar_link,
        )

    # Collapsed sidebar button styles
    def sidebar_button(
        self,
        collapsed_btn_bg: str = "#11523d",
        collapsed_btn_border: str = "#11523d",
        collapsed_btn_hover: str = "#ff8303",
        collapsed_btn_hover_border: str = "#0d3f2f",
    ) -> str:
        return """
        .stAppViewContainer > div > div > button {
            background-color: %s !important;  /* Sidebar collapsed button background */
            border-color: %s !important;  /* Sidebar collapsed button border color */
        }
        .stAppViewContainer > div > div > button:hover {
            background-color: %s !important;  /* Sidebar collapsed button hover background */
            border-color: %s !important;  /* Sidebar collapsed button hover border color */ 
        }

        .stSidebarContent > .stSidebarUserContent > p {
            color: black !important
        }
        """ % (
            collapsed_btn_bg,
            collapsed_btn_border,
            collapsed_btn_hover,
            collapsed_btn_hover_border,
        )

    # Progress bar styles
    def progress_bar(self, progress_bg: str = "#ff9d09") -> str:
        return """
        .stProgress > div > div > div > div {
            background-color: %s !important;  /* Progress bar color */
        }
        """ % (
            progress_bg
        )

    # Header text styles
    def header_text(self, header_color: str = "#ff4499") -> str:
        return """
        h1, h2, h3, h4 {
            color: %s !important;  /* Header text color */
        }
        """ % (
            header_color
        )

    # List item styles
    def list_items(self, ul_text: str = "#ffffff") -> str:
        return """
        .stMarkdown > div > ul {
            color: %s !important;  /* List item text color */
        }
        """ % (
            ul_text
        )

    # Link text styles
    def link_text(self, a_text: str = "#ff8e03") -> str:
        return """
        .stMarkdown > div > a, .stMarkdown > div > ul > a {
            color: %s !important;  /* Link text color */
        }
        """ % (
            a_text
        )

    # Alert box styles
    def alert_box(
        self,
        alert_bg: str = "#11523d",
        alert_text: str = "#ffffff",
    ) -> str:
        return """
        .stAlert {
            background-color: %s !important;  /* Alert box background */
            color: %s !important;  /* Alert box text color */
            border-radius: 10px;  /* Alert box border radius */
        }
        """ % (
            alert_bg,
            alert_text,
        )

    # Spinner styles
    def spinner(self, spinner_text: str = "#11523d") -> str:
        return """
        .stSpinner > div > div > p {
            color: %s !important;  /* Spinner text color */
        }
        """ % (
            spinner_text
        )

    # Spinner styles
    def expander(
        self,
        expander_text: str = "#11523d",
        summary_bg: str = "#000000",
        summary_border: str = "#000000",
        focused_summary_bg: str = "#ffffff",
        focused_summary_text: str = "#000000",
        hovered_summary_bg: str = "#000000",
        hovered_summary_text: str = "#ffffff",
    ) -> str:
        return """
        .stExpander {
            color: %s !important;  /* Expander text color */
        }

        .stExpander > details > summary {
            background-color: %s !important; /* Expander summary background color */
            border-color: %s !important; /* Expander border color */
        }

        .stExpander > details > summary:focus, summary:focus-within {
            background-color: %s !important; /* Expander summary background color */
            color: %s !important; /* Expander summary text color */
        }

        .stExpander > details > summary:hover {
            background-color: %s !important;
            color: %s !important
        }
        """ % (
            expander_text,
            summary_bg,
            summary_border,
            focused_summary_bg,
            focused_summary_text,
            hovered_summary_bg,
            hovered_summary_text,
        )

    # Other UI elements styles
    def others(
        self,
        toolbar_bg: str = "#11523d",
        toolbar_text: str = "#ff8303",
        nav_text: str = "#ffffff",
        widget_label_text: str = "#ff8e03",
        widget_help: str = "#ffffff",
    ) -> str:
        return """
        .stAppToolbar {
            background-color: %s !important;  /* Sidebar and toolbar background */
            color: %s !important;  /* Sidebar and toolbar text color */
        }

        .stAppToolbar > div > div > div.rc-overflow-item > div > div {
            color: %s !important;  /* Nav text color */
        }

        .stDateInput > label, .stButtonGroup > label {
            color: %s !important;  /* Widgets label color */
        }

        .stButtonGroup > label > label > .stTooltipIcon > .stTooltipHoverTarget > svg.icon {
            stroke: %s !important; /* Widget help button color */
        }
        """ % (
            toolbar_bg,
            toolbar_text,
            nav_text,
            widget_label_text,
            widget_help,
        )
