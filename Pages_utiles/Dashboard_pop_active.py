######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import plotly.express as px
from Datas.data_link import data_dir
from Photos.photo_link import main_dir
#######################
# Page configuration
def dash_pop_active():
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
     #######################
    # Load data
    #@st.cache_data
    def load_data():
         data_path=data_dir('base_streamlit_storytellers.xlsx')
         return pd.read_excel(data_path,sheet_name="Pop_active_Af_pays")

    df_reshaped = load_data()


    #######################
    # Sidebar
    with st.sidebar:
        st.title('🏂 Population active')
        
        #year_list = list(df_reshaped.Annee.unique())[::-1]
        #selected_year = st.selectbox('Choisir une année', year_list)
        selected_year = st.sidebar.slider("Sélectionnez une année :", int(df_reshaped.Annee.min()), int(df_reshaped.Annee.max()), 2020)

        sexe=list(df_reshaped.Sexe.unique())
        selected_sexe=st.selectbox('Choisir le genre', sexe)


        df_selected_year = df_reshaped[df_reshaped.Annee == selected_year]
        df_selected_year_sorted = df_selected_year.sort_values(by="Proportion_de_population_active(%)", ascending=False)
        df_selected_final=df_selected_year_sorted[df_selected_year_sorted.Sexe==selected_sexe]

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('Choisir une mise en forme de la carte', color_theme_list)

    # Choropleth map
    def make_choropleth(input_df, input_id, input_column, input_color_theme):
        choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="country names",
                                color_continuous_scale=input_color_theme,
                                range_color=(0, max(df_selected_year["Proportion_de_population_active(%)"])),
                                scope="africa",
                                labels={'Proportion_de_population_active(%)':'Population active(%)'}
                                )
        choropleth.update_layout(
            template=None,
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        return choropleth



    #######################
    # Dashboard Main Panel
    st.markdown(f"# Aperçu général sur la main d'oeuvre en Afrique et au Tchad")
    st.markdown('---')
    data_path=data_dir('base_streamlit_storytellers.xlsx')
   
   
        ##################################################################""
    col = st.columns((4.5, 2), gap='medium')
   

    with col[0]:
        st.markdown(f'#### Proportion de la population active en {selected_year}')
        
        choropleth = make_choropleth(df_selected_year, 'Pays', 'Proportion_de_population_active(%)', selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)
        

    with col[1]:
        st.markdown(f'#### Classement des pays par population active en {selected_year}')

        st.dataframe(df_selected_final,
                    column_order=("Pays", "Proportion_de_population_active(%)"),
                    hide_index=True,
                    width=None,
                    column_config={
                        "Pays": st.column_config.TextColumn(
                            "Pays",
                        ),
                        "Proportion_de_population_active(%)": st.column_config.ProgressColumn(
                            "Population active (%)",
                            format="%f",
                            min_value=0,
                            max_value=max(df_selected_year_sorted["Proportion_de_population_active(%)"]),
                        )}
                    )
        
    logo_path = main_dir("carte_tchad_afr.jpeg")
    logo = Image.open(logo_path)
    st.markdown('---')
    st.markdown('---')
    colonne = st.columns((1.5, 2), gap='medium')
    st.markdown('---')
    val=df_selected_final[df_selected_final['Pays'] == 'Chad']#["Proportion_de_population_active(%)"]

    
    with colonne[0]:
        st.image(logo,use_column_width=True)
    with colonne[1]:
        st.write(f"Population active du Tchad en {selected_year} est : ")
        st.dataframe(val)






