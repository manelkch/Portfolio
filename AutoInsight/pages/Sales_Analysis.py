import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px
 
st.set_page_config(layout="wide")

col1, col2, col3 = st.columns(3)

with col2:
    st.image("img/auto.png")
 
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

 
# Configurer la barre latérale
st.sidebar.title("Options")
st.sidebar.write("Utilisez les filtres ci-dessous pour ajuster les visualisations.")
 
# Chargement des données
data = load_data()
 
# Vérification si les données sont disponibles
if data is not None:
    # Option pour afficher la table
    show_table = st.sidebar.checkbox("Afficher la table de données")
    if show_table:
        st.write("### Données des ventes :")
        st.dataframe(data)
    
    # Filtrer les données par année
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['Year'] = data['Date'].dt.year
    years = st.sidebar.multiselect("Sélectionner l'année", options=data['Year'].unique(), default=data['Year'].unique())
    filtered_data = data[data['Year'].isin(years)]

    # Titre principal
    st.title("Tableau de bord des ventes de voitures")
    
    # Sélection du graphique à afficher
    graph_choice = st.selectbox("Choisir une visualisation", ["Ventes par région", "Ventes par catégorie", "Ventes par année", "Ventes par marque"])

    
    # Graphiques selon la sélection de l'utilisateur
    if graph_choice == "Ventes par région":
        st.subheader("Ventes par Région")
        fig = px.histogram(filtered_data, x="Dealer_Region", color="Dealer_Region", title="Distribution des Ventes par Région")
        st.plotly_chart(fig)
 
    elif graph_choice == "Ventes par catégorie":
        st.subheader("Ventes par Catégorie de Modèle")
        
        # Regrouper les modèles en catégories
        model_categories = {
            'SUV': ['Expedition', 'Durango', 'Mountaineer', 'Navigator', 'Grand Cherokee'],
            'Berline': ['Corolla', 'Accord', 'Camry', 'Jetta', 'Altima'],
            'Coupé / Sport': ['Corvette', 'Mustang', 'Camaro'],
            'Monospace / Familial': ['Odyssey', 'Sienna', 'Town & Country'],
            'Pick-up': ['Ram Pickup', 'F-Series', 'Tacoma'],
            'Berline de luxe': ['A8', 'S-Type', 'GS300'],
            'Compacte': ['Civic', 'Focus', 'Mazda3'],
            'Crossover': ['NX', 'QX50', 'CR-V'],
            'Roadster': ['Boxster', 'MX-5 Miata'],
            'Véhicule Utilitaire': ['Transit', 'Sprinter'],
        }
 
        filtered_data['Category'] = filtered_data['Model'].apply(
            lambda x: next((cat for cat, models in model_categories.items() if x in models), 'Autre')
        )
 
        fig = px.histogram(filtered_data, x="Category", color="Category", title="Ventes par Catégorie de Modèle")
        st.plotly_chart(fig)
 
    elif graph_choice == "Ventes par année":
        st.subheader("Ventes par Année")
        sales_per_year = filtered_data.groupby('Year').size().reset_index(name='Ventes')
        fig = px.bar(sales_per_year, x='Year', y='Ventes', title="Nombre de Ventes par Année")
        st.plotly_chart(fig)
 
    elif graph_choice == "Ventes par marque":
        st.subheader("Ventes par Marque")
        sales_per_company = filtered_data.groupby('Company').size().reset_index(name='Ventes')
        fig = px.bar(sales_per_company, x='Company', y='Ventes', color='Company', title="Ventes par Marque")
        st.plotly_chart(fig)
    
else:
    st.error("Aucune donnée disponible.")
 
 
 
 
 
 
st.title("Sales Analysis")
st.write("Dive into the details of car sales across different regions, models, and time periods.")
st.write("Understand which models are top-sellers and how sales fluctuate throughout the year.")
 
def vente_par_region(df):
    st.subheader("Statistiques de Vente par Région")
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Dealer_Region')
    plt.title("Distribution des Ventes par Région")
    plt.xlabel("Région")
    plt.ylabel("Nombre de Ventes")
    st.pyplot(plt)
 
