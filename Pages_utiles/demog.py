import streamlit as st
import pandas as pd

from Datas.data_link import data_dir
# Titre de l'application avec un fond blanc


def dash_demog():
        
    ##  Design


    # CSS personnalisé pour l'arrière-plan
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

    



    # Titre de l'application


    #st.title("Apercu sur le taux d'emploi en Afrique")

    # Chargement des données

    #""""""""""""""""""""""""""""""""""""""""""""""
    st.sidebar.write("## Démographie")

    #onglets = st.tabs(titres_onglets)

    ## chargement de la premère base 
    data_path=data_dir('base_streamlit_storytellers.xlsx')
    base=pd.read_excel(data_path,sheet_name="Taux_emploi_chomage_Afrique")
    ## chargement de la deuxième base de données

   
