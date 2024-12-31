import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.express as px
from Datas.data_link import data_dir
#from Pages_utiles.Dashboard_pop_active import make_choropleth

def dash_secteur_pro_ais():
     #######################
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
    # Load data
    #@st.cache_data
    def load_data():
         data_path=data_dir('base_streamlit_storytellers.xlsx')
         return pd.read_excel(data_path,sheet_name="Secteur_prof_ais")

    df_reshaped = load_data()
        #######################
    # Sidebar
    with st.sidebar:
        st.title("🌾 🏭 🛍️ Professions clés de l'économie")
        
        year_list = list(df_reshaped.Annee.unique())[::-1]
        selected_year = st.slider('Choisir une année', int(min(year_list)),int(max(year_list)))
        
        #Pays=list(df_reshaped.Pays.unique())
        selected_pays="Tchad"#st.selectbox('Choisir le pays', Pays)

        
        df_selected_year = df_reshaped[df_reshaped.Annee == selected_year]
        df_selected_pays=df_selected_year[df_selected_year.Pays==selected_pays]
###########
    st.markdown("# Professions clés de l'économie")
    st.markdown('---')
    st.subheader(f"Contribution des trois secteurs clés dans l'économie ({selected_pays}) en {selected_year}")
    col = st.columns((1.5, 1.5, 1.5), gap='medium')
    
    colonnes_secteurs = [
        "Agriculture, valeur ajoutée (% du PIB)",
        "Service, valeur ajoutée (% du PIB)",
        "Industrie, valeur ajoutée (% du PIB)",
    ]
    # Affichage des métriques avec une valeur en rouge
    html_template = """
<div style="background-color: white; padding: 10px; border-radius: 5px; text-align: center;">
    <h3 style="color: black; margin: 0;">{label}</h3>
    <p style="font-size: 24px; font-weight: bold; color: red; margin: 0;">{value}</p>
</div>
"""
    for i in range(3):
        with col[i]:
            var=colonnes_secteurs[i]
            valeur = df_selected_pays[var].iloc[0]
            st.markdown(html_template.format(label=var, value=f"{valeur:.2f}"), unsafe_allow_html=True)
            
            #st.metric(label=var, value=f"{valeur:.2f}")
    st.write("Source: Banque Mondiale, WDI")
    st.markdown('---')
#############################################################################################################
    #secteurr=["Emplois dans l'industrie (% du total des emplois)","Emplois dans l'agriculture (% du total des emplois)","Emplois dans les services (% du total des emplois)"]

    #st.subheader("Repartition continentale de la part d'emploi généré par secteur d'activité")
    #selected_secteur=st.selectbox("")
    #df_reshaped

    st.markdown('---')
    st.subheader(f"Proportion des emplois générés par secteur d'activité ({selected_pays}) en {selected_year}")