# Regroupement des modèles en catégories
model_categories = {
    'SUV': [
        'Expedition', 'Durango', 'Mountaineer', 'Navigator', 'Grand Cherokee',
        'Pathfinder', '4Runner', 'CR-V', 'RAV4', 'Xterra', 'Explorer', 'M-Class',
        'Montero Sport', 'Forester', 'Outback', 'TrailBlazer'
    ],
    'Berline': [
        'Corolla', 'Accord', 'Camry', 'Jetta', 'Altima', 'Taurus', 'Malibu',
        'Civic', 'Impala', 'Century', 'Legacy', 'Eldorado', 'TL', 'Diamante',
        'Park Avenue', 'Maxima', 'Grand Am', 'Seville', 'Aurora', 'C-Class',
        'E-Class', 'S40', 'S70', 'Sable', 'Mystique', 'Neon', 'LeSabre', 'Sentra', 'Accent'
    ],
    'Coupé / Sport': [
        'Corvette', 'Mustang', 'Camaro', 'Eclipse', 'Carrera Coupe', 'Viper',
        'SL-Class', 'S-Class', '300M', 'Integra', 'Boxter', 'Firebird', 'Celica', 'Bravada',
        'SC', 'Z4'
    ],
    'Monospace / Familial': [
        'Odyssey', 'Sienna', 'Town & Country', 'Windstar', 'Quest', 'Villager', 'Caravan'
    ],
    'Pick-up': [
        'Ram Pickup', 'F-Series', 'Tacoma', 'Ranger', 'Ram Van'
    ],
    'Berline de luxe': [
        'A8', 'S-Type', 'GS300', 'ES300', 'RL', 'CL500'
    ],
    'Compacte': [
        'Civic', 'Focus', 'Mazda3', 'Golf', 'Elantra', 'Sentra', '3 Series', 'A3'
    ],
    'Crossover': [
        'NX', 'QX50', 'CR-V', 'RAV4', 'CX-5', 'Kona', 'Tiguan'
    ],
    'Roadster': [
        'Boxster', 'MX-5 Miata', 'Z4', 'SLK', 'S2000'
    ],
    'Véhicule Utilitaire': [
        'Transit', 'Sprinter', 'ProMaster', 'Express'
    ],
    # Ajoutez d'autres catégories si nécessaire
}
 
def vente_par_modele(df):
    st.subheader("Statistiques de Vente par Modèle de Voiture")
    # Création d'une nouvelle colonne pour la catégorie
    df['Category'] = df['Model'].apply(
        lambda x: next(
            (cat for cat, models in model_categories.items() if x in models),
            None  # Ne pas ajouter de catégorie si le modèle n'est pas trouvé
        )
    )
    # Filtrer les données pour ne garder que les lignes avec des catégories non nulles
    df_filtered = df[df['Category'].notna()]
 
    # Création d'une figure pour le graphique
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df_filtered, x='Category', order=df_filtered['Category'].value_counts().index)
    plt.title("Distribution des Ventes par Catégorie de Voiture")
    plt.xlabel("Catégorie de Voiture")
    plt.ylabel("Nombre de Ventes")
    plt.xticks(rotation=45)
    st.pyplot(plt)
 
 
def vente_par_periode(df):
    st.subheader("Statistiques de Vente par Période")
    df['Date'] = pd.to_datetime(df['Date'])  # Assurez-vous que la colonne Date est en format datetime
    df['Year'] = df['Date'].dt.year  # Ajout d'une colonne d'année
 
    plt.figure(figsize=(10, 6))
    sales_per_year = df.groupby('Year').size()
    sales_per_year.plot(kind='bar')
    plt.title("Nombre de Ventes par Année")
    plt.xlabel("Année")
    plt.ylabel("Nombre de Ventes")
    st.pyplot(plt)
 
 
