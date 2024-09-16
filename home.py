import streamlit as st
import base64
def set_background_image_from_local(path_to_image):
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
set_background_image_from_local('pages/assets/getimg_ai-2023-12-03T21_14_55.377Z.png')
def app (): 
    st.markdown(
    """
    <style>
    .welcome-banner {
        width: 100%;
        background-size: cover;
        padding: 50px;
        margin-bottom: 30px;
       
        text-align: left; /* Align only h2 and h1 to center in .welcome-banner */
    }
    .welcome-banner h1,
    .welcome-banner h2 {
        
        text-align: center; /* Center align h1 and h2 */
    }
    .navigation-card {
        background-color: #FFA500;
        display: inline-block;
        width: 40%;
        padding: 20px;
        margin: 10px;
        text-align: center;
        text-shadow: 5px 5px 8px #00FF00
        font-weight: bold;
    
        border-radius: 10px;
        transition: transform 0.2s;
    }
    .navigation-card:hover {
        transform: scale(1.05);
    }
    .description {
        /* Additional styles can be added here if needed */
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: none; /* No underline */
        cursor: help; /* Help cursor on hover */
        }
        .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #989b9a;
        color: #fff;
        text-shadow: 5px 5px 8px #00FF00
        text-align: center;
        padding: 5px 0;
        border-radius: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -150px; /* Use half of the width (300px / 2) to center the tooltip */
        opacity: 0;
        transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
        }
        .app-footer {
        text-align: center;
        padding: 20px;
        color : white
    
        }
    ]
    </style>

    <div class="welcome-banner">
        <h2 style="color: #FFA500">Bienvenue au Dashboard Geospatial</h2>
        <h1 style="color: #fff">Explorer les données géospatiales avec des cartes interactives et des visualisations.</h1>
        <p style="color: #cccccc"> Le Dashboard GeoAnalytique a été développé pour exploiter un schéma de données spatio-temporel composé de points géométriques avec divers attributs. Ces données fictives, au nombre de 1200 points, sont distribuées de manière aléatoire à travers le Maroc. .</p>
    </div>
     <div class="description">
        
    </div>

    <div>
        <div>
        <div class="navigation-card tooltip"><strong>Visualisation Dynamique</strong>
            <span class="tooltiptext" style="font-size: small; font-style: italic;">Choisissez les données à afficher sur la carte et naviguez entre les jours pour observer les changements.</span>
        </div>
        <div class="navigation-card tooltip"><strong>Analyse Temporelle</strong>
            <span class="tooltiptext" style="font-size: small; font-style: italic;">Explorez les séries temporelles en cliquant sur les points de la carte.</span>
        </div>
        <div class="navigation-card tooltip"><strong>Filtrage Facile</strong>
            <span class="tooltiptext" style="font-size: small; font-style: italic;">Utilisez des requêtes spatiales ou attributaires pour affiner les données affichées.</span>
        </div>
        <div class="navigation-card tooltip"><strong>Comparaison Rapide</strong>
            <span class="tooltiptext" style="font-size: small; font-style: italic;">Comparez deux cartes de jours différents côte à côte avec la fonctionnalité SplitMap.</span>
        </div>
        
    </div>
        
    </div>

    <div class="app-footer">
        <p>Geospatial Dashboard © 2023 , developpé par :</p>
        <p><strong>Moussadek Rihab </strong></p>
        
        
    </div>
    """,
    unsafe_allow_html=True
)

