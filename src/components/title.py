# Streamlit code for the title header component

# Import necessary libraries
import streamlit as st


# Main function to create the title header
def title_header(
    page_title: str = "",
    text_1: str = "",
    text_2: str = None,
    image_path: str | None = None,
    image_width: int = 150,
) -> None:
    """
    Reusable title header component for Streamlit apps.

    Args:
        page_title (str): Page title on the nav bar.
        text_1 (str): The first line of the title.
        text_2 (str, optional): The second line of the title.
        image_path (str | None): Path to an optional image to display alongside the title. Defaults to None.
        image_width (int): Width of the image if provided. Defaults to 150.

    Returns:
        None: Renders the title header in the Streamlit app.
    """

    # Set up page
    st.set_page_config(
        page_title=page_title,
    )

    # Create two columns for the header
    col1, col2 = (
        st.columns([0.13, 1]) if image_path is not None else st.columns([1, 0.01])
    )

    with col2 if image_path is not None else col1:
        st.html(
            (
                f"""
                <h1 style='font-size:2.5em;'>
                {text_1}<br />
                {text_2 if text_2 != "" or text_2 is not None else ""}
                </h1>
                """
            )
        )

    if image_path is not None:
        with col1:
            st.image(image_path, width=image_width)