def ventes_par_marque(df):
    st.subheader("Analyse des Ventes par Marque de Voiture")
 
    # Regrouper les ventes par marque et calculer le nombre de ventes pour chaque marque
    sales_per_company = df.groupby('Company').size().reset_index(name='Ventes')
 
    # Création d'un graphique à barres des ventes par marque
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Company', y='Ventes', data=sales_per_company,
                order=sales_per_company.sort_values('Ventes', ascending=False)['Company'])
 
    plt.title("Ventes par Marque de Voiture")
    plt.xlabel("Marque de Voiture")
    plt.ylabel("Nombre de Ventes")
    plt.xticks(rotation=45)
 
    # Affichage du graphique dans Streamlit
    st.pyplot(plt)
 
 
def ventes_par_region_et_marque(df):
    st.subheader("Ventes par Région et Marque")
 
    # Obtenir les valeurs uniques des régions et des marques
    regions = df['Dealer_Region'].unique().tolist()
    marques = df['Company'].unique().tolist()
 
    # Ajouter l'option "Tout" pour afficher toutes les régions ou marques
    regions.insert(0, "Tout")
    marques.insert(0, "Tout")
 
    # Widgets Streamlit pour choisir la région et la marque
    region_selection = st.selectbox("Choisir une région", regions)
    marque_selection = st.selectbox("Choisir une marque", marques)
 
    # Filtrer les données en fonction de la région et de la marque sélectionnées
    filtered_data = df.copy()
 
    if region_selection != "Tout":
        filtered_data = filtered_data[filtered_data['Dealer_Region'] == region_selection]
 
    if marque_selection != "Tout":
        filtered_data = filtered_data[filtered_data['Company'] == marque_selection]
 
    # Vérifier s'il y a des données après filtrage
    if not filtered_data.empty:
        # Compter les ventes par modèle dans la région et pour la marque choisie
        sales_per_model = filtered_data.groupby(['Model', 'Company']).size().reset_index(name='Sales Count')
 
        # Créer un graphique à barres pour les ventes par modèle et par marque
        plt.figure(figsize=(12, 8))
        sns.barplot(
            data=sales_per_model,
            x='Model',
            y='Sales Count',
            hue='Company',  # Utilisation de la marque comme hue pour différencier les couleurs
            dodge=False,    # Empêche la séparation des barres pour chaque modèle
            palette='Set2'  # Palette de couleurs pour plus de lisibilité
        )
 
        # Personnaliser le graphique
        if region_selection == "Tout" and marque_selection == "Tout":
            plt.title("Ventes par Modèle dans toutes les Régions et Marques")
        elif region_selection == "Tout":
            plt.title(f'Ventes par Modèle pour la Marque {marque_selection}')
        elif marque_selection == "Tout":
            plt.title(f'Ventes par Modèle dans la Région {region_selection}')
        else:
            plt.title(f'Ventes par Modèle dans {region_selection} pour la Marque {marque_selection}')
 
        plt.xticks(rotation=45)
        plt.xlabel("Modèle")
        plt.ylabel("Nombre de Ventes")
        plt.legend(title='Marque')  # Légende pour les marques
        plt.tight_layout()
 
        # Afficher le graphique dans Streamlit
        st.pyplot(plt)
    else:
        st.warning(f"Aucune vente trouvée pour la région {region_selection} et la marque {marque_selection}")
 
 
def analyse_profil_achats(df):
    """
    Fonction pour analyser quel profil de client achète quel modèle de voiture
    en fonction du revenu annuel et du sexe.
    """
    st.subheader("Analyse des Achats par Profil de Client")
 
    # Sélectionner les options de profil à analyser
    profiles = ['Gender', 'Annual Income']
    selected_profile = st.selectbox("Choisir le profil à analyser", profiles)
 
    # Créer un tableau croisé dynamique selon le profil choisi
    if selected_profile == 'Gender':
        profile_data = df.groupby(['Gender', 'Model']).size().reset_index(name='Count')
    elif selected_profile == 'Annual Income':
        profile_data = df.groupby(['Annual Income', 'Model']).size().reset_index(name='Count')
 
    # Afficher les résultats
    if not profile_data.empty:
        st.write(profile_data)
 
        # Visualiser les résultats avec un graphique
        fig = px.bar(profile_data,
                     x=selected_profile,
                     y='Count',
                     color='Model',
                     title=f"Achats par Modèle selon le Profil de {selected_profile}",
                     labels={selected_profile: selected_profile, 'Count': 'Nombre d\'Achats'},
                     height=600)
 
        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig)
    else:
        st.warning("Aucune donnée trouvée pour l'analyse choisie.")
 
 
