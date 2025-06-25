import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


#### DATA ANALYSIS ####

# Function to get the distribution of the evaluations for a selected feature
def eval_per_feature(df):
    feature = st.selectbox("Select a feature : ", ['reg_name', 'dep_name', 'com_name', 'filtre', 'APP_Libelle_activite_etablissement'])
    df_grouped = df.groupby(['Synthese_eval_sanit', feature]).size().reset_index(name='Evaluation')

    fig = px.bar(
        df_grouped,
        x=feature,         
        y='Evaluation',           
        color='Synthese_eval_sanit', 
        title=f'Summary of health evaluations by {feature}',
        labels={'reg_name': feature, 'Evaluation': 'Number of evaluations'}
    )

    st.plotly_chart(fig)


# Function to get a donut chart of the distribution of the evaluations of a given region
def eval_per_region(df):
    reg = st.selectbox("Select a region :", df['reg_name'].unique())
    filtered_df = df[df['reg_name'] == reg]
    
    evaluations_count = filtered_df['Synthese_eval_sanit'].value_counts().reindex(
        ['Très satisfaisant', 'Satisfaisant', 'A améliorer', 'A corriger de manière urgente'], 
        fill_value=0
    )
    #st.write("Corresponding results : ")
    #st.write(evaluations_count)
    
    # Donut Chart
    fig = go.Figure(data=[go.Pie(
        labels=evaluations_count.index, 
        values=evaluations_count.values, 
        hole=.5,  
        marker=dict(colors=['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']),
        hoverinfo='label+percent+value'
    )])
    
    fig.update_layout(title=f"Sanitary assessments for the region {reg} - Donut Chart")
    st.plotly_chart(fig)


# Function to get a donut chart of the distribution of the evaluations of a given department
def eval_per_dep(df):
    dep = st.selectbox("Select a department :", df['dep_name'].unique())
    filtered_df = df[df['dep_name'] == dep]
    
    evaluations_count = filtered_df['Synthese_eval_sanit'].value_counts().reindex(
        ['Très satisfaisant', 'Satisfaisant', 'A améliorer', 'A corriger de manière urgente'], 
        fill_value=0
    )
    #st.write("Corresponding results : ")
    #st.write(evaluations_count)
    
    # Donut Chart
    fig = go.Figure(data=[go.Pie(
        labels=evaluations_count.index, 
        values=evaluations_count.values, 
        hole=.5,  
        marker=dict(colors=['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']),
        hoverinfo='label+percent+value'
    )])
    
    fig.update_layout(title=f"Sanitary assessments for the department {dep} - Donut Chart")
    st.plotly_chart(fig)


# Function to get a donut chart of the distribution of the evaluations of a given city
def eval_per_com(df):
    com = st.selectbox("Select a city :", df['com_name'].unique())
    filtered_df = df[df['com_name'] == com]
    
    evaluations_count = filtered_df['Synthese_eval_sanit'].value_counts().reindex(
        ['Très satisfaisant', 'Satisfaisant', 'A améliorer', 'A corriger de manière urgente'], 
        fill_value=0
    )
    
    # Donut Chart
    fig = go.Figure(data=[go.Pie(
        labels=evaluations_count.index, 
        values=evaluations_count.values, 
        hole=.5, 
        marker=dict(colors=['#2ecc71', '#f1c40f', '#e67e22', '#e74c3c']),
        hoverinfo='label+percent+value'
    )])
    
    fig.update_layout(title=f"Sanitary assessments for the city {com} - Donut Chart")
    st.plotly_chart(fig)


# Counting the number of a given evaluation for a given type of area
def count_eval_by_area(df, area_column, selected, eval):
    filtered_df = df[(df[area_column] == selected) & (df['Synthese_eval_sanit'] == eval)]
    count = filtered_df.shape[0]
    return count


