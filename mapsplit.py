from folium.plugins import DualMap
import streamlit as st
from folium import Map
from streamlit_folium import folium_static
import rasterio
from rasterio.plot import reshape_as_image
from PIL import Image
import numpy as np
import base64
from io import BytesIO
import folium

# Other imports here based on the needs of the script.
def set_background_image_from_local2(path_to_image):
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
set_background_image_from_local2('pages/assets/bg.png')
class MultiLocatedSelectbox:
    def __init__(self, options, key):
        self._options = options
        self._key = key
        self._counter = 0

    def selectbox(self, label):
        self._counter += 1
        key = f"{self._key}{self._counter}"
        st.session_state[key] = st.session_state.get(self._key, self._options[0])
        return st.selectbox(
            label, self._options, key=key, on_change=self._set_key, args=(key,)
        )

    def _set_key(self, key):
        st.session_state[self._key] = st.session_state[key]
@st.cache_resource
def app():
    st.title("Split-MAap")
    # Helper function to convert raster to PNG.
    def raster_to_png(image_array):
        image = Image.fromarray(reshape_as_image(image_array).clip(0, 255).astype(np.uint8))
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Helper function to create an image overlay.
    
    def create_image_overlay(tiff_file):
        with rasterio.open(tiff_file) as dataset:
            bands = [1, 2, 3] # Red, Green, Blue band indexes
            image_array = dataset.read(bands)
            # Transparency mask where all bands are 0.
            mask = (image_array[0] == 0) & (image_array[1] == 0) & (image_array[2] == 0)
            alpha_band = np.where(mask, 0, 255).astype(np.uint8)
            image_array = np.concatenate((image_array, alpha_band[None, ...]))
            bounds = dataset.bounds
            img_base64 = raster_to_png(image_array)
        return img_base64, bounds

    # Streamlit sidebar user input for attribute and days.
    st.subheader("Choisir le raster à afficher")
    col1, col2 = st.columns(2)
    # First column for the selection of the first day
    with col1:
        
        # Adjust the options based on your data
        unique_val = 0
        st.subheader("Raster 1")
        attribute_options = [1, 2, 3] # Replace with your attributes
        selected_attribute = st.selectbox("Choisir un attribut", options=attribute_options, key="option")
        day_options = [-6, -5, -4, -3, -2, -1, 0] # Days range
        selected_day_one = st.selectbox("Choisir le jour ", options=day_options, key="day_one")
    # Second column for the selection of the second day
    with col2:
        st.subheader("Raster 2 ")
        # The options can be the same as for the first day or different if required
        
        selected_attribute_two = st.selectbox("Choisir un attribut", options=attribute_options, key="attribute_two")
        day_options_raster2 = day_options[day_options.index(selected_day_one) + 1:]
        selected_day_two = st.selectbox("Choose a day", day_options_raster2, key="day_two")
    # Base path for TIFF files (adapt this to your file structure).


    # Build paths to the relevant TIFF files based on user input.
    tiff_file_day_one = f"pages/rasters/Att{selected_attribute}Jour{selected_day_one}.tif"
    tiff_file_day_two = f"pages/rasters/Att{selected_attribute_two}Jour{selected_day_two}.tif"

    # Create image overlays using the helper functions above.
    img_base64_day_one, bounds_day_one = create_image_overlay(tiff_file_day_one)
    img_base64_day_two, bounds_day_two = create_image_overlay(tiff_file_day_two)

    # Initialize the DualMap and set location to the average bounds of the TIFF files.
    m = DualMap(location=[(bounds_day_one.top + bounds_day_one.bottom) / 2, (bounds_day_one.right + bounds_day_one.left) / 2], zoom_start=5)

    # Apply the image overlays to both maps.
    folium.raster_layers.ImageOverlay(
        image=f"data:image/png;base64,{img_base64_day_one}",
        bounds=[[bounds_day_one.bottom, bounds_day_one.left], [bounds_day_one.top, bounds_day_one.right]],
        name=f"Day {selected_day_one} Overlay",
        opacity=1,
        interactive=True,
        cross_origin=False,
        show=True
    ).add_to(m.m1)

    folium.raster_layers.ImageOverlay(
        image=f"data:image/png;base64,{img_base64_day_two}",
        bounds=[[bounds_day_two.bottom, bounds_day_two.left], [bounds_day_two.top, bounds_day_two.right]],
        name=f"Day {selected_day_two} Overlay",
        opacity=1,
        interactive=True,
        cross_origin=False,
        show=True
    ).add_to(m.m2)

    # Allow the user to toggle between the overlays.
    folium.LayerControl().add_to(m)

    # Display the DualMap in Streamlit.
    folium_static(m,width=1000, height=600)
