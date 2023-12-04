import streamlit as st
from streamlit_option_menu import option_menu
import home, Slider, Visualisation_des_colonnes, Timelapse, mapsplit, popupcharts, attquery, spatialquery
from home import set_background_image_from_local
from Slider import set_background_image_from_local4
from Visualisation_des_colonnes import set_background_image_from_local7
from Timelapse import set_background_image_from_local6
from mapsplit import set_background_image_from_local2
from popupcharts import set_background_image_from_local3
from attquery import set_background_image_from_local1
from spatialquery import set_background_image_from_local5

# Example usage, replace 'local_image.png' with the path to your local image file.

class MultiApp:
  
    def __init__(self):
        self.apps = []
    
    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })
        
    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Dashboard Geospatial',
                options=['Home', 'Visualisation des colonnes', 'Slider', 'SplitMap', 'Timelapse', 'PopUp-Charts', 'Requêtes attributaires', 'Requêtes spatiales'],
                icons=['house', 'bar-chart-line', 'sliders', 'map', 'clock-history', 'bar-chart-steps', 'journal-text', 'geo-alt'],
                menu_icon='cast',
                default_index=0,  # "Home" is the first option
                styles={
                    "container": { "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {"font-size": "18px", "text-align": "left", "margin": "0px", "padding": "0px"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        if app == 'Home':
            home.app()
            set_background_image_from_local('multiapp_app\\pages\\assets\\getimg_ai-2023-12-03T21_14_55.377Z.png')
        elif app == 'Visualisation des colonnes':
            Visualisation_des_colonnes.app()
            set_background_image_from_local7('multiapp_app\\pages\\assets\\bg.png')
        elif app == 'Slider':
            Slider.app()
            set_background_image_from_local4('multiapp_app\\pages\\assets\\bg.png')
        elif app == 'SplitMap':
            mapsplit.app()
            set_background_image_from_local2('multiapp_app\\pages\\assets\\bg.png')
        elif app == 'Timelapse':
            Timelapse.app()
            set_background_image_from_local6('multiapp_app\\pages\\assets\\bg.png')
        elif app == 'PopUp-Charts':
            popupcharts.app()
            set_background_image_from_local3('multiapp_app\\pages\\assets\\bg.png')
        elif app == 'Requêtes attributaires':
            attquery.app()
            set_background_image_from_local1('multiapp_app\\pages\\assets\\bg.png')
        elif app == 'Requêtes spatiales':
            spatialquery.app()
            set_background_image_from_local5('multiapp_app\\pages\\assets\\bg.png')

if __name__ == "__main__":
    # Instantiate and run the MultiApp class
    app = MultiApp()
    app.run()
    