# Function to compare the number of a given evaluation between several region or department or city, depending on the user's choice
def evals(df):
    counts = {}
    area_type = st.selectbox("Choose the type of geographical area :", ['Region', 'Department', 'City'])
    evaluation_type = st.selectbox("Choose the evaluation :", ['Très satisfaisant', 'Satisfaisant', 'A améliorer', 'A corriger de manière urgente'])

    # Filter data based on user selection
    if area_type == 'Region':
        area_column = 'reg_name'
        reg = df[area_column].unique()
        selected_reg = st.multiselect(f"Select one or several {area_type} : ",
            options=reg,
            default=["Île-de-France"],  
        )
        if selected_reg:
            st.write("You have selected:", ", ".join(selected_reg))
            for item in selected_reg:
                counts[item] = count_eval_by_area(df, area_column, item, evaluation_type)
            
            eval_max = max(counts.values())
            reg_max = max(counts, key=counts.get)
            st.write(f"The region with the most '{evaluation_type}' is : {reg_max} with {eval_max} '{evaluation_type}'.")

    elif area_type == 'Department':
        area_column = 'dep_name'
        dep = df[area_column].unique()
        selected_dep = st.multiselect(f"Select one or several {area_type} : ",
            options=dep,
            default=["La Réunion"],  
        )
        if selected_dep:
            st.write("You have selected:", ", ".join(selected_dep))
            for item in selected_dep:
                counts[item] = count_eval_by_area(df, area_column, item, evaluation_type)
            
            eval_max = max(counts.values())
            dep_max = max(counts, key=counts.get)
            st.write(f"The department with the most '{evaluation_type}' is : {dep_max} with {eval_max} '{evaluation_type}'.")
    else:  # Commune
        area_column = 'com_name'
        com = df[area_column].unique()
        selected_com = st.multiselect(f"Select one or several {area_type} : ",
            options=com,
            default=["Paris"],  
        )
        if selected_com:
            st.write("You have selected:", ", ".join(selected_com))
            for item in selected_com:
                counts[item] = count_eval_by_area(df, area_column, item, evaluation_type)
            
            eval_max = max(counts.values())
            com_max = max(counts, key=counts.get)
            st.write(f"The city with the most '{evaluation_type}' is : {com_max} with {eval_max} '{evaluation_type}'.")


# Sorting the dataframe based on a given evaluation type and for a given type of area
def count_top3_eval(df, area_column, evaluation_type):
    return df[df['Synthese_eval_sanit'] == evaluation_type].groupby(area_column).size().to_dict()


# Function to get the top areas with the most selected evaluation
def get_top_areas(df):
    # Select the geographical area type and evaluation type
    area_type = st.selectbox("Choose the type of geographical area:", ['Region', 'Department', 'City'])
    evaluation_type = st.selectbox("Choose the evaluation:", ['Très satisfaisant', 'Satisfaisant', 'A améliorer', 'A corriger de manière urgente'])

    if area_type == 'Region':
        area_column = 'reg_name'
    elif area_type == 'Department':
        area_column = 'dep_name'
    else:  # City
        area_column = 'com_name'

    counts = count_top3_eval(df, area_column, evaluation_type)

    top_3 = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:3])

    if top_3:
        max_area = max(top_3, key=top_3.get)
        st.write(f"The {area_type.lower()} with the most '{evaluation_type}' evaluations is: {max_area} with {top_3[max_area]} '{evaluation_type}'.")

    st.plotly_chart(bar_chart_plotly(top_3, area_type, evaluation_type), use_container_width=True)


# Function to get a bar chart of the 3 best evaluations
def bar_chart_plotly(top_3, area_type, evaluation_type):
    labels = list(top_3.keys())
    values = list(top_3.values())

    fig = px.bar(x=labels, y=values, title=f"Top 3 {area_type}s - '{evaluation_type}' Evaluations",
                 labels={'x': area_type, 'y': f'Number of {evaluation_type}'}, color_continuous_scale='Blues')

    fig.update_traces(marker=dict(color=['#AEC6CF', '#FFB347', '#B39EB5'])) 

    fig.update_layout(coloraxis_showscale=False, showlegend=False, 
                      xaxis_title=area_type, yaxis_title="Number of Evaluations")

    return fig


