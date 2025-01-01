import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Datas.data_link import data_dir
# Titre de l'application avec un fond blanc


def dash_demog():
        
    ##  Design


    # CSS personnalisé pour l'arrière-plan
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

    



    # Titre de l'application


    #st.title("Apercu sur le taux d'emploi en Afrique")

    # Chargement des données

    #""""""""""""""""""""""""""""""""""""""""""""""
    st.sidebar.write("## Démographie")

    #onglets = st.tabs(titres_onglets)
    
    ## chargement de la premère base 
    data_path=data_dir('base_streamlit_storytellers.xlsx')
    base=pd.read_excel(data_path,sheet_name="population_tchad_pyramide")
    with st.sidebar:
        selected_year = st.sidebar.slider("Sélectionnez une année :", int(base.Year.min()), int(base.Year.max()), 2020)
    
    st.markdown(
    f"""
    <div style="font-size:24px; font-weight:bold;">
        📊 Représentation de la pyramide des âges de la population du Tchad en {selected_year}
    </div>
    """,
    unsafe_allow_html=True)
   

    def pyramide(data_pop_pivot, year):
        # Étape 1 : Définir les séries et filtrer les données
        series = {
            "SP.POP.0004.MA.5Y": "Hommes 0-4",
            "SP.POP.0004.FE.5Y": "Femmes 0-4",
            "SP.POP.0509.MA.5Y": "Hommes 5-9",
            "SP.POP.0509.FE.5Y": "Femmes 5-9",
            "SP.POP.1014.MA.5Y": "Hommes 10-14",
            "SP.POP.1014.FE.5Y": "Femmes 10-14",
            "SP.POP.1519.MA.5Y": "Hommes 15-19",
            "SP.POP.1519.FE.5Y": "Femmes 15-19",
            "SP.POP.2024.MA.5Y": "Hommes 20-24",
            "SP.POP.2024.FE.5Y": "Femmes 20-24",
            "SP.POP.2529.MA.5Y": "Hommes 25-29",
            "SP.POP.2529.FE.5Y": "Femmes 25-29",
            "SP.POP.3034.MA.5Y": "Hommes 30-34",
            "SP.POP.3034.FE.5Y": "Femmes 30-34",
            "SP.POP.3539.MA.5Y": "Hommes 35-39",
            "SP.POP.3539.FE.5Y": "Femmes 35-39",
            "SP.POP.4044.MA.5Y": "Hommes 40-44",
            "SP.POP.4044.FE.5Y": "Femmes 40-44",
            "SP.POP.4549.MA.5Y": "Hommes 45-49",
            "SP.POP.4549.FE.5Y": "Femmes 45-49",
            "SP.POP.5054.MA.5Y": "Hommes 50-54",
            "SP.POP.5054.FE.5Y": "Femmes 50-54",
            "SP.POP.5559.MA.5Y": "Hommes 55-59",
            "SP.POP.5559.FE.5Y": "Femmes 55-59",
            "SP.POP.6064.MA.5Y": "Hommes 60-64",
            "SP.POP.6064.FE.5Y": "Femmes 60-64",
            "SP.POP.6569.MA.5Y": "Hommes 65-69",
            "SP.POP.6569.FE.5Y": "Femmes 65-69",
            "SP.POP.7074.MA.5Y": "Hommes 70-74",
            "SP.POP.7074.FE.5Y": "Femmes 70-74",
            "SP.POP.7579.MA.5Y": "Hommes 75-79",
            "SP.POP.7579.FE.5Y": "Femmes 75-79",
            "SP.POP.80UP.MA.5Y": "Hommes 80+",
            "SP.POP.80UP.FE.5Y": "Femmes 80+",
        }

        # Filtrer les données pour l'année sélectionnée
        df_year = data_pop_pivot[data_pop_pivot['Year'] == year]
        df_filtered = df_year[list(series.keys())].rename(columns=series)

        # Étape 2 : Créer des listes pour les hommes et les femmes
        pop_male = -df_filtered[[col for col in df_filtered.columns if "Hommes" in col]].sum()
        pop_female = df_filtered[[col for col in df_filtered.columns if "Femmes" in col]].sum()

        # Extraire les tranches d'âge
        age_labels = [col.split(" ")[1] for col in pop_male.index]

        # Étape 3 : Tracer la pyramide des âges
        fig, ax = plt.subplots(figsize=(10, 8))

        # Barres pour hommes et femmes
        ax.barh(age_labels, pop_male, color="blue", label="Hommes")
        ax.barh(age_labels, pop_female, color="pink", label="Femmes")

        # Ajouter les détails au graphique
        ax.set_xlabel("Population (en milliers)")
        ax.set_ylabel("Tranche d'âge")
        ax.set_title(f"Pyramide des âges - Tchad en {year}")
        ax.legend()

        # Rendre les valeurs des abscisses positives
        xticks = ax.get_xticks()
        ax.set_xticklabels([abs(int(tick)) for tick in xticks])

        ax.grid(axis="x", linestyle="--", alpha=0.7)
        

        # Ajuster l'apparence
        plt.tight_layout()
        return fig


    # Génération de la pyramide
    fig = pyramide(base, selected_year)

    # Affichage dans Streamlit
    st.pyplot(fig)
    st.write("Source : WDI")


   
