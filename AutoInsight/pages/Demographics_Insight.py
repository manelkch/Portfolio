import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns(3)

with col2:
    st.image("img/auto.png")
    
st.title("Demographics Insight")
 
st.write("Explore how different demographics influence car sales.")
st.write("Understand which customer segments are more likely to buy certain models and where they are located.")

 
# Fonction pour charger les données
def load_data():
    # Data Preprocessing 
    df = pd.read_excel("Car Sales.xlsx")

    df['Date'] = pd.to_datetime(df['Date'])

    #df = df.drop(['Phone', 'Customer Name', 'Dealer_Name', 'Customer Address', 'Dealer_Add'], axis=1)
    df['Date'] = pd.to_datetime(df['Date'])

    df = df.fillna(df.median(numeric_only=True))
    for column in df.select_dtypes(include=['object', 'category']).columns:
        df[column] = df[column].fillna(df[column].mode()[0])

    df.to_dict(orient="records")

    return df

 
# Calcul du pourcentage des ventes par région
def pourcentage_ventes_par_region(df):
    region_counts = df['Dealer_Region'].value_counts()
    total_sales = region_counts.sum()
    region_percentage = (region_counts / total_sales) * 100
    
    return pd.DataFrame({'Région': region_percentage.index, 'Pourcentage des Ventes': region_percentage.values})
 
# Visualisation du pourcentage des ventes par région
def visualiser_ventes_par_region(df):
    st.subheader("Pourcentage des Ventes par Région")
    
    if 'Dealer_Region' not in df.columns:
        st.error("La colonne 'Dealer_Region' n'existe pas dans les données.")
        return

    region_percentage_df = pourcentage_ventes_par_region(df)

    fig = px.bar(
        region_percentage_df,
        x='Pourcentage des Ventes',
        y='Région',
        orientation='h',
        title="Distribution des Ventes par Région",
        labels={'Pourcentage des Ventes': 'Pourcentage (%)'},
        text='Pourcentage des Ventes'
    )
    fig.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig, use_container_width=True)
 
 
def concessionnaire_leader_par_region(df):
    ventes_par_concessionnaire = df.groupby(['Dealer_Region', 'Dealer_Name']).size().reset_index(name='Nombre_Ventes')
    top_dealers = ventes_par_concessionnaire.loc[ventes_par_concessionnaire.groupby('Dealer_Region')['Nombre_Ventes'].idxmax()]
    
    top_dealers = top_dealers.sort_values(by='Nombre_Ventes', ascending=False).reset_index(drop=True)
    
    return top_dealers
 
 
def afficher_concessionnaire_leader_par_region(df):
    st.subheader("Concessionnaire leader par région")
    top_dealers = concessionnaire_leader_par_region(df)
    st.dataframe(top_dealers)
 
 
 
def types_voitures_par_region(df):
    st.subheader("Types de Marques par Région")

    regions = df['Dealer_Region'].unique()
    selected_regions = st.multiselect("Sélectionnez les régions :", options=regions, default=regions.tolist())

    companies = df['Company'].unique()
    cols = st.columns(3)
    selected_companies = []

    for i, company in enumerate(companies):
        col_index = i % 3
        with cols[col_index]:
            if st.checkbox(company, value=True):
                selected_companies.append(company)

    if selected_regions and selected_companies:
        df_filtered = df[(df['Dealer_Region'].isin(selected_regions)) & (df['Company'].isin(selected_companies))]
        if not df_filtered.empty:
            grouped = df_filtered.groupby(['Dealer_Region', 'Company']).size().reset_index(name='Ventes')

            fig = px.bar(
                grouped,
                x='Dealer_Region',
                y='Ventes',
                color='Company',
                title="Distribution des Marques de Voitures par Région",
                barmode='stack',
                text='Ventes'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Aucune donnée ne correspond à votre sélection.")
    else:
        st.warning("Veuillez sélectionner au moins une région et une marque.")
 
def performances_par_concessionnaire(df):
    st.subheader("Performances par Concessionnaire")

    if 'Dealer_Name' in df.columns and 'Price in thousands' in df.columns:
        performances = df.groupby('Dealer_Name').agg(
            total_sales=('Dealer_Name', 'count'),
            total_revenue=('Price in thousands', 'sum')
        ).reset_index()

        performances = performances.sort_values(by='total_sales', ascending=False)
        selected_dealers = st.multiselect("Sélectionnez des concessionnaires :", performances['Dealer_Name'], default=performances['Dealer_Name'].tolist()[:3])

        if selected_dealers:
            filtered = performances[performances['Dealer_Name'].isin(selected_dealers)]

            fig = px.bar(
                filtered.melt(id_vars='Dealer_Name', value_vars=['total_sales', 'total_revenue']),
                x='Dealer_Name',
                y='value',
                color='variable',
                barmode='group',
                text='value',
                title="Performances des Concessionnaires (Ventes & Revenus)",
                labels={"value": "Valeur", "variable": "Indicateur"}
            )
            st.plotly_chart(fig, use_container_width=True)
            st.write("### Détails des Performances")
            st.dataframe(filtered)
        else:
            st.warning("Veuillez sélectionner au moins un concessionnaire.")
    else:
        st.warning("Colonnes 'Dealer_Name' ou 'Price in thousands' manquantes.")
 
 
def main():
    st.info("Chargement des données...")
    df = load_data()  # Charger les données depuis l'API
    
    if df is not None:
        st.success("Données chargées avec succès.")
        visualiser_ventes_par_region(df)  # Afficher le graphique des ventes par région
        afficher_concessionnaire_leader_par_region(df)  
        types_voitures_par_region(df)
        performances_par_concessionnaire(df)
    else:
        st.error("Impossible de charger les données.")
 
 
main()