# Function to get an interactive map of all the establishments with their details
def interactive_map(df):
    # Getting the coordinates of the establishment
    df[['latitude', 'longitude']] = df['geores'].str.split(',', expand=True).astype(float)

    color_map = {
        'Très satisfaisant': '#AEC6CF',   # Light pastel blue
        'Satisfaisant': '#FFB347',        # Light pastel orange
        'A améliorer': '#B39EB5',         # Light pastel purple
        'A corriger de manière urgente': '#FF6961'  # Light pastel red
    }

    df['color'] = df['Synthese_eval_sanit'].map(color_map)

    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='APP_Libelle_etablissement',
        hover_data={
            'Adresse_2_UA': True,
            'Libelle_commune': True,
            'Code_postal':True,
            'filtre': True,
            'Date_inspection': True,
            'Synthese_eval_sanit': True,
            'latitude': False,
            'longitude': False
        },
        color='Synthese_eval_sanit',
        color_discrete_map=color_map,
        title="Map of Establishments with Health Evaluations",
        zoom=5,
        height=800
    )

    fig.update_layout(
        mapbox_style="carto-positron",  
        mapbox_zoom=5,  # Zoom level
        mapbox_center={"lat": df['latitude'].mean(), "lon": df['longitude'].mean()},  # Centered on the data
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


# Function to count evaluations for each establishment based on the selected are and evaluation
def count_eval_by_establishment(df, area_column, selected_area, evaluation_types):
    filtered_df = df[df[area_column] == selected_area]
    
    # Count evaluations for each establishment
    counts = {}
    for est in filtered_df['APP_Libelle_etablissement'].unique():
        count = filtered_df[filtered_df['APP_Libelle_etablissement'] == est]['Synthese_eval_sanit'].value_counts().get(evaluation_types[0], 0) + \
                filtered_df[filtered_df['APP_Libelle_etablissement'] == est]['Synthese_eval_sanit'].value_counts().get(evaluation_types[1], 0)
        counts[est] = count
    return counts


# Function to get the top 10 establishments based on the geographical area and evaluation
def get_top_establishments(df):
    area_type = st.selectbox("Choose the type of geographical area:", ['Region', 'Department', 'City'], key="area_type_select")
    
    evaluation_types = ['Très satisfaisant', 'Satisfaisant']
    
    if area_type == 'Region':
        area_column = 'reg_name'
    elif area_type == 'Department':
        area_column = 'dep_name'
    else:  # City
        area_column = 'com_name'

    unique_areas = df[area_column].unique()
    selected_area = st.selectbox(f"Select a {area_type}:", unique_areas, key="area_select")

    counts = count_eval_by_establishment(df, area_column, selected_area, evaluation_types)

    # Get the top 10 establishments 
    top_10 = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True)[:10])

    if top_10:
        fig = px.bar(
            x=list(top_10.values()),
            y=list(top_10.keys()),
            orientation='h',
            title=f"Top 10 Establishments in {selected_area} with Evaluations",
            labels={'x': "Number of Evaluations 'Très satisfaisant' and 'Satisfaisant'", 'y': 'Establishments'},
            hover_name=list(top_10.keys()),  
            hover_data={"Total Evaluations": list(top_10.values())},  # Hover data
            color=list(top_10.values()),
            color_continuous_scale="Greens"
        )
        
        fig.update_traces(hovertemplate="%{hovertext}<br>Total Evaluations 'Très satisfaisant' and 'Satisfaisant' : %{x}<extra></extra>", showlegend=False)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No evaluations found for the selected area.")


# Function to get the distribution of evaluations for the selected establishment activity
def get_eval_distribution(df, selected_activity):
    filtered_df = df[df['APP_Libelle_activite_etablissement'] == selected_activity]
    
    # Count occurrences of each evaluation type
    eval_counts = filtered_df['Synthese_eval_sanit'].value_counts()
    
    return eval_counts


