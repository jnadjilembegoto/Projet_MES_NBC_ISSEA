import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import plotly.express as px
from Datas.data_link import data_dir

data_path=data_dir('base_streamlit_storytellers.xlsx')
## Definition de fonction pour gerer sidebar

#pd.read_excel(data_path,sheet_name="Secteur_prof_ais")


def dash_Environnement():   
    st.markdown("""
        <style>
        .stApp {
            background-color: #eaf6ff; /* Bleu clair inspiré de Stata */
        }
        .sidebar .sidebar-content {
            background-color: #d0e6f5; /* Bleu encore plus clair pour la barre latérale */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1f77b4; /* Bleu Stata pour les titres */
        }
        .stButton>button {
            background-color: #1f77b4; /* Boutons Stata */
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)        
    st.header("Environnement-climat-agriculture")

    st.markdown("""
    <style>
    /* Ajuste la largeur totale du conteneur principal */
    [data-testid="stAppViewContainer"] {
        max-width: 100%; /* Ajustez la largeur à 95% de l'écran */
        padding-left: 0rem; /* Supprime les marges latérales */
        padding-right: 0rem;
        margin-left: auto;
        margin-right: auto;
    }

    /* Réduit les marges des blocs pour un meilleur alignement */
    [data-testid="block-container"] {
        padding: 1rem 0rem; /* Ajoute un espacement en haut et en bas uniquement */
    }

    /* Permet d'afficher plusieurs graphiques sur une même ligne */
    [data-testid="stHorizontalBlock"] > div {
        flex: 1; /* Répartit l'espace horizontalement */
        margin-right: 1rem; /* Ajoute un espace entre les colonnes */
    }

    /* Améliore la gestion des composants interactifs */
    [data-testid="stSidebar"] {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)
    # Curseur pour sélectionner une année
    st.sidebar.markdown('---')
    st.sidebar.write("## 🌱 Environnement-agriculture")
    st.sidebar.write("Aller ")
    titres_onglets = ["Température", "Précipitation", "Productivité agricole","Emission des gaz à effet de serre"]

    #onglets = st.tabs(titres_onglets)
    onglets_selectionnee=st.sidebar.radio("Indicateur",titres_onglets)
    if onglets_selectionnee=="Température":
        st.write("## Evolution de la température du Tchad")
        data=pd.read_excel(data_path,
                        sheet_name="Infomel_Region")
       
              