def heatmap_ventes_region_sexe(df):
    st.subheader("Heatmap des Ventes par Région et Sexe")
 
    # Compter les ventes par région et sexe
    sales_heatmap = df.groupby(['Dealer_Region', 'Gender']).size().unstack(fill_value=0)
 
    # Créer une heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(sales_heatmap, annot=True, fmt='g', cmap='Blues')
    
    plt.title("Heatmap des Ventes par Région et Sexe")
    plt.xlabel("Sexe")
    plt.ylabel("Région")
    plt.tight_layout()
 
    # Afficher le graphique dans Streamlit
    st.pyplot(plt)
 
def camembert_ventes_sexe(df):
    """
    Fonction pour afficher un camembert des ventes par sexe.
    """
    st.subheader("Camembert des Ventes par Sexe")
 
    # Compter les ventes par sexe
    sales_by_sexe = df['Gender'].value_counts()
 
    # Créer le camembert
    plt.figure(figsize=(8, 8))
    plt.pie(
        sales_by_sexe,
        labels=sales_by_sexe.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette('pastel')
    )
    
    plt.title("Répartition des Ventes par Sexe")
    plt.axis('equal')  # Pour que le camembert soit circulaire
 
    # Afficher le graphique dans Streamlit
    st.pyplot(plt)
 
def camembert_ventes_par_sexe(df):
    """
    Fonction pour afficher un camembert des ventes par sexe en fonction du modèle et de la marque choisis.
    """
    st.subheader("Comparaison des Ventes par Sexe")
 
    # Obtenir les valeurs uniques des marques
    marques = df['Company'].unique().tolist()
    marques.insert(0, "Tout")  # Ajouter l'option "Tout" pour inclure toutes les marques
 
    # Widget Streamlit pour choisir la marque
    marque_selection = st.selectbox("Choisir une marque", marques, key="marque_pie_chart")
 
    # Filtrer les modèles en fonction de la marque sélectionnée
    if marque_selection == "Tout":
        modeles = df['Model'].unique().tolist()  # Tous les modèles si "Tout" est sélectionné
    else:
        modeles = df[df['Company'] == marque_selection]['Model'].unique().tolist()  # Modèles de la marque choisie
 
    modeles.insert(0, "Tout")  # Ajouter l'option "Tout" pour inclure tous les modèles
 
    # Widget Streamlit pour choisir le modèle (basé sur la marque sélectionnée)
    modele_selection = st.selectbox("Choisir un modèle", modeles, key="modele_pie_chart")
 
    # Filtrer les données en fonction de la marque et du modèle sélectionnés
    filtered_data = df.copy()
 
    if marque_selection != "Tout":
        filtered_data = filtered_data[filtered_data['Company'] == marque_selection]
 
    if modele_selection != "Tout":
        filtered_data = filtered_data[filtered_data['Model'] == modele_selection]
 
    # Vérifier s'il y a des données après filtrage
    if not filtered_data.empty:
        # Compter les ventes par sexe
        ventes_par_sexe = filtered_data['Gender'].value_counts()
 
        # Créer un camembert
        plt.figure(figsize=(6, 6))
        plt.pie(
            ventes_par_sexe,
            labels=ventes_par_sexe.index,
            autopct='%1.1f%%',
            colors=['#ff9999','#66b3ff'],
            startangle=90
        )
 
        # Ajouter un titre au camembert
        if marque_selection == "Tout" and modele_selection == "Tout":
            plt.title("Répartition des Ventes par Sexe pour toutes les Marques et Modèles")
        elif marque_selection == "Tout":
            plt.title(f"Répartition des Ventes par Sexe pour le Modèle {modele_selection}")
        elif modele_selection == "Tout":
            plt.title(f"Répartition des Ventes par Sexe pour la Marque {marque_selection}")
        else:
            plt.title(f"Répartition des Ventes par Sexe pour {marque_selection} {modele_selection}")
 
        # Afficher le camembert dans Streamlit
        st.pyplot(plt)
    else:
        st.warning(f"Aucune vente trouvée pour la marque {marque_selection} et le modèle {modele_selection}")
 
