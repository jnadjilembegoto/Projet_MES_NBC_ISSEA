import streamlit as st
from PIL import Image
from Photos.photo_link import main_dir
from Pages_utiles.About_us  import about_us_page

logo_path = main_dir("drapeau_tchad.png")
logo = Image.open(logo_path)
#eaf6ff
#d0e6f5
#1f77b4
#32CD32
def accueil_load(): 
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
        # Sidebar
    with st.sidebar:
        st.title('🏠 Accueil')
         
    
    col = st.columns((1.5, 4.5), gap='medium')
    with col[0]:
        st.image(logo,use_column_width=True)
    with col[1]:
        st.title("IMPACT DU CHANGEMENT CLIMATIQUE SUR LA PRODUCTION AGRICOLE AU TCHAD")
    st.markdown('---')
    st.title("Analyse Interactive et simulation d'impact de la variation relative d'une variable exogène sur les variables endogènes de notre système")
    st.markdown('Créé par **NADJILEM Bégoto** et **NGUEKORAL Chancéline**')
    st.markdown("Sous l'encadrement de **M. CHASSEM**")
    st.sidebar.markdown('---')
    st.sidebar.markdown("## Base de données utilisée")
    st.sidebar.markdown("""[*Données appurées*](https://github.com/jnadjilembegoto/Projet_MES_NBC_ISSEA)
                        """)
    st.sidebar.markdown('---')
    st.sidebar.markdown("## Scripts de l'application")
    st.sidebar.markdown("""[*Code de l'application*](https://github.com/jnadjilembegoto/Projet_MES_NBC_ISSEA)
                        """)
    st.markdown('---')
    st.markdown(
        """
        ### Résumé
        Comprendre les variables climatiques qui agissent sur la production agricole au Tchad 
        """
    )
    st.markdown('---')

    st.markdown(
        """
        ### Utilisation de l'application

        A gauche se trouve le ménu déroulant pour naviguer dans les différents tableaux de board :

        - **Accueil:** We are here!
        - **Dynamique de la population active:** Un aperçu sur la proportion des personnes âgées de 15 à 64 ans dans un pays
        - **Emploi-Activité économique:** Une description des trois secteurs d'activités clés (agriculture, industrie et service)
        - **Démographie:** Une présentation générale de la démographie du Tchad suivant les années
        - **Environnement-Agriculture:** Une présentation des indicateurs climatique et environnemental
        - **Simulation:** Une simulation de l'impact de la variation relative d'une variable exogène sur les variables endogènes de notre système
        - **About us:** Une présentation de tous les membres de la Data Storytellers Team.
        """
    )
    st.markdown("---")
    st.markdown("""
                Version 1.0 du 31 décembre 2024
                """)
    st.sidebar.markdown('---')
    #st.sidebar.markdown("## Qui sommes nous?")
    #if st.sidebar.markdown("[About us](#)", unsafe_allow_html=True):
     #   about_us_page()
    #titres_onglets = ["About us"]
    #onglets_selectionnee=st.sidebar.radio(" ",titres_onglets)
    #if onglets_selectionnee== "About us":
        #about_us_page()
