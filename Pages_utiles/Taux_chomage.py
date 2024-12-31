import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import plotly.express as px

from Datas.data_link import data_dir
def dash_chom():
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

    #
    # Titre de l'application


    st.title("Apercu sur le taux de chômage en Afrique")

    # Chargement des données
    data_path=data_dir('base_streamlit_storytellers.xlsx')
    data=pd.read_excel(data_path,sheet_name="Taux_chomage_Afrique")
    base=pd.read_excel(data_path,sheet_name="Taux_emploi_chomage_Afrique")
    #""""""""""""""""""""""""""""""""""""""""""""""
    titres_onglets = ["Analyse par région 🌍", "Analyse par pays 🏳", "Analyse comparative ↔ 📊"]

    #onglets = st.tabs(titres_onglets)
    onglets_selectionnee=st.sidebar.radio("Forme d'analyse",titres_onglets)
    if onglets_selectionnee=="Analyse par région 🌍":
        st.write("### 1.Analyse selon les régions Africaines")
        # importations toute la base
        st.write("####  1.1 Evolution du Taux de chômage par Région et par sexe")
        

        Region_afrique=['Central Africa','Eastern Africa', 'Southern Africa', 'Western Africa','Northern Africa']

        data_region=base[base["Region"].isin(Region_afrique)]

        data_region_sexe=data_region[data_region["Age"]=="Age (Jeunes, adultes) : 15-64 ans"]


        # Sélection interactive de l'année

        annees=data_region_sexe["Annee"].unique()
        selected_year = st.sidebar.slider(
            "Sélectionnez une année :",
            min_value=min(annees),
            max_value=max(annees),
            value=min(annees),  # Valeur par défaut
            step=1
        )
        #selected_year = st.selectbox("Sélectionnez une année :", sorted(data_region_sexe["Annee"].unique()))

        # Filtrer les données pour l'année sélectionnée
        data_filtered = data_region_sexe[data_region_sexe["Annee"] == selected_year]

        # Pivot des données pour structurer les colonnes "Hommes", "Femmes", "Total"
        data_pivot = data_filtered.pivot(index="Region", columns="Sexe", values="Taux_chomage").reset_index()
        #col = st.columns((1,2), gap='medium')
        #with col[1]:
            # Création du graphique avec Plotly
        fig = go.Figure()

            # Ajout de la barre "Masculin"
        if "Masculin" in data_pivot.columns:
                fig.add_trace(go.Bar(
                    x=data_pivot['Region'],
                    y=data_pivot['Masculin'],
                    name="Masculin",
                    marker_color='#A10000',
                ))

            # Ajout de la barre "Feminin"
        if "Feminin" in data_pivot.columns:
                fig.add_trace(go.Bar(
                    x=data_pivot['Region'],
                    y=data_pivot['Feminin'],
                    name="Feminin",
                    marker_color='#0067A5',
                ))

            # Mise en forme du graphique interactif avec Plotly
        fig.update_layout(
                title=f"Taux de de chômage par région et sexe en {selected_year}",
                title_font_color="black",  # Couleur du titre en noir
                xaxis_title="Région",
                yaxis_title="Taux de chômage (%)",
                xaxis_title_font_color="black",  # Couleur du titre de l'axe X
                yaxis_title_font_color="black",  # Couleur du titre de l'axe Y
                template="plotly_white",  # Utilisation du template Plotly White pour fond blanc
                barmode='group',  # Groupement des barres
                plot_bgcolor='white',  # Fond blanc pour le graphique
                paper_bgcolor='white',  # Fond blanc pour l'ensemble de l'application
                legend_title="Sexe",
                legend_title_font_color="black",  # Légende en noir
                legend_font_color="black",  # Texte de la légende en noir
                font=dict(color="black"),  # Texte général en noir
                height=600,  # Augmenter la hauteur du graphique pour une meilleure visibilité
            )

            # Affichage du graphique interactif dans Streamlit
        if fig:
            st.plotly_chart(fig)
            st.write("Sources:Données issues de ILOSTAT")


        st.write("#### 1.2 Analyse du taux de chômage par Région et par Tranche d'âge de la population active")
        # Choix de la region
        selected_Region=st.selectbox("Filtrez selon la  Region d'Afrique :", Region_afrique)



        # Fonction pour tracer la courbe
        def plot_employment_rate_evolution(df, year_col='Annee', employment_col='Taux_chomage', age_col='Age'):
            """
            Tracer l'évolution du taux de chomage en fonction des années et des catégories d'âge avec Plotly.

            Args:
                df (pd.DataFrame): DataFrame contenant les données.
                year_col (str): Nom de la colonne représentant les années.
                unemployment_col (str): Nom de la colonne représentant le taux de chômage.
                age_col (str): Nom de la colonne représentant les catégories d'âge.
                selected_age (str, optional): Tranche d'âge à afficher. Si None, toutes les catégories seront affichées.

            Returns:
                plotly.graph_objects.Figure: Graphique interactif.
            """
            
            fig = px.line (
                df,
                x=year_col,
                y=employment_col,
                color=age_col, 
                title="Évolution du taux de chômage",
                labels={"Année",  "Taux de chômage",  "Tranche d'âge"}
            )
            fig.update_traces(mode="lines")  # Ajouter des points sur la courbe
            fig.update_layout(
                template="plotly_white",
                hovermode="x unified",
                xaxis_title="Année",
                yaxis_title="Taux de chômage (%)",
                legend_title="Tranche d'âge"
            )
            return fig


        data_region_age=data_region[data_region["Sexe"]=="Total"]

        # Affichage du graphique
        fig = plot_employment_rate_evolution(data_region_age[data_region_age["Region"]==selected_Region])
        if fig:
            st.plotly_chart(fig)
    

        st.write("Sources:Données issues de ILOSTAT")

    if onglets_selectionnee=="Analyse par pays 🏳":
        st.write("# 2.Analyse du taux de chômage  selon les pays")
        
        

        

        select_pays=st.selectbox("Choisir le pays", data["Pays"].unique())
        data_pays=data[data["Pays"]==select_pays]
        def plot_employment_evolution(df: pd.DataFrame, year_col: str = 'Annee'):
            """
            Trace l'évolution du chômage des femmes, des hommes et total.

            Args:
                df: Le DataFrame contenant les données.
                year_col: Le nom de la colonne pour les années.
            """
            # Réorganisation des données pour un format long
            df_melted = df.melt(
                id_vars=[year_col], 
                value_vars=["Chômage_femmes", "Chômage_hommes ", "chômage_pays","Chômage_jeunes_femmes","Chômage_jeunes_hommes"], 
                var_name="Catégorie", 
                value_name="Taux de chômage")
            
            
            # Création du graphique interactif
            fig = px.line(
                df_melted,
                x=year_col,
                y="Taux de chômage",
                color="Catégorie",
                markers=True,
                labels={year_col: "Année", "Taux de chômage": "Taux de chômage (%)", "Catégorie": "Catégorie"},
                title="Évolution du taux de chômage (Femmes, Hommes, Total,jeunes femmes, jeunes hommes)"
            )

            fig.update_layout(
                template="plotly_white",
                hovermode="x unified",
                legend=dict(title="Catégorie", orientation="h", y=-0.2),
                height=500
            )

            if fig:
                st.plotly_chart(fig)

        
        plot_employment_evolution(data_pays)
        st.write("Sources: Données issues de WDI")
    ## l'onglet Analyse comparative
    if onglets_selectionnee=="Analyse comparative ↔ 📊":
        st.write("#### 3.Analyse comparative :Cartographie des pays Africains selon le taux de chômage")
        st.write("##### 3.1 Apercu général du taux de chômage")

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme ="reds"
        annees =data["Annee"].unique()
        selected_year = st.sidebar.slider(
            "Sélectionnez une année :",
            min_value=min(annees),
            max_value=max(annees),
            value=min(annees),  # Valeur par défaut
            step=1
        )
        


        def make_choropleth(
            df_selected_year, 
            input_id, 
            input_column, 
            input_color_theme="reds", 
            source_text="Source: Données officielles", 
            chart_title="Carte Choroplèthe - Taux de chômage en Afrique"
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
                labels={input_column: 'Taux de chômage(%)'}
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
                    title="Taux de chômage",
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

        df_selected_year=data[data["Annee"]==selected_year]
        ## Construction de la carte
        
        choropleth = make_choropleth(df_selected_year, "Pays", "chômage_pays",selected_color_theme)
        if choropleth:
            st.plotly_chart(choropleth, use_container_width=True)

        
        st.write("###  3.2 Analyse des inégalités entre Hommes/Femmes")
        
        df_selected_year_Hommes=data[data["Annee"]==selected_year]


        choropleth_hommes= make_choropleth(df_selected_year_Hommes,
                                    "Pays", 
                                    "Chômage_hommes ", 
                                    selected_color_theme,
                                    source_text="Sources:Données issues de ILOSTAT",
                                    chart_title="Taux de chomage des Hommes en "+str(selected_year)

                                    )





        df_selected_year_Femmes=data[data["Annee"]==selected_year]


        ## Cartographie Femmes

        choropleth_femmes= make_choropleth(df_selected_year_Femmes,
                                    "Pays", 
                                    "Chômage_femmes", 
                                    selected_color_theme,
                                    source_text="Sources:Données issues de WDI",
                                    chart_title="Taux de chômage des Femmes en "+str(selected_year)

                                    )


        col = st.columns(2)
        with col[0]:
            if choropleth_hommes:
                st.plotly_chart(choropleth_hommes, use_container_width=True)
        with col[1]:
            if choropleth_femmes:
                st.plotly_chart(choropleth_femmes, use_container_width=True)







        df_selected_year_age1=data[data["Annee"]==selected_year]

        choropleth_age1= make_choropleth(df_selected_year_age1,
                                    "Pays", 
                                    "Chômage_jeunes_femmes", 
                                    selected_color_theme,
                                    source_text="Sources:Données issues de WDI",
                                    chart_title="Taux de chômage des jeunes femmes en "+str(selected_year)

                                    )


        #selected_color_theme="reds"

        df_selected_year_age2=data[data["Annee"]==selected_year]

        choropleth_age2= make_choropleth(df_selected_year_age2,
                                    "Pays", 
                                    "Chômage_jeunes_hommes", 
                                    selected_color_theme,
                                    source_text="Données issues de WDI",
                                    chart_title="Taux de chômage des jeunes hommes en "+str(selected_year)

                                    )

        col=st.columns(2)
        with col[0]:
            if choropleth_age1:
                st.plotly_chart(choropleth_age1,use_container_width=True)
        with col[1]:
            if choropleth:
                st.plotly_chart(choropleth_age2, use_container_width=True)
