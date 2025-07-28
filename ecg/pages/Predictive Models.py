from detection_methods import article_method, autoencoder, isolation_forest
import streamlit as st
from streamlit_option_menu import option_menu

#st.set_page_config(layout="wide")

# Define sections and their content
sections = [ 
    "CNN Method",
    "Autoencoder Method",
    "Isolation Forest Method"
  
]

# Sidebar: clickable list of sections
with st.sidebar:
    selected_section = option_menu(
        menu_title=None,
        options=sections,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "nav-link-selected": {"background-color": "#dde7e4", "color": "black",}
        }
    )


if selected_section == "CNN Method":
    st.title("ECG Arrhythmia Detection")
    st.markdown("Based on the **shallow CNN model** from Rasti et al. (2024)")

    article_method()

if selected_section == "Autoencoder Method":
    
    autoencoder()


if selected_section == "Isolation Forest Method":
    
    isolation_forest()