# Function to display the pie chart
def display_pie_chart(eval_counts, selected_activity):
    # Create the pie chart
    fig = px.pie(
        values=eval_counts.values,
        names=eval_counts.index,
        title=f"Distribution of Evaluations for {selected_activity}",
        color=eval_counts.index,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    
    # Update the layout to remove the legend
    fig.update_traces(textinfo='percent+label', showlegend=False)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


# Function to get a pie chart of the evaluation of a given activity 
def get_activity_eval_distribution(df):
    activities = df['APP_Libelle_activite_etablissement'].unique()
    selected_activity = st.selectbox("Select an Activity:", activities)

    # Get the distribution of evaluations
    eval_counts = get_eval_distribution(df, selected_activity)

    if not eval_counts.empty:
        display_pie_chart(eval_counts, selected_activity)
    else:
        st.write("No evaluations found for the selected activity.")


# Function to get the evaluation of an establishment based on its activity
def get_eval_establishments_per_activity(df):
    selected_activity = st.selectbox(
        "Select Activity (APP_Libelle_activite_etablissement)",
        df['APP_Libelle_activite_etablissement'].unique()
    )

    # Filter the DataFrame based on the selected activity
    filtered_df = df[df['APP_Libelle_activite_etablissement'] == selected_activity]

    selected_establishment = st.selectbox(
        "Select Establishment (APP_Libelle_etablissement)",
        filtered_df['APP_Libelle_etablissement'].unique()
    )

    # Get the data for the selected establishment
    establishment_data = filtered_df[filtered_df['APP_Libelle_etablissement'] == selected_establishment]

    if not establishment_data.empty:
        eval_counts = establishment_data['Synthese_eval_sanit'].value_counts().reset_index()
        eval_counts.columns = ['Synthese_eval_sanit', 'Count']

        pastel_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#FFABAB']
        fig = px.pie(
            eval_counts,
            names='Synthese_eval_sanit',
            values='Count',
            title=f"Synthese Evaluation Sanit - {selected_establishment}",
            hover_name='Synthese_eval_sanit',  
            labels={'Synthese_eval_sanit': 'Sanitary Evaluation'},
            color_discrete_sequence=pastel_colors
        )

        fig.update_traces(textinfo='percent+label')
        
        st.plotly_chart(fig)


# function to get the evaluations of establishments which had several inspections
def get_eval_establishments_multiple_inspections(df):
    selected_activity = st.selectbox(
        "Select an Activity",
        df['APP_Libelle_activite_etablissement'].unique(),
        key="activity_selectbox"
    )

    filtered_df = df[df['APP_Libelle_activite_etablissement'] == selected_activity]

    multi_inspections = filtered_df['APP_Libelle_etablissement'].value_counts()
    establishments_with_multiple_inspections = multi_inspections[multi_inspections > 1].index

    filtered_df = filtered_df[filtered_df['APP_Libelle_etablissement'].isin(establishments_with_multiple_inspections)]

    selected_establishment = st.selectbox(
        "Select an Establishment",
        filtered_df['APP_Libelle_etablissement'].unique(),
        key="establishment_selectbox"
    )

    establishment_data = filtered_df[filtered_df['APP_Libelle_etablissement'] == selected_establishment]

    if not establishment_data.empty:
        establishment_data = establishment_data.sort_values(by='Date_inspection')

        fig = px.bar(
            establishment_data,
            x='Synthese_eval_sanit',
            y='Date_inspection',
            orientation='v',
            title=f"Synthese Evaluation Sanit - {selected_establishment}",
            labels={'Synthese_eval_sanit': 'Sanitary Evaluation', 'Date_inspection': 'Date of Inspection'},
            hover_data=['APP_Libelle_etablissement'],
            color_discrete_sequence=['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9']
        )

        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title='Sanitary Evaluation',
            yaxis_title='Date of Inspection',
            height=600
        )

        st.plotly_chart(fig)


