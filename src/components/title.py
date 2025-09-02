# Streamlit code for the title header component

# Import necessary libraries
import streamlit as st


# Main function to create the title header
def title_header(
    text_1: str = "",
    text_2: str = "",
    image_path: str | None = None,
    image_width: int = 150,
) -> None:
    """
    Reusable title header component for Streamlit apps.

    Args:
        text_1 (str): The first line of the title.
        text_2 (str, optional): The second line of the title.
        image_path (str | None): Path to an optional image to display alongside the title. Defaults to None.
        image_width (int): Width of the image if provided. Defaults to 150.

    Returns:
        None: Renders the title header in the Streamlit app.
    """

    # Create two columns for the header
    col1, col2 = (
        st.columns([0.13, 1]) if image_path is not None else st.columns([1, 0.01])
    )

    with col2 if image_path is not None else col1:
        st.markdown(
            (
                "<h1 style='font-size:2.5em;'>"
                f"<span>{text_1}</span><br>"
                f"<span>{text_2}</span>"
                if text_2 != ""
                else f"" "</h1>"
            ),
            unsafe_allow_html=True,
        )

    if image_path is not None:
        with col1:
            # render_image(image_path, image_width)
            st.image(
                image_path,
                width=image_width,
            )
