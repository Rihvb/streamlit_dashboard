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
@st.cache_resource
def set_background_image_from_local7(path_to_image):
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
set_background_image_from_local7('pages/assets/bg.png')
def app():
    

    st.title("Visualisation des attributs")
    st.markdown("""
            <style>
            .column {
                position: flex; /* Use relative positioning for flexibility */
            }
            .map-container {
                /* Example CSS for the map container */
                height: 10px; /* Adjust height as needed */
                width: 100%; /* Adjust width as needed, or use fixed width */
                margin-bottom: 10px; /* Space below the map */
                margin-right: 20px
            .legend-container {
                /* Example CSS for the legend container */
                height: auto; /* Height based on content */
                width: =10%; /* Width of the sidebar */
                padding: 5px; /* Padding around legend items */
                border: 1px solid #ccc; /* Border around the legend */
                border-radius: 5px; /* Rounded corners for the legend */
                background-color: #f8f9fa; /* Light grey background */
                box-shadow: 0 2px 4px rgba(0,0,0,.1); /* Box shadow for a slight depth effect */
            }
            </style>
            """, unsafe_allow_html=True)
    
    visualization_type = st.selectbox("Choisir la colonne à visualiser", ["Propriete2", "Propriete3", "Attributs"])

    # Load the geospatial data
    gdf = gpd.read_parquet("pages/assets/output.geoparquet555")
    st.markdown('<div class="row">', unsafe_allow_html=True)
                # Ensure the GeoDataFrame has the correct Coordinate Reference System (CRS)
    if gdf.crs is None:
                    gdf.set_crs(epsg=4326, inplace=True)
    elif gdf.crs.to_epsg() != 4326:
                    gdf = gdf.to_crs(epsg=4326)

                # Add latitude and longitude columns
    gdf['latitude'] = gdf.geometry.y
    gdf['longitude'] = gdf.geometry.x

                # Drop rows with missing or invalid geometries
    gdf = gdf[~gdf.geometry.is_empty & gdf.geometry.notnull() & gdf.geometry.is_valid]
                

                # Sidebar for selecting visualization type

                # Legends for "propriete2" and "propriete3" columns based on color scale
    if visualization_type in ["Propriete2", "Propriete3"]:

                        st.markdown('<div class="map-container">', unsafe_allow_html=True)
                        # Initialize Folium map
                        m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=6)
                        min_value = gdf[visualization_type].min()
                        max_value = gdf[visualization_type].max()
                        
                        minimap = plugins.MiniMap(width=100, height=100)
                        m.add_child(minimap,)
                        color_scale = LinearColormap(['green', 'yellow', 'red'], vmin=min_value, vmax=max_value)
                        for idx, row in gdf.iterrows():
                            value = row[visualization_type]
                            if value == 0:
                                continue
                            color = color_scale(value)
                            folium.CircleMarker(
                                location=(row['latitude'], row['longitude']),
                                radius=5,
                                color=color,
                                fill=True,
                                fill_color=color,
                                fill_opacity=0.8,
                                popup=f"{visualization_type}: {value}"
                        ).add_to(m)
                        Fullscreen().add_to(m)
                        folium_static(m,width=1000, height=600)
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Legends for "propriete2" and "propriete3" columns based on color scale
                        
                        with st.expander("Voir légende"):
                            st.markdown('<div class="legend-container">', unsafe_allow_html=True)
                            st.subheader(f"Légende") 
                            # Generate a color scale legend
                            
                            
                            # Display color scale legend
                        
                            st.write("Legend:")
                            st.write(color_scale)
                            st.markdown('</div>', unsafe_allow_html=True)
                        # Add points to the map with colors based on the selected column
                            st.markdown('</div>', unsafe_allow_html=True)     
                # Legends for "attributes" columns with circles representing values
    else:
                    

                        m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=6)
                        # Let user select an attribute (1-2-3)
                        attribute_options = [1, 2, 3]  # Replace with your attribute options
                        day_options = [-6, -5, -4, -3, -2, -1, 0]  # Replace with your day options
                        columns = st.columns(2)
                        selected_attribute = columns[0].selectbox("Choisir un attribut (1-2-3)", attribute_options)
                        selected_day = columns[1].selectbox("Choisir un jour (-6 to 0)", day_options)
                        minimap = plugins.MiniMap(width=100, height=100)
                        m.add_child(minimap,)
                        # Let user select a day (-6 to 0)
                        
                    

                        # Combine the selected attribute and day to form the column name without parentheses
                        attribute_str = str(selected_attribute)
                        day_str = str(selected_day)
                        column_to_visualize = f"Attibut{attribute_str}Jour{day_str}"

                        # Get the values from the column
                        values = gdf[column_to_visualize].tolist()

                        # Normalize the values for radius scaling between 1 and 10 (adjust as needed)
                        min_val = min(values)
                        max_val = max(values)

                        for idx, row in gdf.iterrows():
                            value = row[column_to_visualize]
                            if value == 0:
                                continue
                            normalized_value = (value - min_val) / (max_val - min_val)
                            radius = (normalized_value ** 0.5) * 5

                            # Single color for 'attributes' column
                            color = 'blue'

                            # Add CircleMarker to the map
                            folium.CircleMarker(
                                location=(row['latitude'], row['longitude']),
                                radius=radius,
                                color=color,
                                fill=True,
                                fill_color=color,
                                fill_opacity=0.3,
                                popup=f"{value}"
                            ).add_to(m)
                        Fullscreen().add_to(m)
                        folium_static(m,width=1000, height=600)
                        step = (max_val - min_val) / 5

                    # Generate legends with 5 specific values
                        with st.expander("Voir légende"):
                            st.subheader(f"Légende")

                            legend_html = '<div style="display: flex ; flex-direction: row; align-items: center;">'

                            for i in range(1, 6):
                                value = min_val + (step * i)

                                # Normalize the value for radius scaling between 1 and 10
                                normalized_value = (value - min_val) / (max_val - min_val)
                                radius = int((normalized_value ** 0.5) * 10)

                                # Adding the SVG circle to the legend HTML
                                legend_html += (
                                    f'<div style="display: flex; align-items: center; margin-bottom: 5px; margin-right : 20px">'
                                    f'<svg height="{radius * 2}" width="{radius * 2}" style="margin-right: 10px;">'
                                    f'<circle cx="{radius}" cy="{radius}" r="{radius}" fill="blue" />'
                                    f'</svg>'
                                    f'<span>{value}</span>'
                                    f'</div>'
                                )

                            legend_html += '</div>'

                            # Displaying the legend using the HTML content
                            st.markdown(legend_html, unsafe_allow_html=True)
