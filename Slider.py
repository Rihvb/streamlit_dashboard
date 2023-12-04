import streamlit as st
from PIL import Image
import rasterio
import base64
from rasterio.plot import reshape_as_image
def set_background_image_from_local4(path_to_image):
    with open(path_to_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    background_image_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
    }}
    </style>
    """
    
    st.markdown(background_image_css, unsafe_allow_html=True)
# Example usage, replace 'local_image.png' with the path to your local image file.
set_background_image_from_local4('multiapp_app\\pages\\assets\\bg.png')
def app():
    st.title("Slider des rasters")
    # User selects the attribute
    attribute= st.selectbox('Select Attribute', ['Attribut 1', 'Attribut 2', 'Attribut 3'])

    # Dictionary mapping attributes to their respective raster files
    raster_files_dict = {
        'Attribut 1': [
            'multiapp_app\\pages\\rasters\\Att1Jour0.tif',
            'multiapp_app\\pages\\rasters\\Att1Jour-1.tif',
            'multiapp_app\\pages\\rasters\\Att1Jour-2.tif',
            'multiapp_app\\pages\\rasters\\Att1Jour-3.tif',
            'multiapp_app\\pages\\rasters\\Att1Jour-4.tif',
            'multiapp_app\\pages\\rasters\\Att1Jour-5.tif',
            'multiapp_app\\pages\\rasters\\Att1Jour-6.tif'
            
            # ... add the rest of the Attribute 1 raster files
        ],
        'Attribut 2': [
            'multiapp_app\\pages\\rasters\\Att2Jour0.tif',
            'multiapp_app\\pages\\rasters\\Att2Jour-1.tif',
            'multiapp_app\\pages\\rasters\\Att2Jour-2.tif',
            'multiapp_app\\pages\\rasters\\Att2Jour-3.tif',
            'multiapp_app\\pages\\rasters\\Att2Jour-4.tif',
            'multiapp_app\\pages\\rasters\\Att2Jour-5.tif',
            'multiapp_app\\pages\\rasters\\Att2Jour-6.tif',

            # ... add the rest of the Attribute 2 raster files
        ],
        'Attribut 3': [
            'multiapp_app\\pages\\rasters\\Att3Jour0.tif',
            'multiapp_app\\pages\\rasters\\Att3Jour-1.tif',
            'multiapp_app\\pages\\rasters\\Att3Jour-2.tif',
            'multiapp_app\\pages\\rasters\\Att3Jour-3.tif',
            'multiapp_app\\pages\\rasters\\Att3Jour-4.tif',
            'multiapp_app\\pages\\rasters\\Att3Jour-5.tif',
            'multiapp_app\\pages\\rasters\\Att3Jour-6.tif',
            # ... add the rest of the Attribute 3 raster files
        ]
    }

    # Retrieve the list of raster files for the selected attribute
    raster_files = raster_files_dict[attribute]

    # Initialize session state for index if it doesn't exist
    if 'index' not in st.session_state:
        st.session_state['index'] = 0

    # Function to load and display the raster image or map
    def load_raster(index, image_placeholder, text_placeholder):
        raster_path = raster_files[index]
        with rasterio.open(raster_path) as src:
            data = src.read()
            image_data = reshape_as_image(data)
            image = Image.fromarray(image_data)

            text_for_image = [f"JOUR{i}" for i in range(len(raster_files))]
            image_text = text_for_image[index]
            image_placeholder.image(image, use_column_width=True, caption=f"{attribute} - {image_text}")

            # Display the styled text using Markdown
            centered_text = f"<div style='text-align: center; font-size: 20px; font-weight: bold;'>{image_text}</div>"
            text_placeholder.markdown(centered_text, unsafe_allow_html=True)

    # Function to increment index (with wrap-around)
    def increment_index():
        st.session_state.index = (st.session_state.index + 1) % len(raster_files)
        load_raster(st.session_state.index, image_placeholder, text_placeholder)

    # Function to decrement index (with wrap-around)
    def decrement_index():
        st.session_state.index = (st.session_state.index - 1) % len(raster_files)
        load_raster(st.session_state.index, image_placeholder, text_placeholder)

    st.write("Use the arrows below to navigate through the images.")
    col1, col3 = st.columns([1, 1])
    with col1:
        st.button('◀', key='previous', on_click=decrement_index)
    with col3:
        st.button('▶', key='next', on_click=increment_index)

    image_placeholder = st.empty()
    text_placeholder = st.empty()
    load_raster(st.session_state['index'],text_placeholder, image_placeholder )

# Call the app function

