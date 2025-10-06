# Streamlit code for the title header component

# Import necessary libraries
import streamlit as st


# Main function to create the title header
def title_header(
    page_title: str = "",
    text_1: str = "",
    text_2: str = None,
    image_path: str | None = None,
    image_width: int = 5.7,
    image_height: int = 10,
) -> None:
    """
    Reusable title header component for Streamlit apps.

    Args:
        page_title (str): Page title on the nav bar.
        text_1 (str): The first line of the title.
        text_2 (str, optional): The second line of the title.
        image_path (str | None): Path to an optional image to display alongside the title. Defaults to None.
        image_width (int): Width of the image in rem if provided. Defaults to 150.

    Returns:
        None: Renders the title header in the Streamlit app.
    """

    # Set up page
    st.set_page_config(
        page_title=page_title,
    )

    title_text: str = f"""
        <div style='display: flex;'>
            {f"<img src='{image_path}' style='width: {image_width}rem; height: {image_height}rem;' />" if image_path is not None else "<p style='width: 0rem;' />"}
            &emsp; &emsp;
            <h1 style='font-size:2.5em;'>
            {text_1}<br />
            {text_2 if text_2 != "" or text_2 is not None else ""}
            </h1>
        </div>
    """
    st.html(title_text)