# correlation matrix to see the relationship between variables
def correlation_matrix(df):
    df_copy = df.copy()
    label_encoders = {}
    categorical_columns = [
        'APP_Libelle_etablissement', 'Adresse_2_UA', 'Libelle_commune', 'Date_inspection',
        'APP_Libelle_activite_etablissement', 'Synthese_eval_sanit', 'geores', 'filtre', 'reg_name', 'dep_name', 'dep_code', 'com_name', 'com_code'
    ]

    for col in categorical_columns:
        le = LabelEncoder()
        df_copy[col] = le.fit_transform(df_copy[col].astype(str))
        label_encoders[col] = le

    # Sélectionner les colonnes d'intérêt pour la heatmap
    features = [
        'APP_Libelle_etablissement', 'Adresse_2_UA', 'Code_postal', 'Libelle_commune', 'Date_inspection',
        'APP_Libelle_activite_etablissement', 'Synthese_eval_sanit', 'APP_Code_synthese_eval_sanit',
        'geores', 'filtre', 'reg_name', 'reg_code', 'dep_name', 'dep_code',
        'com_name', 'com_code'
    ]

    # Calculer la matrice de corrélation
    corr_matrix = df_copy[features].corr()

    # Créer une heatmap interactive avec Plotly
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='Viridis',  # Utiliser 'Viridis' comme échelle de couleurs
        labels=dict(color='Coefficient de Corrélation'),
        title='Heatmap des Corrélations entre les Variables',
        aspect='auto'

    )

    # Ajuster la taille de la figure
    fig.update_layout(
        width=2500,  # Largeur personnalisée
        height=800,  # Hauteur personnalisée
    )

    st.plotly_chart(fig, use_container_width=True)


#### PORTFOLIO VIZUALISATION ####

# donut chart of my hard skills
def hard_skills():
    skills = ["Machine Learning", "Web Development",  "Other Programming Skills"]
    programming_languages = [
        ["Python", "R", "Pandas", "Numpy", "Matplotlib"],
        ["HTML", "CSS", "JS", "Express Js", "php"],
        ["Java", "C", "Linux"]
    ]

    # Corresponding proficiency levels 
    proficiencies = [
        [0.6, 0.1, 0.1, 0.1, 0.1],  # Percentages for Machine Learning languages
        [0.3, 0.3, 0.2,0.1, 0.1],        # Percentages for Web Development languages
        [0.4, 0.4, 0.2]              # Percentages for Other Programming Skills
    ]

    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],
                        subplot_titles=skills)

    # Pie charts for each skill
    for i, skill in enumerate(skills):
        fig.add_trace(go.Pie(
            labels=programming_languages[i],
            values=proficiencies[i],
            name=skill,
            hole=0.4, 
        ), row=1, col=i+1)

    fig.update_layout(
        title_text="Hard Skills by Programming Languages",
        showlegend=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)


# time line of my educational background
def education_timeline():
    data = {
    "Institution": [
        "EFREI Paris, Villejuif", 
        "Asia Pacific University, Malaysia", 
        "Lycée Léonard de Vinci, Levallois-Perret"
    ],
    "Description": [
        "2021-2023: Integrated Prep in Biology & Digital Technology (2 years)\n2023-2024: 1st year of Engineering Program", 
        "Sept. 2023 - Dec. 2023: Study Semester in Malaysia (4 months)", 
        "2021: Scientific High School Diploma (with Honors)"
    ],
    "Start": ["2021-09-01", "2023-09-01", "2018-09-01"],
    "End": ["2024-06-01", "2023-12-31", "2021-06-30"]
    }

    df = pd.DataFrame(data)
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])

    pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA"]

    # Create the timeline figure with pastel colors
    fig = px.timeline(
        df, 
        x_start="Start", 
        x_end="End", 
        y="Institution", 
        color="Institution", 
        hover_name="Institution",
        hover_data={"Description": True, "Start": False, "End": False},
        title="My Educational Journey",
        color_discrete_sequence=pastel_colors  # Set pastel colors
    )

    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(
        xaxis_title="Dates",
        yaxis_title="",
        hoverlabel=dict(bgcolor="white", font_size=12),
        showlegend=False
    )

    st.write("\n\n\n### Education 🎓")
    st.plotly_chart(fig, use_container_width=True)


# pie chart of the distribution of the sports I plaued
def pie_sports():
    data = {
        'Sports': ['Swimming 🏊🏼‍♀️', 'Boxing 🥊', 'Gym 🏋️‍♀️'],
        'Years': [11, 5, 3]
    }
    df = pd.DataFrame(data)

    # Créer le graphique en camembert avec une palette de couleurs correcte
    fig = px.pie(df, names='Sports', values='Years', title='Visualization of the sports I have played',
                color_discrete_sequence=px.colors.diverging.RdYlGn)

    st.plotly_chart(fig)



















