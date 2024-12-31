import streamlit as st

def dash_ml():
    
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



    # Titre de l'application



    # Chargement des données
    # Load data
    #@st.cache_data
    
