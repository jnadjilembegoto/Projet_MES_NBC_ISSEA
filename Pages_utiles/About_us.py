import streamlit as st
from PIL import Image
from Photos.photo_link import main_dir




def about_us_page():
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
    st.title("À propos de nous")
    st.write("""
    L'équipe est constitué de deux élèves ingénieurs statisticiens économistes en formation à l'ISSEA en spécialité Finance et actuariat.
             
    """)
    
    st.markdown('---')

    nadji = Image.open(main_dir("nadji.jpg"))
    nadji = nadji.resize((200,300))
    st.markdown(
        f"""
        ##### NADJILEM BEGOTO
        """,
        unsafe_allow_html=True,
    )
    col_im,col_ad=st.columns(2)
    with col_im:
        st.image(nadji,use_column_width=False)
    with col_ad:
        st.markdown(
        f"""
        - 📧 Email:  <jnadjilembegoto@gmail.com> ou <student.begoto.nadjilem@issea-cemac.org>
        - Linkedin:  https://www.linkedin.com/in/bégoto-nadjilem-192b8617b
        """,
        unsafe_allow_html=True,
    )
    st.markdown('---')
     

    nc = Image.open(main_dir("nc.jpeg"))
    nc = nc.resize((200,300))
    st.markdown(
        f"""
        ##### NGUEKORAL Chanceline
        """,
        unsafe_allow_html=True,
    )
    col_im,col_ad=st.columns(2)
    with col_im:
        st.image(nc,use_column_width=False)
    with col_ad:
        st.markdown(
        f"""
        - 📧 Email:  <nguekoralc@gmail.com>
        """,
        unsafe_allow_html=True,
    )
    
    
    st.markdown('---')

    