def analyse_ventes_par_revenu(df):
    st.subheader("Analyse des Ventes par Revenu et Gamme de Prix")
 
    # Ajouter des colonnes pour les gammes de voitures
    df['Gamme'] = pd.cut(df['Price in thousands'],
                         bins=[0, 20, 35, float('inf')],
                         labels=['Bas de gamme', 'Moyenne gamme', 'Haut de gamme'])
 
    # Segmenter les clients par revenu
    df['Revenu_Categorie'] = pd.cut(df['Annual Income'],
                                    bins=[0, 30000, 70000, float('inf')],
                                    labels=['Faible revenu', 'Revenu moyen', 'Revenu élevé'])
 
    # Filtre pour choisir la gamme de voiture
    gamme_selection = st.selectbox("Choisir une gamme de voitures", ['Toutes', 'Bas de gamme', 'Moyenne gamme', 'Haut de gamme'])
 
    # Filtrer les données en fonction de la gamme de voitures choisie
    if gamme_selection != 'Toutes':
        df = df[df['Gamme'] == gamme_selection]
 
    # Compter les ventes par catégorie de revenu et par gamme de voitures
    ventes_par_revenu = df.groupby(['Revenu_Categorie', 'Gamme']).size().reset_index(name='Nombre de Ventes')
 
    # Créer un graphique à barres empilées pour comparer les ventes par revenu et gamme de voitures
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=ventes_par_revenu,
        x='Revenu_Categorie',
        y='Nombre de Ventes',
        hue='Gamme',
        palette='Set2'
    )
 
    # Personnaliser le graphique
    plt.title('Nombre de Ventes par Revenu et Gamme de Voitures')
    plt.xlabel("Catégorie de Revenu")
    plt.ylabel("Nombre de Ventes")
    plt.legend(title='Gamme de Voiture')
    plt.xticks(rotation=45)
    plt.tight_layout()
 
    # Afficher le graphique dans Streamlit
    st.pyplot(plt)
 
 
def analyse_ventes_par_revenu_marque_modele(df):
    st.subheader("Analyse des Ventes par Revenu, Marque et Modèle")
 
    # Choix de la marque
    marques = df['Company'].unique()
    marque_selectionnee = st.selectbox("Sélectionnez une Marque :", marques)
 
    # Filtrer le DataFrame en fonction de la marque sélectionnée
    df_marque = df[df['Company'] == marque_selectionnee]
 
    # Choix du modèle basé sur la marque sélectionnée
    modeles = df_marque['Model'].unique()
    modele_selectionne = st.selectbox("Sélectionnez un Modèle :", modeles)
 
    # Filtrer le DataFrame en fonction du modèle sélectionné
    df_modele = df_marque[df_marque['Model'] == modele_selectionne]
 
    # Afficher les moyennes du revenu et prix
    moyenne_revenu = df_modele['Annual Income'].mean()
    moyenne_prix = df_modele['Price in thousands'].mean()
 
    st.write(f"**Moyenne du Revenu Annuel pour {marque_selectionnee} - {modele_selectionne}** : {moyenne_revenu:,.2f} €")
    st.write(f"**Moyenne du Prix des Voitures (en milliers) pour {marque_selectionnee} - {modele_selectionne}** : {moyenne_prix:,.2f} K€")
 
    # Segmentation du Revenu Annuel
    conditions_revenu = [
        (df_modele['Annual Income'] < 100000),
        (df_modele['Annual Income'] >= 100000) & (df_modele['Annual Income'] <= 500000),
        (df_modele['Annual Income'] > 500000) & (df_modele['Annual Income'] <= 1000000),
        (df_modele['Annual Income'] > 1000000)
    ]
    labels_revenu = ['Faible revenu', 'Revenu moyen', 'Revenu élevé', 'Très haut revenu']
    df_modele['Segment Revenu'] = pd.cut(df_modele['Annual Income'], bins=[0, 100000, 500000, 1000000, float('inf')], labels=labels_revenu)
 
    # Afficher les résultats par segment de revenu
    ventes_par_segment = df_modele.groupby('Segment Revenu')['Annual Income'].count()
 
    st.write("### Nombre de ventes par Segment de Revenu :")
    st.bar_chart(ventes_par_segment)
 
