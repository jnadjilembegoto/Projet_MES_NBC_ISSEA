
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import plotly.express as px
from Datas.data_link import data_dir

## Importation de la base de données

def dash_chef_entreprise():
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
    def load_data():
         data_path=data_dir('base_streamlit_storytellers.xlsx')
         return pd.read_excel(data_path,sheet_name="chef_entreprises")

    data = load_data()
    st.write("### Importance de la femme dans la gestion des entreprises en Afriques")


    st.write("### 1.Evolution des proportions des chefs d'entreprises(% personnes en emploi)")

    select_pays=st.selectbox("Filtrer selon un pays", data["Pays"].unique())
    data_pays=data[data["Pays"]==select_pays]


    annees =data_pays["Annee"].unique()
    annee_selectionnee = st.slider(
            "Sélectionnez une année :",
            min_value=min(annees),
            max_value=max(annees),
            value=min(annees),  # Valeur par défaut
            step=1
        )


    #base_pays_annee_Sexe=base_pays_annee[base_pays_annee["Sexe"]=="Total"]
    noms_var=["Chefs _entreprise (% )","Chefs_entreprise_femmes (% )","Chefs_entreprise_hommes(%)"]

    data_annee=data_pays[data_pays["Annee"]==annee_selectionnee]

    valeur=list(data_annee[noms_var].values)

    #valeur_secteur=list(base_pays_annee["Taux_emploi_informel"].values)
    st.write("Annee "+str(annee_selectionnee))
    # Afficher les autres rectangles trois par ligne
    cols = st.columns(3)  # Créer trois colonnes pour placer les rectangles

    # Afficher les autres régions dans les rectangles suivants
    for i in range(0,3):
        col = cols[i]  # Choisir la colonne en fonction de l'index
        with col:
            st.markdown(
                f"""
                <div style="background-color: #5D9CEC; padding: 2px; border-radius: 2px; margin: 1px;">
                    <h3 style="text-align: center; color: white;">{noms_var[i]}</h3>
                    <p style="text-align: center; font-size: 24px; color: white;">{valeur[0][i]:.2f}%</p>
                </div>
                """, unsafe_allow_html=True
            )


    st.write("chefs _entreprise (% ):Chefs d’entreprise hommes (% de la population  en emploi)")
    st.write("Chefs_entreprise_femmes (% ):Chefs d’entreprise hommes (% de la population masculine en emploi) ")
    st.write("Chefs_entreprise_hommes(%):Chefs d’entreprise hommes (% de la population masculine en emploi)")



    st.write("### 1.2 Ratio de la proportion chef d'entreprise femmes /proportion chef d'entreprise homme")





    def make_choropleth(
            df_selected_year, 
            input_id, 
            input_column, 
            input_color_theme="reds", 
            source_text="Source: Données officielles", 
            chart_title=""
        ):
        """
        Crée une carte choroplèthe pour afficher les données.
        """
        # Vérifiez si le DataFrame est vide ou si la colonne est entièrement vide
        #if df_selected_year.empty or df_selected_year[input_column].isnull().all():
            #st.error("Les données sont insuffisantes pour tracer la carte.")
            #return None

        # Création de la carte choroplèthe
        try:
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

            # Mise à jour du layout
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
        except Exception as e:
            st.error(f"Erreur lors de la création de la carte : {e}")
            return None


    # Sélection de l'année
    annee_selectionnee2 = st.selectbox("Choisissez une année", data["Annee"].unique())

    # Filtrer les données pour l'année sélectionnée
    data_annee = data[data["Annee"] == annee_selectionnee2]

    # Correction des noms des colonnes
    data_annee = data_annee.rename(columns={"Chefs _entreprise (% )": "Chefs_entreprise"})

    # Génération de la carte
    selected_color_theme = "reds"  # Exemple d'échelle de couleur valide
    choropleth = make_choropleth(
        data_annee, 
        input_id="Pays", 
        input_column="Ratio", 
        input_color_theme=selected_color_theme, 
        chart_title=f"Ratio de la proportion chef d'entreprise femmes /proportion chef d'entreprise homme en {annee_selectionnee2}"
    )

    # Affichage de la carte
    if choropleth:
        st.plotly_chart(choropleth, use_container_width=True)

    st.write("Sources : Données issues de ILOSTAT")


