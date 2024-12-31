import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import plotly.express as px
from Datas.data_link import data_dir
from Pages_utiles.Emploi_vulnerable import emploi_vul# ici c'est travailleur pauvre
from Pages_utiles.Taux_emploi_vulnerable import dash_taux_empl_vul

data_path=data_dir('base_streamlit_storytellers.xlsx')
## Definition de fonction pour gerer sidebar

#pd.read_excel(data_path,sheet_name="Secteur_prof_ais")


def dash_sect_informel():   
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
    st.header("Défis de l'emploi")

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
    # Curseur pour sélectionner une année
    st.sidebar.markdown('---')
    st.sidebar.write("## 👷‍♂️ 🛠️ Emploi informel et vulnérable")
    st.sidebar.write("Aller ")
    titres_onglets = ["Analyse par région 🌍", "Analyse par pays 🏳", "Analyse comparative ↔ 📊"," Travailleur pauvre","Taux d'emploi vulnérable"]

    #onglets = st.tabs(titres_onglets)
    onglets_selectionnee=st.sidebar.radio("Forme d'analyse",titres_onglets)
    if onglets_selectionnee=="Analyse par région 🌍":
        st.write("## 1.Secteur informel:Taux d'emploi informel par région")
        data=pd.read_excel(data_path,
                        sheet_name="Infomel_Region")
        #data_Africa=data[data["Region"]=="Africa"]
        data_Africa_total=data[data["Sexe"]=="Total"]




        

        #recuperons les données pour faire les rectangles
    
        annees =data_Africa_total["Annee"].unique()
        annee_selectionnee = st.slider(
            "Sélectionnez une année :",
            min_value=min(annees),
            max_value=max(annees),
            value=min(annees),  # Valeur par défaut
            step=1
        )


        data_Africa_total_annee=data_Africa_total[data_Africa_total["Annee"]==annee_selectionnee]


        #recuperons les données pour faire les rectangles
        noms_pays = data_Africa_total_annee["Region"].values
        valeur = data_Africa_total_annee["Taux_emploi_informel"].values

        # Combiner les noms de pays et les taux informels dans une liste de tuples
        regions_taux = list(zip(noms_pays, valeur))

        # Séparer l'Afrique du reste des régions
        afrique = [region for region in regions_taux if region[0] == "Africa"]  # Assurez-vous que "Afrique" est bien dans les données
        autres_regions = [region for region in regions_taux if region[0] != "Africa"]

        # Trier les autres régions par taux informel de manière décroissante
        autres_regions_sorted = sorted(autres_regions, key=lambda x: x[1], reverse=True)

        # Reconstituer la liste avec "Afrique" en premier, suivie des autres régions triées
        regions_taux_sorted = afrique + autres_regions_sorted

        # Séparer à nouveau les noms de regions et les taux informels triés
        noms_pays_sorted, valeur_sorted = zip(*regions_taux_sorted)

        # Créer le premier rectangle centré en haut avec "Afrique"
        st.markdown(
            f"""
            <div style="background-color: #FF0000; padding: 20px; border-radius: 10px; width: 300px; margin: 20px auto;">
                <h3 style="text-align: center; color: white;">Afrique</h3>
                <p style="text-align: center; font-size: 24px; color: white;">{valeur_sorted[0]}%</p>
            </div>
            """, unsafe_allow_html=True
        )

        # Afficher les autres rectangles trois par ligne
        cols = st.columns(3)  # Créer trois colonnes pour placer les rectangles

        # Afficher les autres régions dans les rectangles suivants
        for i in range(1, len(noms_pays_sorted)):
            col = cols[(i - 1) % 3]  # Choisir la colonne en fonction de l'index
            with col:
                st.markdown(
                    f"""
                    <div style="background-color: #FF0000; padding: 0.5px; border-radius: 0.5px; margin: 1px;">
                        <h3 style="text-align: center; color: white;">{noms_pays_sorted[i]}</h3>
                        <p style="text-align: center; font-size: 24px; color: white;">{valeur_sorted[i]}%</p>
                    </div>
                    """, unsafe_allow_html=True
                )



        # Construction des Histogrammes

        data_Africa_sexe=data[data["Annee"]==annee_selectionnee]

        data_Africa_sexe=data_Africa_sexe[data_Africa_sexe["Sexe"].isin(["Feminin", "Masculin"])]


        # Pivot des données pour structurer les colonnes "Hommes", "Femmes", "Total"
        data_pivot = data_Africa_sexe.pivot(index="Region", columns="Sexe", values="Taux_emploi_informel").reset_index()
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
                title=f"Taux d'emploi informel par région et sexe en {annee_selectionnee}",
                title_font_color="black",  # Couleur du titre en noir
                xaxis_title="Région",
                yaxis_title="Taux d'emploi informel (%)",
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
                height=300,  # Augmenter la hauteur du graphique pour une meilleure visibilité
            )

            # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig)
        st.write("Sources:Données issues de ILOSTAT")
        ##"##############################################################################"""

    if onglets_selectionnee=="Analyse par pays 🏳":
        st.sidebar.empty()
        st.write("## 2.Analyse selon le pays")


        base=pd.read_excel(data_path,sheet_name="Secteur_Activite_Pays")

        select_pays=st.selectbox(" Filtrer selon le pays", base["Pays"].unique() )
        

        
        #Fitre du pays
        base_pays=base[base["Pays"]==select_pays]
        annees=base_pays["Annee"].unique()
        annee_selectionnee = st.selectbox("Filtrer selon l'année ", annees)
    
        #base_pays=base[base["Pays"]==select_pays]
        #select_annee=gestion_sidebar(base_pays,1)
        base_pays_annee=base_pays[base_pays["Annee"]==annee_selectionnee]
        #base_pays_annee_Sexe=base_pays_annee[base_pays_annee["Sexe"]=="Total"]
        noms_secteur=base_pays_annee["Secteur"].values

        valeur_secteur=list(base_pays_annee["Taux_emploi_informel"].values)
        st.write("## Le taux d'emploi informel dans l'Economie et par differents secteurs de "+ select_pays)
        # Afficher les autres rectangles trois par ligne
        cols = st.columns(len(base_pays_annee["Secteur"].unique()))  # Créer trois colonnes pour placer les rectangles
        
        # Afficher les autres régions dans les rectangles suivants
        for i in range(0,len(base_pays_annee["Secteur"].unique())):
            col = cols[i]  # Choisir la colonne en fonction de l'index
            with col:
                st.markdown(
                    f"""
                    <div style="background-color: #FF0000; padding: 2px; border-radius: 2px; margin: 1px;">
                        <h3 style="text-align: center; color: white;">{noms_secteur[i]}</h3>
                        <p style="text-align: center; font-size: 24px; color: white;">{valeur_secteur[i]}%</p>
                    </div>
                    """, unsafe_allow_html=True
                )



    if onglets_selectionnee=="Analyse comparative ↔ 📊":
        st.write("## 3.1 Analyse comparative:Cartographie")


        data=pd.read_excel(data_path,
                        sheet_name="Secteur_Activite_Pays")

        data_Africa_total=data[data["Sexe"]=="Total"]
        data_Africa_Secteur=data_Africa_total[data_Africa_total["Secteur"]=="Economie"]
        #
        ## Ecrivons la fonction pour faire la carte

        def make_choropleth(
            df_selected_year, 
            input_id, 
            input_column, 
            input_color_theme="reds", 
            source_text="Source: Données officielles", 
            chart_title=""
        ):
            if df_selected_year.empty or df_selected_year[input_column].isnull().all():
                st.error("Les données sont insuffisantes pour tracer la carte.")
                return None

            choropleth = px.choropleth(
                data_frame=df_selected_year,
                locations=input_id,
                color=input_column,
                locationmode="country names",
                color_continuous_scale=input_color_theme,
                range_color=(0, max(df_selected_year[input_column].dropna())),
                scope="africa",
                labels={input_column: 'Taux emploi informel (%)'}
            )

            choropleth.update_layout(
                template='plotly_white',
                plot_bgcolor='rgba(255, 255, 255, 1)',
                paper_bgcolor='rgba(255, 255, 255, 1)',
                margin=dict(l=0, r=0, t=50, b=50),
                height=400,
                title=dict(
                    text=chart_title,
                    x=0.5,
                    xanchor='center',
                    font=dict(size=16, color='black')
                ),
                coloraxis_colorbar=dict(
                    title="Taux d'emploi",
                    tickvals=[0, max(df_selected_year[input_column].dropna()) / 2, max(df_selected_year[input_column].dropna())],
                    ticktext=["Bas", "Moyen", "Haut"],
                    titlefont=dict(size=14, color='black'),
                    tickfont=dict(color='black')
                ),
                annotations=[
                    dict(
                        text=source_text,
                        x=0.5,
                        y=-0.2,
                        showarrow=False,
                        font=dict(size=12, color="black"),
                        align="center"
                    )
                ]
            )

            return choropleth



        selected_year = st.sidebar.selectbox("Choisissez une année", data_Africa_Secteur["Annee"].unique())
        df_selected_year = data_Africa_Secteur[data_Africa_Secteur["Annee"] == selected_year]

        

        selected_color_theme = "reds"
        choropleth = make_choropleth(
            df_selected_year, 
            "Pays", 
            "Taux_emploi_informel", 
            selected_color_theme, 
            chart_title="Carte Choroplèthe - Taux d'emploi informel en Afrique  en " + str(selected_year)
        )

        if choropleth:
            st.plotly_chart(choropleth, use_container_width=True)

        st.write("Sources : Données issues de ILOSTAT")



        


        data_Africa_total=data[data["Sexe"]=="Masculin"]
        data_Africa_Secteur=data_Africa_total[data_Africa_total["Secteur"]=="Economie"]
        #selected_year_Compar = st.sidebar.selectbox("Choisissez une année", data_Africa_Secteur["Annee"].unique())
        df_selected_Hommes = data_Africa_Secteur[data_Africa_Secteur["Annee"] == selected_year]
        selected_color_theme = "reds"
        choropleth_Hommes = make_choropleth(
            df_selected_Hommes, 
            "Pays", 
            "Taux_emploi_informel", 
            selected_color_theme, 
            chart_title="Taux d'emploi informel des Hommes en " + str(selected_year)
        )

        

    # Cartographie pour les femmes
        data_Africa_total=data[data["Sexe"]=="Feminin"]
        data_Africa_Secteur=data_Africa_total[data_Africa_total["Secteur"]=="Economie"]
        #selected_year = st.sidebar.selectbox("Choisissez une année", data_Africa_Secteur["Annee"].unique())
        df_selected_Femmes= data_Africa_Secteur[data_Africa_Secteur["Annee"] == selected_year]
        selected_color_theme = "reds"
        choropleth_Femmes = make_choropleth(
            df_selected_Femmes, 
            "Pays", 
            "Taux_emploi_informel", 
            selected_color_theme, 
            chart_title="Taux d'emploi informel des femmes en " + str(selected_year)
        )
        st.write(" Les pays de disposant pas de données à l'année "+str(selected_year)+ " seront illustrés par la couleur blanche sur la carte")
        col=st.columns(2)
        with col[0]:
            st.plotly_chart(choropleth_Hommes, use_container_width=True)
        with col[1]:
            st.plotly_chart(choropleth_Femmes, use_container_width=True)
        st.write("Sources:Données issues de ILOSTAT")
    if onglets_selectionnee== " Travailleur pauvre":
         emploi_vul()
    if onglets_selectionnee== "Taux d'emploi vulnérable":
         dash_taux_empl_vul()
              