################
    def make_donut(input_response, input_text, input_color):
       
        if input_color == 'blue':
            chart_color = ['#29b5e8', '#155F7A']
        elif input_color == 'green':
            chart_color = ['#27AE60', '#12783D']
        elif input_color == 'orange':
            chart_color = ['#F39C12', '#875A12']
        elif input_color == 'red':
            chart_color = ['#E74C3C', '#781F16']
        else:
            # Couleur par défaut si input_color est invalide
            chart_color = ['#D3D3D3', '#A9A9A9']

        source = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100-input_response, input_response]
        })
        source_bg = pd.DataFrame({
            "Topic": ['', input_text],
            "% value": [100, 0]
        })

        plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
            theta="% value",
            color= alt.Color("Topic:N",
                            scale=alt.Scale(
                                #domain=['A', 'B'],
                                domain=[input_text, ''],
                                # range=['#29b5e8', '#155F7A']),  # 31333F
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height=130)

        text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
            theta="% value",
            color= alt.Color("Topic:N",
                            scale=alt.Scale(
                                # domain=['A', 'B'],
                                domain=[input_text, ''],
                                range=chart_color),  # 31333F
                            legend=None),
        ).properties(width=130, height=130)
        return plot_bg + plot + text
    
    gen_emploi=["Emplois dans l'agriculture (% du total des emplois)","Emplois dans les services (% du total des emplois)","Emplois dans l'industrie (% du total des emplois)"]
    col = st.columns((1.5, 1.5, 1.5), gap='medium')
    couleurs=['orange',"red",'green']
    for i in range(3):
        var=gen_emploi[i]
        val=round(df_selected_pays[var].iloc[0],1)
        with col[i]:
            
            if not np.isnan(val):
                color=couleurs[i]
                donut_chart = make_donut(val, var,color )
                st.write(f'{var}')
                st.altair_chart(donut_chart)
            else :
                st.write("Données indisponible")
    st.write("Source: Banque Mondiale, WDI")

    st.markdown('---')    
    st.subheader(f"Proportion des emplois générés par secteur d'activité ({selected_pays}) en {selected_year} en fonction du sexe")
    
    # Histogramme avec Altair
    def hist_comp(data,domaine):
        """
        la forme du data attendu en entrée :

        data = pd.DataFrame({
        "Genre": ["Hommes", "Femmes"],
        "Pourcentage": [30, 25]  # Taux d'emploi en agriculture})
        """
        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X("Genre:N", title="Genre"),
            y=alt.Y("Pourcentage:Q", title="Pourcentage (%)"),
            color=alt.Color("Genre:N", scale=alt.Scale(range=["#1f77b4", "#ff7f0e"]),legend=None),  # Couleurs : bleu et orange
            tooltip=["Genre", "Pourcentage"]
        ).properties(
            width=400,
            height=300,
            title=domaine
        )

        # Affichage dans Streamlit
        st.altair_chart(chart, use_container_width=True)
    ag_emploi=["Employées, agriculture, femmes (% d'emploi des femmes)","Employés, agriculture, hommes (% d'emploi des hommes)"]
    ind_emploi=["Employées, industrie, femmes (% d'emploi des femmes)","Employés, industrie, hommes (% d'emploi des hommes)"]
    serv_emploi=["Employées, services, femmes (% d'emploi des femmes)","Employés, services, hommes (% d'emploi des hommes)"]
    #activities=[ag_emploi,serv_emploi,ind_emploi]
    col_comp= st.columns((1.5, 1.5, 1.5), gap='medium')
    with col_comp [0]:
        valh=round(df_selected_pays["Employés, agriculture, hommes (% d'emploi des hommes)"].iloc[0],1)
        valf=round(df_selected_pays["Employées, agriculture, femmes (% d'emploi des femmes)"].iloc[0],1)
        if np.isnan(valh) or np.isnan(valf):
            st.write("Données indisponibles")
        else :
            data = pd.DataFrame({
            "Genre": ["Hommes", "Femmes"],
            "Pourcentage": [valh, valf] })
            hist_comp(data,"Emploi dans l'agriculture par genre")
    with col_comp [1]:
        valh=round(df_selected_pays[serv_emploi[1]].iloc[0],1)
        valf=round(df_selected_pays[serv_emploi[0]].iloc[0],1)
        if np.isnan(valh) or np.isnan(valf):
            st.write("Données indisponibles")
        else:
            data = pd.DataFrame({
            "Genre": ["Hommes", "Femmes"],
            "Pourcentage": [valh, valf] })
            hist_comp(data,"Emploi dans les services par genre")
    with col_comp [2]:
        valh=round(df_selected_pays[ind_emploi[1]].iloc[0],1)
        valf=round(df_selected_pays[ind_emploi[0]].iloc[0],1)
        if np.isnan(valh) or np.isnan(valf):
            st.write("Données indisponibles")
        else:
            data = pd.DataFrame({
            "Genre": ["Hommes", "Femmes"],
            "Pourcentage": [valh, valf] })
            hist_comp(data,"Emploi dans l'industrie par genre")
    st.write("Source: Banque Mondiale, WDI")

   

        