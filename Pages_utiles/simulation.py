
import streamlit as st
import pandas as pd
from Datas.data_link import data_dir

## Importation de la base de données

def dash_simulation():
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
    def load_data():
         data_path=data_dir('base_streamlit_storytellers.xlsx')
         return pd.read_excel(data_path,sheet_name="chef_entreprises")

    data = load_data()
    st.write("### Simulation de l'impact de la variation relative d'une variable exogène sur les variables endogènes de notre système")


    

    variable_meanings = {
    'aqua_culti_land': "Surface totale des terres agricoles cultivées (%)",
    'aqua_pluvio': "Indice pluviométrique annuel",
    'gaz_effet_serre': "Émissions totales de gaz à effet de serre (t CO2/personne)",
    'tasmax_annuel': "Température maximale moyenne annuelle (°C)",
    'tasmin_annuel': "Température minimale moyenne annuelle (°C)",
    'emploi_ag': "Employé agricole (% population employée)",
    'Prix_cotton': "Prix du coton (USD/kg)",
    'Prix_mais': "Prix du maïs (USD/kg)"
}
    results_dict = {
    "tasmax_annuel": 0.05,
    "tasmin_annuel": 9.10,
    "aqua_pluvio": 5.21,
    "aqua_culti_land": 11.21,
    "Prix_cotton": -1.48,
    "Prix_mais": 1.50,
    "emploi_ag": -0.15,
    "gaz_effet_serre": 16.51
}
    
    

    # Fonction pour demander les valeurs pour chaque variable
    def get_input_values():
        values = {}
        for variable, meaning in variable_meanings.items():
            value = st.number_input(f"Entrez la valeur pour {meaning} ({variable})", min_value=-1e10, value=0.0)
            values[variable] = value
        return values
    # Disposition en colonnes
    col1, col2 = st.columns(2)

    # Affichage dans la première colonne
    with col1:
        input_values = get_input_values()
        
    # Affichage dans la deuxième colonne
    with col2:
        if input_values["aqua_culti_land"]<1.5408878 and input_values["aqua_culti_land"]>3.9739096:
            input_values["aqua_culti_land"]=1
        else:
            input_values["aqua_culti_land"]=0

        if input_values["aqua_pluvio"]< 625.026 and input_values["aqua_pluvio"]> 686.823:
            input_values["aqua_pluvio"]=1
        else:
            input_values["aqua_pluvio"]=0

        ipa=-181.51
        for key in results_dict:
            ipa=ipa+results_dict[key]*input_values[key]
        #st.write(f"Valeurs saisies :{ipa}")
        st.markdown(f"""
                    <style>
                    .clignotant {{
                        font-weight: bold;
                        font-size: 18px;
                        animation: clignote 1s linear infinite;
                    }}
                    
                    @keyframes clignote {{
                        0% {{ opacity: 1; }}
                        50% {{ opacity: 0; }}
                        100% {{ opacity: 1; }}
                    }}

                    .cadre {{
                        border: 2px solid black;
                        padding: 10px;
                        display: inline-block;
                        margin-top: 20px;
                    }}
                    </style>
                    <div class="cadre">
                        <p class="clignotant">Indice de productivité agricole simulé :</p>
                        <p>{ipa}</p>
                    </div>
                """, unsafe_allow_html=True)
        