def afficher_moyennes_et_segmentations(df):
    st.subheader("Calcul des Moyennes et Segmentations")
 
    # Calcul des moyennes
    moyenne_revenu = df['Annual Income'].mean()
    moyenne_prix = df['Price in thousands'].mean()
 
    # Afficher les résultats
    st.write(f"**Moyenne du Revenu Annuel des Clients** : {moyenne_revenu:,.2f} €")
    st.write(f"**Moyenne du Prix des Voitures (en milliers)** : {moyenne_prix:,.2f} K€")
 
    # Segmentation du Revenu Annuel
    conditions_revenu = [
        (df['Annual Income'] < 100000),
        (df['Annual Income'] >= 100000) & (df['Annual Income'] <= 500000),
        (df['Annual Income'] > 500000) & (df['Annual Income'] <= 1000000),
        (df['Annual Income'] > 1000000)
    ]
    labels_revenu = ['Faible revenu', 'Revenu moyen', 'Revenu élevé', 'Très haut revenu']
    df['Segment Revenu'] = pd.cut(df['Annual Income'], bins=[0, 100000, 500000, 1000000, float('inf')], labels=labels_revenu)
 
    # Segmentation du Prix des Voitures
    conditions_prix = [
        (df['Price in thousands'] < 20),
        (df['Price in thousands'] >= 20) & (df['Price in thousands'] <= 40),
        (df['Price in thousands'] > 40)
    ]
    labels_prix = ['Entrée de gamme', 'Moyenne gamme', 'Haut de gamme']
    df['Segment Prix'] = pd.cut(df['Price in thousands'], bins=[0, 20, 40, float('inf')], labels=labels_prix)
 
    # Afficher les segments
    st.write("### Segmentation des Revenus :")
    st.write(df.groupby('Segment Revenu')['Annual Income'].mean())
    st.write("### Segmentation des Prix :")
    st.write(df.groupby('Segment Prix')['Price in thousands'].mean())
 
 
 
 
def main():
    st.title("Analyse des Ventes de Voitures")
 
    # Navigation entre les pages
    page = st.sidebar.selectbox("Choisissez une page:", ["Accueil", "Analyse des Ventes", "Profil client"])
 
    # Chargez les données
    df = load_data()
 
    if page == "Accueil":
        if df is not None:
            st.write("Car Sales Data")
            st.dataframe(df)
 
            # Afficher les statistiques descriptives
            st.subheader("Statistiques Descriptives")
            stats = df.describe()
            st.write(stats)
 
    elif page == "Analyse des Ventes":
        if df is not None:
            #vente_par_region(df)
            vente_par_modele(df)
            vente_par_periode(df)
            ventes_par_marque(df)
            ventes_par_region_et_marque(df)
 
    elif page == "Profil client":
        if df is not None:
            analyse_profil_achats(df)
            heatmap_ventes_region_sexe(df)
            camembert_ventes_sexe(df)
            camembert_ventes_par_sexe(df)
            analyse_ventes_par_revenu_marque_modele(df)
 
main()