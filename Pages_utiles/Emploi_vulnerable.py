import pandas as pd
import streamlit as st
import plotly.express as px
from Datas.data_link import data_dir

    # Style personnalisé pour l'application
def emploi_vul():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        max-width: 100%;
        padding: 0;
        margin: auto;
    }
    [data-testid="block-container"] {
        padding: 1rem 0;
    }
    [data-testid="stSidebar"] {
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Chargement des données
    data_path=data_dir('base_streamlit_storytellers.xlsx')
    base =pd.read_excel(data_path,sheet_name="Taux_de_pauvreté")



    #

    st.header("Visualisation l'évolution du taux de travailleurs pauvres par pays et par sexe.")

    # Filtrer la tranche d'âge
    tranche_age = 'Age (Youth, adults): 15+'
    base_filtered = base[base['Tranche_age'] == tranche_age]



    # Filtrer les données pour l'année sélectionnée
    #base_year = base_filtered[base_filtered['Annee'] == annee_selectionnee]



    # Sélection du pays via un menu déroulant
    pays_cible = st.sidebar.selectbox(
        "Sélectionnez un pays :", 
        options=base["Pays"].unique(), 
        key="select_pays"
    )
        
    st.write("#### Evolution animée du taux de travailleurs pauvres :")

    # Sélection de l'animation via un sélecteur radio
    selection = st.sidebar.radio(
        "Sélectionnez une visualisation :", 
        options=["Aperçu global", "Aperçu pays"], 
        index=0,
        key="radio_selection"
    )

    # Graphique animé selon la sélection
    if selection == "Aperçu global":
        fig_animation_global = px.scatter(
            base[base['Tranche_age'] == tranche_age],
            x='Pays',
            y='Working poverty rate (%)',
            color='Sexe',
            hover_name='Pays',
            range_y=[0, 100],
            animation_frame='Annee',
            title="Evolution du taux de travailleurs pauvres  et par sexe "  )#+pays_cible
        
        st.plotly_chart(fig_animation_global, key="animation_global")

    elif selection == "Aperçu pays":
        # Filtrer les données pour le pays sélectionné
        base_pays_animation = base[base["Pays"] == pays_cible]
        
        fig_animation_pays = px.bar(
            base_pays_animation,
            x="Tranche_age",
            y="Working poverty rate (%)",
            range_y=[0, 100],
            color="Sexe",
            barmode="group",
            animation_frame="Annee",
            title=f"Taux de travailleurs pauvres selon le sexe et l'âge pour {pays_cible}",
            labels={
                "Tranche_age": "Tranche d'âge",
                "Working poverty rate (%)": "Taux de travailleurs pauvres (%)"
            },
            template="plotly_white"
        )
        st.plotly_chart(fig_animation_pays, key="animation_pays")
