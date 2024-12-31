import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import plotly.express as px
from Datas.data_link import data_dir
# Titre de l'application avec un fond blanc


def dash_taux_emploi():
        
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
    st.sidebar.write("## Navigation")
    st.sidebar.write("Aller ")
    titres_onglets = ["Analyse par région 🌍", "Analyse par pays 🏳", "Analyse comparative ↔ 📊"]

    #onglets = st.tabs(titres_onglets)

    ## chargement de la premère base 
    data_path=data_dir('base_streamlit_storytellers.xlsx')
    base=pd.read_excel(data_path,sheet_name="Taux_emploi_chomage_Afrique")
    ## chargement de la deuxième base de données

    data=pd.read_excel(data_path,sheet_name="Taux_emploi_chomage_Afrique1")
   
    onglets_selectionnee=st.sidebar.radio("Forme d'analyse",titres_onglets)
    if onglets_selectionnee=="Analyse par région 🌍":
        st.write("## 1.Analyse selon les régions Africaines")
        # importations toute la base
        st.write("###  1.1 Evolution du Taux d'emploi par Région et par sexe")
    



        Region_afrique=['Central Africa','Eastern Africa', 'Southern Africa', 'Western Africa','Northern Africa']

        data_region=base[base["Region"].isin(Region_afrique)]

        data_region_sexe=data_region[data_region["Age"]=="Age (Jeunes, adultes) : 15-64 ans"]


        # Sélection interactive de l'année


        selected_year = st.selectbox("Sélectionnez une année :", sorted(data_region_sexe["Annee"].unique()))

        # Filtrer les données pour l'année sélectionnée
        data_filtered = data_region_sexe[data_region_sexe["Annee"] == selected_year]

        # Pivot des données pour structurer les colonnes "Hommes", "Femmes", "Total"
        data_pivot = data_filtered.pivot(index="Region", columns="Sexe", values="Taux_emploi").reset_index()
        #col = st.columns((1,2), gap='medium')
        #with col[1]:
            # Création du graphique avec Plotly
        fig = go.Figure()

            # Ajout de la barre "Total"
        #if "Total" in data_pivot.columns:
        #       fig.add_trace(go.Bar(
        #           x=data_pivot['Region'],
        #          y=data_pivot['Total'],
        #         name="Total",
        #          marker_color='blue',
        #     ))

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
                title=f"Taux de d'emploi par région et sexe en {selected_year}",
                title_font_color="black",  # Couleur du titre en noir
                xaxis_title="Région",
                yaxis_title="Taux d'emploi (%)",
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
        st.plotly_chart(fig)
        st.write("Source:Données issues de ILOSTAT")


        st.write("### 1.2 Analyse du taux d'emploi par Région et par Tranche d'âge de la population active")
        # Choix de la region
        selected_Region=st.selectbox("Filtrez selon la  Region d'Afrique :", Region_afrique)



        # Fonction pour tracer la courbe
        def plot_employment_rate_evolution(df, year_col='Annee', employment_col='Taux_emploi', age_col='Age'):
            """
            Tracer l'évolution du taux d'emploi en fonction des années et des catégories d'âge avec Plotly.

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
                title="Évolution du taux de d'emploi",
                labels={"Année",  "Taux d'emploi",  "Tranche d'âge"}
            )
            fig.update_traces(mode="lines")  # Ajouter des points sur la courbe
            fig.update_layout(
                template="plotly_white",
                hovermode="x unified",
                xaxis_title="Année",
                yaxis_title="Taux d'emploi (%)",
                legend_title="Tranche d'âge"
            )
            return fig



        # Application Streamlit
        #st.title("Analyse de l'évolution du taux de d'emploi")
        #st.write("Sélectionnez une tranche d'âge pour visualiser son évolution ou affichez toutes les catégories.")



        data_region_age=data_region[data_region["Sexe"]=="Total"]

        # Affichage du graphique
        fig = plot_employment_rate_evolution(data_region_age[data_region_age["Region"]==selected_Region])
        st.plotly_chart(fig)
        #La source des données
        st.write("Source:Caculs de l'auteur,ILOSTAT")


    if onglets_selectionnee=="Analyse par pays 🏳":
        st.write("## 2.Analyse du taux de l'emploi selon les pays")
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
                value_vars=["Ratio_emploi/population(15+,Femmes)","Ratio_emploi/population(15+,Hommes)",
                            "Ratio_emploi/population(15+)","Ratio_emploi/population(15-24ans,femmes)",
                            "Ratio_emploi/population(15-24ans,hommes)","Ratio_emploi/population(15-24ans,Total)"],

    #", "Chômage_hommes ", "chômage_pays","Chômage_jeunes_femmes","Chômage_jeunes_hommes"], 
                var_name="Catégorie", 
                value_name="emploi /population active")
            
            
            # Création du graphique interactif
            fig = px.line(
                df_melted,
                x=year_col,
                y="emploi /population active",
                color="Catégorie",
                markers=False,
                labels={year_col: "Année", "Ratio emploi/population": "emploi/population (%)", "Catégorie": "Catégorie"},
                title="Évolution du ratio emploi/population active par sexe et âge"
            )

            fig.update_layout(
                template="plotly_white",
                hovermode="x unified",
                legend=dict(title="Catégorie", orientation="h", y=-0.2),
                height=500
            )

            
            st.plotly_chart(fig)

        
        plot_employment_evolution(data_pays)
        st.write("Sources: Calculs de l'auteur, Banque mondiale(WDI)")

        ### Commentaire automatique

        def commentaire(df: pd.DataFrame, year_col: str = 'Annee', country: str = None) -> None:
            """
            Génère un commentaire automatique sur les tendances du ratio emploi/population.

            Args:
                df: Le DataFrame contenant les données.
                year_col: La colonne indiquant les années.
                country: Le pays sélectionné pour le commentaire.
            """
            # Réorganisation des données pour un format long
            df_melted = df.melt(
                id_vars=[year_col],
                value_vars=["Ratio_emploi/population(15+,Femmes)", "Ratio_emploi/population(15+,Hommes)",
                            "Ratio_emploi/population(15+)", "Ratio_emploi/population(15-24ans,femmes)",
                            "Ratio_emploi/population(15-24ans,hommes)", "Ratio_emploi/population(15-24ans,Total)"],
                var_name="Catégorie",
                value_name="Emploi/Population"
            )

            # Calcul des statistiques par catégorie
            stats = (
                df_melted.groupby("Catégorie")
                .apply(lambda group: pd.Series({
                    "Tendance": "croissante" if group["Emploi/Population"].iloc[-1] > group["Emploi/Population"].iloc[0] else "décroissante",
                    "Variation": (group["Emploi/Population"].iloc[-1] - group["Emploi/Population"].iloc[0]) / group["Emploi/Population"].iloc[0] * 100,
                    "Annee_max": group.loc[group["Emploi/Population"].idxmax(), year_col],
                    "Valeur_max": group["Emploi/Population"].max(),
                }))
                .reset_index()
            )

            # Génération du commentaire
            commentaire_text = f"### Analyse des tendances pour {country} :\n\n"
            for _, row in stats.iterrows():
                tendance = row["Tendance"]
                variation = row["Variation"]
                categorie = row["Catégorie"]
                annee_max = int(row["Annee_max"])
                valeur_max = row["Valeur_max"]

                commentaire_text += (
                    f"- **{categorie}** : tendance {tendance} avec une variation de {variation:.2f}%.\n"
                    f" Le ratio emploi/population active a été le plus élevé en {annee_max} avec une valeur de {valeur_max:.2f}.\n"
                )

                # Ajout d'explications adaptées
                if tendance == "décroissante":
                    if "Femmes" in categorie:
                        commentaire_text += (
                        f" La population active de sexe feminin croît probablement plus vite que les emplois des femmes ({select_pays}).\n"
                    )
                    elif "Hommes" in categorie:
                        commentaire_text += (
                        f" La population des Hommes en activité croît probablement plus vite que les emplois des hommes ({select_pays}).\n")
                    elif "15-24ans" and "Total" in categorie:
                        commentaire_text += (
                        f" La population des jeunes  en activité croît probablement plus vite que les emplois des hommes ({select_pays}).\n")
                
                    elif "Ratio_emploi/population(15+)" in categorie:
                        commentaire_text += f"  Ainsi la population active croît plus vite que le nombre d'emploi ({select_pays}).\n"

            

            # Affichage dans Streamlit
            st.write(commentaire_text)

        commentaire(data_pays, year_col='Annee', country=select_pays)

    ## l'onglet Analyse comparative



    if onglets_selectionnee == "Analyse comparative ↔ 📊":
        st.write("## 3. Analyse comparative : Cartographie des pays africains selon le niveau d'emploi")
        st.write("### 3.1 Aperçu général du taux d'emploi")

        selected_color_theme = "blues"
        annees = data["Annee"].unique()

        # Sélection de l'année via un slider
        selected_year = st.sidebar.slider(
            "Sélectionnez une année :",
            min_value=int(min(annees)),
            max_value=int(max(annees)),
            value=int(min(annees)),  # Valeur par défaut
            step=1
        )

        # Filtrer les données pour l'année sélectionnée
        df_selected_year = data[data["Annee"] == selected_year]

        def make_choropleth(
            df_selected_year,
            input_id,
            input_column,
            input_color_theme="reds",
            source_text="Source: Données officielles",
            chart_title="Carte Choroplèthe - Ratio emploi/population active",
        ):
            """
            Crée une carte choroplèthe avec une interface personnalisée en blanc et détecte les pays sans données.
            """
            # Vérifier si le DataFrame n'est pas vide
            if df_selected_year.empty or df_selected_year[input_column].isnull().all():
                st.error(f"Aucune donnée disponible pour {input_column}.")
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
                labels={input_column: "Emploi / Population active (%)"},
            )

            # Mise à jour de la mise en page
            choropleth.update_layout(
                template="plotly_white",
                plot_bgcolor="rgba(255, 255, 255, 1)",
                paper_bgcolor="rgba(255, 255, 255, 1)",
                margin=dict(l=0, r=0, t=50, b=50),
                height=400,
                title=dict(
                    text=chart_title,
                    x=0.5,
                    xanchor="center",
                    font=dict(size=16, color="black"),
                ),
                coloraxis_colorbar=dict(
                    title="Ratio emploi / population",
                    tickvals=[0, max(df_selected_year[input_column]) / 2, max(df_selected_year[input_column])],
                    ticktext=["Bas", "Moyen", "Haut"],
                    titlefont=dict(size=14, color="black"),
                    tickfont=dict(color="black"),
                ),
                annotations=[
                    dict(
                        text=source_text,
                        x=0.5,
                        y=-0.1,
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        font=dict(size=12, color="black"),
                        align="center",
                    )
                ],
            )

            return choropleth

        # Carte principale
        choropleth = make_choropleth(
            df_selected_year, "Pays", "Ratio_emploi/population(15+)", selected_color_theme
        )
        if choropleth:
            st.plotly_chart(choropleth, use_container_width=True)

        st.write("### 3.2 Analyse des inégalités entre hommes et femmes d'accès à l'emploi")

        # Cartes comparatives pour les hommes et les femmes
        
        
        st.write(f"##### Ratio emploi population active "+ str(selected_year))
        col=st.columns(2)
        if col[0]:
            choropleth_gender = make_choropleth(
                df_selected_year, "Pays", "Ratio_emploi/population(15+,Hommes)", selected_color_theme, "Sources:calaculs, Banque mondiale", "Cas des hommes"
            )
            if choropleth_gender:
                st.plotly_chart(choropleth_gender, use_container_width=True)
            choropleth_gender = make_choropleth(
                df_selected_year, "Pays", "Ratio_emploi/population(15+,Femmes)", selected_color_theme, "Sources:calaculs, Banque mondiale", "Cas des femmes"
            )
            if choropleth_gender:
                st.plotly_chart(choropleth_gender, use_container_width=True)




        st.write(f"##### Ratio emploi population active des jeunes "+ str(selected_year))
        col=st.columns(2)
        if col[0]:
            choropleth_gender = make_choropleth(
                df_selected_year, "Pays", "Ratio_emploi/population(15-24ans,hommes)", selected_color_theme, "Sources:calaculs, Banque mondiale", "Cas des jeunes hommes"
            )
            if choropleth_gender:
                st.plotly_chart(choropleth_gender, use_container_width=True)
            choropleth_gender = make_choropleth(
                df_selected_year, "Pays", "Ratio_emploi/population(15-24ans,femmes)", selected_color_theme, "Sources:calaculs, Banque mondiale", "Cas des jeunes filles"
            )
            if choropleth_gender:
                st.plotly_chart(choropleth_gender, use_container_width=True)
