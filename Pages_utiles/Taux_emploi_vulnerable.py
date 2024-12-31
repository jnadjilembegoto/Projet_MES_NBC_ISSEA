import pandas as pd
import streamlit as st
import plotly.express as px
from Datas.data_link import data_dir
    # Style personnalisé pour l'application
    # CSS personnalisé pour l'arrière-plan
def dash_taux_empl_vul():
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

    #

    # Chargement des données
    data_path=data_dir('base_streamlit_storytellers.xlsx')
    data = pd.read_excel(data_path,sheet_name='Emploi_vuln')




    ## Les cartes
    annees=data["Annee"].unique()
    selected_year_vulneralble = st.sidebar.slider(
            "Sélectionnez une année :",
            min_value=min(annees),
            max_value=max(annees),
            value=min(annees),  # Valeur par défaut
            step=1
        )


    base=data[data["Annee"]==selected_year_vulneralble]

    def make_choropleth(
            df_selected_year, 
            input_id, 
            input_column, 
            input_color_theme="reds", 
            source_text="Source: Nos Claculs, Banque Mondiale", 
            chart_title="Carte Choroplèthe - Taux d'emploi vulérable en Afrique"
        ):
            """
            Crée une carte choroplèthe avec une interface personnalisée en blanc et détecte les pays sans données.

            Args:
                df_selected_year (pd.DataFrame): Données filtrées pour l'année sélectionnée.
                input_id (str): Colonne contenant les noms des pays.
                input_column (str): Colonne contenant les valeurs à afficher (ex. taux d'emploi).
                input_color_theme (str): Palette de couleurs à utiliser.
                source_text (str): Texte de la source à afficher en bas de la carte.
                chart_title (str): Titre de la carte.

            Returns:
                plotly.graph_objects.Figure: La carte choroplèthe.
            """
            
            # Vérifier si le DataFrame n'est pas vide
            if df_selected_year.empty or df_selected_year[input_column].isnull().all():
                st.error("Les données sont insuffisantes pour tracer la carte.")
                return None

            # Créer la carte choroplèthe
            choropleth = px.choropleth(
                data_frame=df_selected_year,
                locations=input_id,
                color=input_column,
                locationmode="country names",
                color_continuous_scale=input_color_theme,
                range_color=(0, max(df_selected_year[input_column])),
                scope="africa",
                labels={input_column: 'Taux emploie vulnérable(%)'}
            )

            # Mise à jour de la mise en page avec un thème blanc
            choropleth.update_layout(
                template='plotly_white',  # Thème blanc
                plot_bgcolor='rgba(255, 255, 255, 1)',  # Couleur blanche pour le fond du graphique
                paper_bgcolor='rgba(255, 255, 255, 1)',  # Couleur blanche pour l'arrière-plan global
                margin=dict(l=0, r=0, t=50, b=50),  # Ajustement des marges
                height=400,  # Hauteur du graphique
                title=dict(
                    text=chart_title,  # Titre personnalisé
                    x=0.5,  # Centrage du titre
                    xanchor='center',
                    font=dict(size=16, color='black')  # Couleur et taille du texte du titre
                ),
                coloraxis_colorbar=dict(
                    title="Taux emploie vulnérable",
                    tickvals=[0, max(df_selected_year[input_column]) / 2, max(df_selected_year[input_column])],
                    ticktext=["Bas", "Moyen", "Haut"],
                    titlefont=dict(size=14, color='black'),
                    tickfont=dict(color='black')
                ),
                annotations=[
                    dict(
                        text=source_text,  # Texte de la source
                        x=0.5,  # Position horizontale (centré)
                        y=-0.1,  # Position verticale (en bas, hors de la carte)
                        showarrow=False,  # Pas de flèche
                        xref="paper",  # Référence horizontale relative à la mise en page
                        yref="paper",  # Référence verticale relative à la mise en page
                        font=dict(size=12, color="black"),  # Style de police
                        align="center"  # Alignement du texte
                    )
                ]
            )

            return choropleth

    base_Total=base[base["Sexe"]=="Total"]
        ## Construction de la carte
    st.write("## Aperçu general sur les emplois vulnérables en Afrique")

    selected_color_theme="reds"
        
    choropleth = make_choropleth(base_Total, "Pays", "Taux_emplois_vulnerable",selected_color_theme)
    if choropleth:
            st.plotly_chart(choropleth, use_container_width=True)

    st.write("## 2.Taux d'emplois vulenrabe par sexe")

    base_homme=base[base["Sexe"]=="Homme"]
    base_femme=base[base["Sexe"]=="Femme"]
    col=st.columns(2)
    with col[0]:
        

        choropleth_homme= make_choropleth(base_homme, "Pays", "Taux_emplois_vulnerable",selected_color_theme,
                                        chart_title="Cas des Hommes")
        if choropleth_homme:
                st.plotly_chart(choropleth_homme, use_container_width=True)

    with col[1]:
        choropleth_femme= make_choropleth(base_femme, "Pays", "Taux_emplois_vulnerable",selected_color_theme,chart_title="Cas des femmes")
        if choropleth_femme:
                st.plotly_chart(choropleth_femme, use_container_width=True)


