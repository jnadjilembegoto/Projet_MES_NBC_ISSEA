
import streamlit as st
import pandas as pd
from Datas.data_link import data_dir

## Importation de la base de données

def dash_simulation():
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
    def load_data():
         data_path=data_dir('base_streamlit_storytellers.xlsx')
         return pd.read_excel(data_path,sheet_name="chef_entreprises")

    data = load_data()
    st.write("### Simulation de l'impact de la variation relative d'une variable exogène sur les variables endogènes de notre système")


    

    st.write("Sources : Données issues de ILOSTAT")


