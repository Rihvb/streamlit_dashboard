import streamlit as st
from PIL import Image, ImageSequence
import base64
import io
def set_background_image_from_local6(path_to_image):
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
set_background_image_from_local6('pages/assets/bg.png')

def app():
    
    st.title("Timelapse des jours")
    # Dictionary of attributes to corresponding timelapse GIF paths
    timelapse_gifs = {
        'Attribute 1': 'pages/timelapse/timelapseatt1.gif',
        'Attribute 2': 'pages/timelapse/timelapseatt2.gif',
        'Attribute 3': 'pages/timelapse/timelapseatt3.gif',
    }

    # Let the user select an attribute
    selected_attribute = st.selectbox("Seléctionner un attribut", list(timelapse_gifs.keys()), key="timelapse_selectbox")

    # Get the path of the selected attribute's timelapse GIF
    gif_path = timelapse_gifs[selected_attribute]

    # Open the GIF file using PIL and adjust frame duration
    with Image.open(gif_path) as im:
        frames = [frame.copy() for frame in ImageSequence.Iterator(im)]
        # Define a slower frame duration or speed ratio
        frame_duration = int(im.info['duration'] *3)  # Increase duration by 50%
        frames = [frame.resize((frame.width//2, frame.height//2)) for frame in frames]  # Reduce size by 50%
        # Save frames to bytes buffer
        byte_io = io.BytesIO()
        frames[0].save(byte_io, format='GIF', save_all=True,
                       append_images=frames[1:], 
                       loop=0, duration=frame_duration)
        byte_io.seek(0)

    # Encode the modified GIF to a data URL
    contents = byte_io.read()
    data_url = base64.b64encode(contents).decode("utf-8")

    # Include the width style in the 'img' tag
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="timelapse gif" style="width:100%;">',
        unsafe_allow_html=True,
    )

# Call the app function
