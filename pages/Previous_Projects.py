import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from Alim_Data_Project import page_content_alim_data
from explain.app import page_content_explain
from AutoInsight.Home import page_home_autoinsight, page_demographics_autoinsight, page_sales_autoinsight, page_pred_autoinsight, page_about_autoinsight, page_contact_autoinsight
from ecg.Home import page_home_ecg, page_preprocessing, page_frequency_analysis, page_models

st.set_page_config(layout="wide")

page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "ECG Project", "Deep Learning Project","Explain", "AutoInsight", "Alim Confiance Data"]
)


if page == "Home":
    st.title(" Discover my previous Data Science projects !✨")
    st.markdown("### Projects completed during my studies at **EFREI Paris**")

    st.markdown("""
    Welcome to the project showcase of my data science journey.  
    Each project listed below was developed during my academic training and reflects the application of essential data science workflows including data preprocessing, visualization, and predictive modeling techniques (supervised, unsupervised, and semi-supervised learning).

    These projects illustrate a blend of technical proficiency and problem-solving skills in real-world datasets.
    """)

    st.divider()

    # Define projects and descriptions
    projects = [
        {
            "title": "🫀 ECG Project",
            "description": "Signal processing and classification of ECG data to detect cardiac anomalies using supervised learning algorithms.",
            "skills": "Time series preprocessing, feature extraction, classification, evaluation metrics."
        },
        {
            "title": "🧠 Deep Learning Project",
            "description": "Image generation and classification using convolutional neural networks applied to computer vision datasets.",
            "skills": "TensorFlow/Keras, CNN architectures, CPU training, hyperparameter tuning, model interpretability."
        },
        {
            "title": "📈 Explain",
            "description": "Explainable Patent Classification. Interpretability-focused dashboard that explains machine learning model predictions using SHAP and LIME.",
            "skills": "Model explainability, Streamlit dashboarding, SHAP values."
        },
        {
            "title": "📊 AutoInsight",
            "description": "A comprehensive analytics tool for exploring car sales data and making strategic recommendations.",
            "skills": "EDA, regression models, Streamlit apps, recommendation systems."
        },
        {
            "title": "🥗 Alim Confiance Data",
            "description": "Data cleaning and visualization of French restaurant hygiene ratings, and prediction.",
            "skills": "Geospatial analysis, supervised learning, map visualization (Folium)."
        }
    ]

    cols = st.columns(3)
    for i, project in enumerate(projects):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                    <div style="background-color:#f9f9f9; padding: 20px; border-radius: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px; height: 340px;">
                        <h4 style="margin-bottom:10px;">{project['title']}</h4>
                        <p style="font-size: 14px; color: #333;">{project['description']}</p>
                        <p style="font-size: 13px;"><strong>Skills:</strong> {project['skills']}</p>
                    </div>
                """, unsafe_allow_html=True)

elif page == "ECG Project":

    p = st.sidebar.selectbox(
        "ECG Project",
        ["Home", "Preprocessing", "Frequency Analysis", "Predictive Models"]
    )

    if p == "Home":
        page_home_ecg()
    elif p == "Preprocessing":
        page_preprocessing()
    elif p == "Frequency Analysis":
        page_frequency_analysis()
    elif p == "Predictive Models":
        page_models()

elif page == "Deep Learning Project":

    import streamlit as st
    import streamlit.components.v1 as components

    # Load the HTML content
    with open("Deep_Learning_Project_Marion_FRESQUET_Manel_EL_KOUCH_ING2_BIOINF.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Display in Streamlit
    components.html(html_content, height=1000, scrolling=True)

elif page == "Explain":
    page_content_explain()

elif page == "AutoInsight":

    p = st.sidebar.selectbox(
        "AutoInsight Project",
        ["Home", "Demographics Insight", "Sales Analysis", "Strategic Recommendations", "About Us", "Contact"]
    )

    if p == "Home":
        page_home_autoinsight()
    elif p == "Demographics Insight":
        page_demographics_autoinsight()
    elif p == "Sales Analysis":
        page_sales_autoinsight()
    elif p == "Strategic Recommendations":
        page_pred_autoinsight()
    elif p == "About Us":
        page_about_autoinsight()
    elif p == "Contact":
        page_contact_autoinsight()
    


elif page == "Alim Confiance Data":

    page_content_alim_data()