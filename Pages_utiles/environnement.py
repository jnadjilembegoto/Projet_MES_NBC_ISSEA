import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from Datas.data_link import data_dir

data_path=data_dir('base_streamlit_storytellers.xlsx')
## Definition de fonction pour gerer sidebar

#pd.read_excel(data_path,sheet_name="Secteur_prof_ais")


def dash_Environnement():   
    st.markdown("""
        <style>
        .stApp {
            background-color:#2ca02c; /* Bleu clair inspiré de Stata */
        }
        .sidebar .sidebar-content {
            background-color: #2ca02c; /* Bleu encore plus clair pour la barre latérale */
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1f77b4; /* Bleu Stata pour les titres */
        }
        .stButton>button {
            background-color: #2ca02c; /* Boutons Stata */
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
    data=pd.read_excel(data_path,
                        sheet_name="base_mes_nbc")
    
    
    variable_meanings = {
    'aqua_culti_land': "Surface totale des terres agricoles cultivées (%)",
    'aqua_pluvio': "Indice pluviométrique annuel",
    'gaz_effet_serre': "Émissions totales de gaz à effet de serre (t CO2/personne)",
    'indice_prod_ag': "Indice de production agricole",
    'tasmax_annuel': "Température maximale moyenne annuelle (°C)",
    'tasmin_annuel': "Température minimale moyenne annuelle (°C)",
    'emploi_ag':"Employé agricole(%population employée)",
    'Prix_cotton (USD/kg)':"Prix du coton($ US/kg)",
    'Prix_corn (USD/kg)':"Prix du maïs ($ US/kg)"
}
    
    variable_color = {
    'aqua_culti_land': "#8B4513",  # Marron
    'aqua_pluvio': "purple",       # Violet
    'gaz_effet_serre': "orange",   # Orange
    'indice_prod_ag': "#1f77b4",   # Bleu (anciennement "b")
    'tasmax_annuel': "#FF0000",    # Rouge (anciennement "r")
    'tasmin_annuel': "#008000",    # Vert (anciennement "g")
    'emploi_ag': "#8B4513",        # Marron
    'Prix_cotton (USD/kg)': "#8B4513",  # Marron
    'Prix_corn (USD/kg)': "#8B4513"     # Marron
}

    def graphique_uni(df, var):
        fig = px.line(
            df,
            x="Year",
            y=var,
            title=f"Évolution de {variable_meanings[var]}",
            labels={"Year": "Année", var: variable_meanings[var]},
            line_shape="linear"
        )
        fig.update_traces(line=dict(color=variable_color[var]), mode="lines+markers")
        fig.update_layout(
            title=dict(x=0.5),  # Centrer le titre
            xaxis_title="Année",
            yaxis_title=variable_meanings[var],
            template="plotly_white"
        )
        st.plotly_chart(fig)
    
    # Curseur pour sélectionner une année
    st.sidebar.markdown('---')
    st.sidebar.write("## 🌱 Environnement-agriculture")
    titres_onglets = ["Température", "Précipitation", "Productivité agricole","Emission des gaz à effet de serre"]

    #onglets = st.tabs(titres_onglets)
    onglets_selectionnee=st.sidebar.radio("Choisissez un indicateur",titres_onglets)
    if onglets_selectionnee=="Température":
        st.write("## Evolution de la température du Tchad")
        graphique_uni(data, "tasmax_annuel")
        st.sidebar.markdown('---')
        st.sidebar.markdown('---')
        graphique_uni(data, "tasmin_annuel")
    if onglets_selectionnee=="Précipitation":
        st.write("## Evolution des pécipitations au Tchad")
        graphique_uni(data, "aqua_pluvio")
    if onglets_selectionnee=="Productivité agricole":
        st.write("## Agriculture au Tchad")
        graphique_uni(data, "indice_prod_ag")
    if onglets_selectionnee=="Emission des gaz à effet de serre":
        st.write("## Pollution atmosphérique")
        graphique_uni(data, "gaz_effet_serre")
              


