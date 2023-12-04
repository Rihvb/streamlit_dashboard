import pandas as pd
import streamlit as st
import geopandas as gpd
import folium
from branca.colormap import LinearColormap
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster, Fullscreen, MeasureControl
from plotly.offline import plot
import plotly.graph_objs as go
import base64
from folium import FeatureGroup, Marker, Map
from branca.element import Template, MacroElement
from shapely.geometry import Point
def set_background_image_from_local5(path_to_image):
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
set_background_image_from_local5('pages/assets/bg.png')
def app() :
    # Load GeoDataFrame and ensure the GeoDataFrame has the right CRS
    gdf = gpd.read_parquet("pages/assets/output.geoparquet555")
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    elif gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    # Function to create a map based on a GeoDataFrame
    def create_map(gdf):
        # Ensure the GeoDataFrame uses the correct CRS
        gdf = gdf.to_crs(epsg=4326)
        mean_location = gdf['geometry'].unary_union.centroid
        mean_lat, mean_lon = mean_location.y, mean_location.x
        # Initialize Folium map
        m = folium.Map(location=[mean_lat, mean_lon], zoom_start=6)
        # Add circular markers for the existing data points
        for idx, row in gdf.iterrows():
            folium.CircleMarker(
                location=(row['geometry'].y, row['geometry'].x),
                radius=5,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.7,
                popup=f"Location: Latitude: {row['geometry'].y}, Longitude: {row['geometry'].x}"
            ).add_to(m)
        return m
    # Streamlit title
    st.title("Filtrage par requêtes spatiales")
    # Sidebar for selecting spatial query type
    st.sidebar.header("Spatial Query Selection")
    unique_value = 0
    spatial_query_type = st.sidebar.radio(
        "CHoisir une requête spatiale",
        ["Chercher point par coordonnées", "Chercher point par région", "Créer Buffer Zone"],
        key=f"radio_{unique_value}"
    )
    unique_value += 1
    # Initialize map container
    map_container = st.empty()
    # Sidebar functionality based on the spatial query type selected
    if spatial_query_type == "Chercher point par coordonnées":
        # Sidebar for coordinate input
        st.header("Chercher point par coordonnées")
        coordinate_input = st.text_input("Entrer les coordonnées (lat, lon)", "")
        # Display the initial map
        initial_map = create_map(gdf)
        map_container = folium_static(initial_map, width=1000, height=600)
        # Validate input and update the existing map with the searched location marker
        if coordinate_input:
            try:
                lat, lon = map(float, coordinate_input.split(','))
                # Create a new map with the marker at the entered coordinates
                new_map = folium.Map(location=[lat, lon], zoom_start=12)
                folium.Marker([lat, lon],
                            popup=f"Location choisie: Latitude: {lat}, Longitude: {lon}",
                            icon=folium.Icon(color='red', icon='info-sign')).add_to(new_map)
                # Add existing points from the GeoDataFrame to the new map
                for idx, row in gdf.iterrows():
                    folium.CircleMarker(
                        location=(row['geometry'].y, row['geometry'].x),
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_color='blue',
                        fill_opacity=0.7,
                        popup=f"Location: Latitude: {row['geometry'].y}, Longitude: {row['geometry'].x}"
                    ).add_to(new_map)
                    
                # Display the updated map
                Fullscreen().add_to(new_map)
                MeasureControl().add_to(new_map)
                map_container.empty()
                map_container = folium_static(new_map, width=1000, height=600)
                
            except ValueError:
                st.sidebar.error("Coordonnées incorrectes, Veuillez respecter le format: (lat, lon)")
    elif spatial_query_type == "Chercher point par région":
        gdf_points = gpd.read_parquet("pages/assets/output.geoparquet555")
        # Load the shapefile containing region boundaries
        # Load region boundaries and extract unique regions
        regions_gdf = gpd.read_file("pages/assets/region1.shp")
        regions = [''] + list(regions_gdf['Nom_Region'].unique())

        # Initialize Streamlit selectors with empty default option
        selected_region = st.selectbox("Selectionner une region ", regions, index=0)
        selected_province = None
        selected_commune = None

        # Initialize an empty GeoDataFrame for points to show
        points_to_show = gpd.GeoDataFrame()

        if selected_region:
            region_polygon = regions_gdf[regions_gdf['Nom_Region'] == selected_region].geometry.iloc[0]
            points_within_region = gdf_points[gdf_points.geometry.within(region_polygon)]
            
            provinces_gdf = gpd.read_file("pages/assets/provinec.shp")
            provinces_gdf_within_region = provinces_gdf[provinces_gdf.within(region_polygon)]
            provinces = [''] + list(provinces_gdf_within_region['Nom_Provin'].unique())
            selected_province = st.selectbox("Selectionner une province", provinces, index=0)

            if selected_province:
                province_polygon = provinces_gdf[provinces_gdf['Nom_Provin'] == selected_province].geometry.iloc[0]
                points_within_province = points_within_region[points_within_region.geometry.within(province_polygon)]
                
                communes_gdf = gpd.read_file("pages/assets/commune.shp")
                communes_gdf_within_province = communes_gdf[communes_gdf.within(province_polygon)]
                communes = [''] + list(communes_gdf_within_province['Nom_Commun'].unique())
                selected_commune = st.selectbox("Selectionner une commune", communes, index=0)

                if selected_commune:
                    commune_polygon = communes_gdf[communes_gdf['Nom_Commun'] == selected_commune].geometry.iloc[0]
                    points_to_show = points_within_province[points_within_province.geometry.within(commune_polygon)]
                else:
                    points_to_show = points_within_province
            else:
                points_to_show = points_within_region
        elif selected_region == '':
            points_to_show = gdf_points

        # Only display the map if there are points to show
        if not points_to_show.empty:
            # Calculate the centroid of points to show
            points_mean_lat = points_to_show.geometry.y.mean()
            points_mean_lon = points_to_show.geometry.x.mean()
            
            # Display the map
            m = folium.Map(location=[points_mean_lat, points_mean_lon], zoom_start=6)
            marker_cluster = MarkerCluster().add_to(m)
            
            # Add markers to the map
            for idx, row in points_to_show.iterrows():
                folium.Marker(
                    location=[row.geometry.y, row.geometry.x]
                ).add_to(marker_cluster)

            folium_static(m)
        if points_to_show.empty: 
            st.write('Il n y a pas de point dans cette zone')
            m = folium.Map(location=[33, -7], zoom_start=6)
            folium_static(m)
    elif spatial_query_type == "Créer Buffer Zone":
            st.header("Buffer Zone: Point Selection")
            point_input = st.text_input("Entrer les coordonnées du point centre (lat, lon)", "33, -7")

            # Process the user input for the Point
            try:
                lat, lon = map(float, point_input.split(','))
                point = Point(lon, lat)
            except ValueError:
                st.error("Coordonnées incorrectes, Veuillez respecter le format: (lat, lon)")
                point = None

            distance_threshold_km = st.number_input("Entrer la distance Buffer  (en KM)", min_value=0, value=50, step=5)

            # Perform spatial query - Filter GeoDataFrame based on Point proximity
            if point is not None and point.is_valid:
                # Create a buffer around the Point in kilometers
                buffered_point = point.buffer(distance_threshold_km / 111.32)  # Approximation for kilometers to degrees conversion

                # Filter GeoDataFrame based on the proximity of the buffered Point
                filtered_gdf_by_buffer = gdf[gdf.geometry.within(buffered_point)]

                # Initialize Folium map centered around the input point
                    
                m = folium.Map(location=[point.y, point.x], zoom_start=6,control_scale=True)
                folium.Marker([lat, lon], 
                                popup=f"Centre Buffer : Latitude: {lat}, Longitude: {lon}",
                                icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
                    
                cluster = MarkerCluster().add_to(m)

                # Add markers for points within the buffer zone to the MarkerCluster
                for idx, row in filtered_gdf_by_buffer.iterrows():
                    geom = row['geometry']
                    if geom.type == 'Point':
                        folium.Marker(
                            location=[geom.y, geom.x],
                            popup=f"{geom}"
                        ).add_to(cluster)

                # Convert the buffer zone to GeoJSON and add it to the Folium map
                folium.GeoJson(
                    buffered_point.__geo_interface__,
                    style_function=lambda x: {'color': 'blue', 'fillColor': 'blue', 'opacity': 0.3}
                ).add_to(m)

            # Add Fullscreen control to the map
                Fullscreen().add_to(m)
                # Display the Folium map in the Streamlit app
                folium_static(m,width=1000, height=600)
