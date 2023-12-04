import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
from branca.colormap import LinearColormap
from plotly.offline import plot
import plotly.graph_objs as go
import base64 
from folium import FeatureGroup, Marker, Map
from branca.element import Template, MacroElement
from folium import plugins
from folium.plugins import MarkerCluster, Fullscreen
def set_background_image_from_local3(path_to_image):
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

set_background_image_from_local3('pages/assets/bg.png')

@st.cache_resource
def app():
        st.title("Pop_Up charts")
        st.header('Charts')
        st.write("Clique sur un point pour afficher son graphe")
        # Content for Raster Map Slider will go here
      
        # Column setup for Streamlit layout
        col1, col2 = st.columns([2, 1])
    
        # Load GeoDataFrame
        gdf = gpd.read_parquet("pages/assets/output.geoparquet555")

        # Ensure the GeoDataFrame has the right CRS
        if gdf.crs is None:
            gdf.set_crs(epsg=4326, inplace=True)
        elif gdf.crs.to_epsg() != 4326:
            gdf = gdf.to_crs(epsg=4326)

        # Add latitude and longitude columns
        gdf['latitude'] = gdf['geometry'].y
        gdf['longitude'] = gdf['geometry'].x

        # Remove rows with invalid or missing geometries
        gdf = gdf[~gdf['geometry'].is_empty & gdf['geometry'].notnull() & gdf['geometry'].is_valid]

        # Calculate the mean location for the map center
        if not gdf.empty:
            mean_location = gdf['geometry'].unary_union.centroid
            mean_lat, mean_lon = mean_location.y, mean_location.x
        else:
            mean_lat, mean_lon = 0, 0
        with col1:
            # Initialize the Folium map
            m = folium.Map(location=[mean_lat, mean_lon], zoom_start=6)

            # Loop through the GeoDataFrame to add the popups with Plotly charts
            for idx, row in gdf.iterrows():
                # Prepare data
                days = list(range(0, -7, -1))
                attrib_data = {f'Attibut{i}': [row.get(f'Attibut{i}Jour{day}', None) for day in days] 
                            for i in range(1, 4)}

                # Generate Plotly figure
                fig = go.Figure()
                colors_dict = {
                    'Attibut1': 'red',
                    'Attibut2': 'green',
                    'Attibut3': 'blue',
                }

                for attrib, data in attrib_data.items():
                    color = colors_dict[attrib]  # Use the color from dictionary
                    fig.add_trace(go.Scatter(x=days, y=data, mode='lines+markers', name=attrib, line=dict(color=color)))

                fig.update_layout(title='Attribute Values Over The Week',
                                xaxis_title='Days Ago',
                                yaxis_title='Value',
                                margin=dict(l=20, r=20, t=30, b=20))

                # Convert figure to HTML and encode it for iframe embedding
                fig_html = plot(fig, output_type='div', include_plotlyjs='cdn')
                encoded_fig = base64.b64encode(fig_html.encode('utf-8')).decode('utf-8')

                # Create Folium popup with the embedded Plotly chart
                iframe = folium.IFrame(html=f'<div style="width: 100%;"><iframe src="data:text/html;base64,{encoded_fig}" style="border: none; width: 100%; height: 100%;"></iframe></div>',
                                    width=500,
                                    height=300)
                popup = folium.Popup(iframe, max_width=500)
                
                # Add circle marker with popup to map
                folium.CircleMarker(
                    location=(row['latitude'], row['longitude']),
                    radius=5,
                    color='blue',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.7,
                    popup=popup
                ).add_to(m)

            # Display the interactive map in the Streamlit app
            folium_static(m,width=1000,height=600)
            
