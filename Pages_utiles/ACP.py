import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from factor_analyzer import calculate_kmo
import streamlit as st
from Datas.data_link import data_dir

def acp_analyse():
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
    # Charger les données
    path = data_dir('base_streamlit_storytellers.xlsx')
    data = pd.read_excel(path, sheet_name='ACP_OK')

    # Configuration Streamlit


    st.title("Analyse en Composantes Principales (ACP)")
    st.write("un coup d'oeil sur les variables utilisées")
    with st.expander('About', expanded=False):

        st.markdown("share_yth_not_in_EET : Share of youth not in education, employment or training, total (% of youth population) (modeled ILO estimate)")
        st.markdown("female_labor_rate_particip: Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)")
        st.markdown("unempl_tot_pct : Unemployment, total (% of total labor force) (modeled ILO estimate)")
        st.markdown("labor_part_1524_fem : Labor force participation rate for ages 15-24, female (%) (modeled ILO estimate)")
        st.markdown("labor_part_1524_tot : Labor force participation rate for ages 15-24, total (%) (modeled ILO estimate)")
        st.markdown("labor_part_15+_tot : Labor force participation rate, total (% of total population ages 15+) (modeled ILO estimate)")
        st.markdown("labor_part_fem : Labor force, female (% of total labor force)")
        st.markdown("labor_part_tot : Labor force, total")
        st.markdown("unempl_yth_fem_1524 : Unemployment, youth female (% of female labor force ages 15-24) (modeled ILO estimate)")
        st.markdown("unempl_yth_tot : Unemployment, youth total (% of total labor force ages 15-24) (modeled ILO estimate)")
    st.sidebar.header("Configuration")
    fixed_year = st.sidebar.selectbox(
        "Sélectionnez l'année pour l'analyse :", 
        data["year"].unique()
    )

    # Préparer les données pour l'ACP
    data_acp = data[data['year'] == fixed_year]
    data_acp = data_acp.set_index('country').drop('year', axis=1)
    columns_for_pca = data_acp.columns.tolist()

    # Afficher un aperçu des données
    st.write("### Aperçu des données")
    st.write(data_acp.head())

    # Matrice de corrélation
    st.write("### Matrice de corrélation")
    corr_matrix = data_acp.corr(method='pearson')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True, cbar=True, ax=ax)
    st.pyplot(fig)

    # Standardisation des données
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_acp)

    # Calcul de l'indice KMO
    _, kmo_value = calculate_kmo(data_acp)
    st.write("### Indice KMO")
    st.write(f"KMO : {kmo_value:.2f}")
    if kmo_value >= 0.6:
        st.success("L'ACP est adéquate. On peut procéder.")
    else:
        st.warning("L'ACP peut ne pas être adéquate. Considérez d'autres options.")

    # Réalisation de l'ACP
    pca = PCA()
    principal_components = pca.fit_transform(scaled_data)
    explained_variance = pca.explained_variance_ratio_ * 100

    # Graphique des valeurs propres
    st.write("### Courbe des valeurs propres")
    eigenvalues = pca.explained_variance_
    fig_eigen = go.Figure()
    fig_eigen.add_trace(go.Scatter(
        x=np.arange(1, len(eigenvalues) + 1),
        y=eigenvalues,
        mode='lines+markers',
        name="Valeurs propres",
        line=dict(color='blue'),
        marker=dict(size=8)
    ))
    fig_eigen.add_trace(go.Scatter(
        x=np.arange(1, len(eigenvalues) + 1),
        y=[1] * len(eigenvalues),
        mode='lines',
        name="Seuil Kaiser (1.0)",
        line=dict(color='red', dash='dash')
    ))
    fig_eigen.update_layout(
        title="Courbe des valeurs propres (critère de Kaiser)",
        xaxis_title="Composantes principales",
        yaxis_title="Valeurs propres",
        template="plotly_white"
    )
    st.plotly_chart(fig_eigen)

    # Variance expliquée par les deux premières composantes principales
    st.write("### Variance expliquée par le premier plan factoriel")
    st.write(f"La variance totale expliquée par le premier plan factoriel est de {explained_variance[:2].sum():.2f}%.")

    # Contributions des variables
    components = pca.components_[:2] ** 2
    contributions = components / components.sum(axis=1, keepdims=True)
    contribution_df = pd.DataFrame(contributions.T, index=data_acp.columns, columns=['PC1', 'PC2'])
    contributions_PC1_sorted = contribution_df['PC1'].sort_values(ascending=True)
    contributions_PC2_sorted = contribution_df['PC2'].sort_values(ascending=True)

    # Contributions pour PC1
    st.write("### Contributions des variables à la première composante principale (PC1)")
    fig_PC1 = px.bar(
        contribution_df,
        y=contributions_PC1_sorted.index,
        x=contributions_PC1_sorted.values,
        orientation='h',
        title="Contributions à PC1",
        labels={"PC1": "Contribution", "index": "Variables"},
        template="plotly_white"
    )
    fig_PC1.update_layout(
    title="Contributions des variables à la première composante principale (PC1)",
    yaxis_title="Variables",
    xaxis_title="Contribution",
    template="plotly_white"
    )
    st.plotly_chart(fig_PC1)

    # Contributions pour PC2
    st.write("### Contributions des variables à la seconde composante principale (PC2)")
    fig_PC2 = px.bar(
        contribution_df,
        y=contributions_PC2_sorted.index,
        x=contributions_PC2_sorted.values,
        orientation='h',
        title="Contributions à PC2",
        labels={"PC2": "Contribution", "index": "Variables"},
        template="plotly_white"
    )
    fig_PC2.update_layout(
    title="Contributions des variables à la seconde composante principale (PC2)",
    yaxis_title="Variables",
    xaxis_title="Contribution",
    template="plotly_white"
    )
    st.plotly_chart(fig_PC2)

    # Cercle des corrélations
    st.write("### Cercle des corrélations")
    loadings = pca.components_[:2].T * np.sqrt(pca.explained_variance_[:2])
    loading_df = pd.DataFrame(loadings, columns=["PC1", "PC2"], index=data_acp.columns)

    fig_corr = go.Figure()
    for var in loading_df.index:
        fig_corr.add_trace(
            go.Scatter(
                x=[0, loading_df.loc[var, "PC1"]],
                y=[0, loading_df.loc[var, "PC2"]],
                mode='lines+markers+text',
                text=[None, var],
                name=var
            )
        )
    fig_corr.update_layout(
        title=f"Cercle des corrélations (Variance expliquée : {explained_variance[0]:.2f}% + {explained_variance[1]:.2f}%)",
        xaxis_title=f"PC1 ({explained_variance[0]:.2f}%)",
        yaxis_title=f"PC2 ({explained_variance[1]:.2f}%)",
        template="plotly_white"
    )
    st.plotly_chart(fig_corr)

    # Projection des pays
    st.write("### Projection des pays sur le plan factoriel")
    pca_df = pd.DataFrame(principal_components, columns=[f"PC{i+1}" for i in range(principal_components.shape[1])])
    pca_df["country"] = data_acp.index
    fig_scatter = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        text="country",
        title=f"Projection des pays (Variance expliquée : {explained_variance[:2].sum():.2f}%)",
        labels={"PC1": f"PC1 ({explained_variance[0]:.2f}%)", "PC2": f"PC2 ({explained_variance[1]:.2f}%)"},
        template="plotly"
    )
    fig_scatter.update_traces(textposition="top center")
    st.plotly_chart(fig_scatter)
