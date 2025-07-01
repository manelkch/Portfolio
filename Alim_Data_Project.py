

def page_content_alim_data():
    from streamlit_option_menu import option_menu
    from plots import eval_per_feature, eval_per_region, eval_per_com, eval_per_dep, get_activity_eval_distribution, get_eval_distribution, evals, get_top_areas, interactive_map, get_top_establishments, correlation_matrix, get_eval_establishments_multiple_inspections, get_eval_establishments_per_activity
    from data_preprocessing import data_preprocessing
    from prediction_model import main_mlp

    import streamlit as st
    import pandas as pd
    import nbformat
    import io
    import contextlib    

    

    df = pd.read_csv('data/export_alimconfiance.csv', delimiter=";")
    df_clean = data_preprocessing(df)

    def objective_presentation(df):
        st.title("Results of official health inspections: “Alim'confiance” information system.")
        st.write("According to the source : 'Publishing the results of health checks in the food sector (restaurants, canteens, abattoirs, etc.) is a legitimate expectation of citizens that helps improve consumer confidence. Provided for in the French Law on the Future of Agriculture, Food and Forestry of October 13, 2014, this measure is part of a move towards greater transparency in government action. The decree on the transparency of State controls in the field of food safety in France published on December 17, 2016 generalizes the experiment conducted in Paris and Avignon from July to December 2015. Publication of the results of controls carried out from March 1, 2017 onwards in all establishments in the food chain will be effective from April 3, 2017, on the website www.alim-confiance.gouv.fr.'")
        st.write("Source : https://www.data.gouv.fr/fr/datasets/resultats-des-controles-officiels-sanitaires-dispositif-dinformation-alimconfiance/")

        st.markdown("## Problem : Where can you eat in France without risking food poisoning ?")

        st.markdown("#### 🔍 Data Overview")
        st.write(df.head(20))

        st.markdown("#### 🔢 Features explanation")
        st.write("- ###### APP_Libelle_etablissement : \n   - Type : string\n   - Meaning : Names of establishments.")
        st.write("- ###### SIRET : \n   - Type : int\n   - Meaning : A 14-digit identifier for businesses in France. (INSEE - Official SIRET definition)")
        st.write("- ###### Adresse_2_UA : \n   - Type : string\n   - Meaning : Address details, containing street names and numbers.")
        st.write("- ###### Code_postal : \n   - Type : int\n   - Meaning : 5-digit postal codes used in France. (Official postal code system from La Poste)")
        st.write("- ###### Libelle_commune : \n   - Type : string\n   - Meaning : Name of cities or towns.")
        st.write("- ###### Date_inspection : \n   - Type : datetime\n   - Meaning : Date of inspection in `YYYY-MM-DD` format. (Standard date formats as per [ISO 8601])")
        st.write("- ###### APP_Libelle_activite_etablissement : \n   - Type : string\n   - Meaning : Descriptions of activities (e.g., 'restaurant', 'Alimentation générale'). General classifications found in datasets on data.gouv.fr.")
        st.write("- ###### Synthese_eval_sanit : \n   - Type : string\n   - Meaning : Sanitary evaluation summary ('Très satisfaisant', 'Satisfaisant', 'A améliorer', 'A corriger de manière urgente'). (French Ministry of Agriculture and Food)")
        st.write("- ###### APP_Code_synthese_eval_sanit : \n   - Type : int\n   - Meaning : Codes corresponding to the sanitary evaluations. From 1 to 4.")
        st.write("- ###### Agrement : \n   - Type : int\n   - Meaning : Certification or approval identifiers. (French Ministry of Agriculture and Food)")
        st.write("- ###### geores : \n   - Type : object\n   - Meaning : Geographic coordinates (latitude, longitude). (WGS84 standard)")
        st.write("- ###### filtre : \n   - Type : string\n   - Meaning : Filter criteria (e.g., 'Restaurants', 'Métiers de bouche').")
        st.write("- ###### ods_type_activite : \n   - Type : string\n   - Meaning : Type of activity (e.g., 'Lait et produits laitiers', 'Viandes et produits carnés', 'Autres')")
        st.write("- ###### reg_name : \n   - Type : string\n   - Meaning : Name of the region (e.g., 'Île-de-France').")
        st.write("- ###### reg_code : \n   - Type : int\n   - Meaning : Official codes for regions. (Region coding system)")
        st.write("- ###### dep_name : \n   - Type : string\n   - Meaning : Department name (e.g., 'Seine-et-Marne').")
        st.write("- ###### dep_code : \n   - Type : int\n   - Meaning : Department code, two or three digits. (Department codes defined by France's statistical agency)")
        st.write("- ###### com_name : \n   - Type : string\n   - Meaning : Commune or municipality name. (Commune data from France's statistical agency)")
        st.write("- ###### com_code : \n   - Type : int\n   - Meaning : 5-digit INSEE code for communes. (France's official commune coding system.)")


        st.markdown("#### 🎯 Objectives of the project")
        st.write("The objective of this analysis is to **identify for each area the tendancieses of the sanitary assessment of food businesses**. We also want to **predict this assessment result for a given restaurant** based on its previous evaluations and the tendancies of the city, department or region from which it belongs.")

        st.markdown("#### Steps of the project")
        st.write(" - Step 1. Data Preprocessing \n - Step 2. Data Analysis \n - Step 3. Prediction Model \n")


    def data_preprocessing_notebook():
        display_notebook("Data_preprocessing.ipynb")


    def display_notebook(notebook_path):
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)

        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                st.markdown(cell.source)
            elif cell.cell_type == 'code':
                st.code(cell.source)

                if 'outputs' in cell:
                    for output in cell.outputs:
                        if output.output_type == 'stream':
                            st.text(output.text)
                        elif output.output_type == 'execute_result':
                            st.write(output.data['text/plain'])
                        elif output.output_type == 'error':
                            st.error(''.join(output.traceback))


    with st.sidebar:
        selected=option_menu(
            menu_title = "Menu",
            options = ["Objective", "Data Preprocessing", "Data Analysis", "Prediction Model"], 
            icons = ["check2-circle", "database", "bar-chart-line", "robot"],
            menu_icon = "house",
            default_index = 0,
        )

    if selected == "Objective":
        #st.title(f"🎯 {selected} Page")
        objective_presentation(df)

    if selected == "Data Preprocessing":
        data_preprocessing_notebook()

    if selected == "Data Analysis":
        st.title("Where can you eat in France without risking food poisoning ?")
        st.markdown("### Analysis of official health inspection results.")

        st.markdown("#### 1. Summary of health evaluations per feauture.")
        eval_per_feature(df_clean)

        st.markdown("##### - Evaluations per regions.")
        eval_per_region(df_clean)
        st.markdown("##### - Evaluations per department.")
        eval_per_dep(df_clean)
        st.markdown("##### - Evaluations per city.")
        eval_per_com(df_clean)

        st.markdown("\n\n#### 2. Distribution of sanitary evaluations per type of establishment.")
        get_activity_eval_distribution(df_clean)

        st.markdown("#### 3. Comparison of sanitary evaluations per type of geographical area.")
        evals(df_clean)

        st.markdown("\n\n#### 4. Top 3 health-safest geographical areas.")
        get_top_areas(df_clean)

        st.markdown("\n\n#### 5. Map of establishments with sanitary evaluations.")
        interactive_map(df_clean)

        st.markdown("\n\n#### 6. Top 10 health-safest places to eat.")
        get_top_establishments(df_clean)

        st.markdown("\n\n#### 7. Correlation between dataset variables.")
        correlation_matrix(df_clean)

        st.markdown("\n\n#### 8. Distribution of the sanitary evaluations per activity.")
        get_eval_establishments_per_activity(df_clean)

        st.markdown("\n\n#### 9. Comparison of the sanitary evaluations over time.")
        get_eval_establishments_multiple_inspections(df_clean)


    if selected == "Prediction Model":
        st.title("Sanitary Evaluation Prediction")
        main_mlp(df_clean)
