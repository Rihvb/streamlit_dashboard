import pandas as pd
import streamlit as st
import geopandas as gpd
import folium
from branca.colormap import LinearColormap
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from plotly.offline import plot
import plotly.graph_objs as go
import base64
from folium import FeatureGroup, Marker, Map
from branca.element import Template, MacroElement
@st.cache_resource
def set_background_image_from_local1(path_to_image):
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

set_background_image_from_local1('pages/assets/bg.png')
@st.cache_resource
def app (): 
    

    st.header('Filtrage par requêtes attributaires')

    # Load the geospatial data
    gdf = gpd.read_parquet("pages/assets/output.geoparquet555")

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
    col1, col2 = st.columns([3, 1])
    # for selecting visualization type
    visualization_type = st.radio("Select Visualization Type", ["Attribute Range Query", "Time Range Query"])

    if visualization_type == "Attribute Range Query":
        # Code for attribute range query
        st.subheader("Entrer un intervalle")
        
        # Get column names for selection
        selectable_columns = [col for col in gdf.columns if col not in ['geometry', 'latitude', 'longitude', 'Latitude', 'Longitude', 'Propriete1','Propriete4']]
        selected_column = st.selectbox("Selectionner une colonne", selectable_columns)

        # Get minimum and maximum values for the selected column
        min_value = gdf[selected_column].min()
        max_value = gdf[selected_column].max()

        # Input widgets for the attribute range with submit button
        st.write(f"Attribute Range for {selected_column}:")
        start_value = st.number_input("Start Value", min_value=min_value, max_value=max_value, value=min_value)
        end_value = st.number_input("End Value", min_value=min_value, max_value=max_value, value=max_value)
        submit_button = st.button('Submit Range')

        # Initialize the map outside the condition
        m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=6)

        if submit_button:
            # Filter GeoDataFrame based on the selected column and range
            filtered_gdf = gdf[(gdf[selected_column] >= start_value) & (gdf[selected_column] <= end_value)]
            
            # Loop through the filtered GeoDataFrame to add points to the map
            for idx, row in filtered_gdf.iterrows():
                folium.CircleMarker(
                            location=(row['latitude'], row['longitude']),
                            radius=5,
                            color='blue',
                            fill=True,
                            fill_color='blue',
                            popup=f"{selected_column}: {row[selected_column]}",
                            tooltip=row[selected_column]
                ).add_to(m)
            # Display the map in the Streamlit app
            folium_static(m)

            # Display filtered data in a table
            st.write(filtered_gdf)
    else:
        # Code for time range query
        st.subheader("Selectionner un intervalle de temps")
        gdf['Propriete4'] = pd.to_datetime(gdf['Propriete4'])
        min_date = gdf['Propriete4'].min()
        max_date = gdf['Propriete4'].max()

        # Calculate a default date within the valid range
        default_date = min_date + (max_date - min_date) // 2  # Adjust the default date calculation as needed

        # for selecting date range
        start_date = pd.Timestamp(st.date_input("Start Date", min_value=min_date, max_value=max_date, value=default_date))
        end_date = pd.Timestamp(st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date))

        submit_dates = st.button("Submit Date Range")

        m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=6)

        if submit_dates:
            # Filter the GeoDataFrame based on the selected date range
            filtered_gdf_by_date = gdf[(gdf['Propriete4'] >= start_date) & (gdf['Propriete4'] <= end_date)]

            # Loop through the filtered GeoDataFrame to add the points
            for idx, row in filtered_gdf_by_date.iterrows():
                
                popup_text = row['Propriete4'].strftime('%Y-%m-%d')
                folium.CircleMarker(
                    location=(row['latitude'], row['longitude']),
                    radius=5,
                    color='blue',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.7,
                    popup=folium.Popup(popup_text, max_width=300)
                ).add_to(m)
            # Display the map in the Streamlit app with filtered data
            folium_static(m)

            # Display filtered data in a table
            st.write(filtered_gdf_by_date)
