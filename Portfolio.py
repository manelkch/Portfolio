import streamlit as st
from plots import *

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1200px;  
        padding-left: 5%;
        padding-right: 5%;
        color : #746c70;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.image("img/bitmoji.png")
st.sidebar.title("Manel EL KOUCH")

st.sidebar.text("Second year engineering\nstudent in bioinformatics\n")

st.sidebar.markdown(
    """
    <style>
    .custom-link {
        color: black; 
        text-decoration: none;
    }
    
    .custom-link:hover {
        color: #274472;
    }
    </style>
    <a class="custom-link" href="https://www.linkedin.com/in/manel-el-kouch/" target="_blank">💼 Find me on LinkedIn</a>
    <br>
    <a class="custom-link" href="https://github.com/manelkch" target="_blank">💻 Find me on GitHub</a>
    """,
    unsafe_allow_html=True
)

st.markdown("# Welcome to my portfolio !✨")
st.write("### Profile")
st.write("Passionate about the mechanisms of the biological 🧬 phenomena that surround us, mathematics 📈 and programming 💻, I'm curious and eager to make a difference. I'd like to join a dynamic team where I can contribute to innovative projects combining digital technology 🌐, data analysis 📊 and healthcare 💊.")

st.write("### Skills")

hard_skills()

st.write("#### Soft skills ")
st.write("- **Project management**")
st.write("- **Tenacity**")
st.write("- **Autonomy**")
st.write("- **Open-mindedness**")

education_timeline()

st.write("### Professional experiences 💼")
st.write("- **Mc Donald's Champerret, Paris** : 2 months (Jun. - Jul. 2023)")
st.write("- **Fnac des Ternes, Paris** : 1 months internship (Dec. 2022 - Jan. 2023)")
st.write("- **Centre socioculturel Louise Michel, Asnières** : 1 months internship (Jun. 2022) ")
st.write("- **Pharmacie SO OUEST, Levallois-Perret** : 1 week internship (Jan. 2018) ")

st.write("### Languages")
st.write("- **English** : C1 (950/990 TOEIC)")
st.write("- **Spanish** : A1")

st.write("### Interests ")

st.write("##### Travel ")
st.write("🛩️ Malaysia, Singapore, Thailand, Morocco, Spain, Italy, Belgium, United Kingdom.")

st.write("##### Sport ")
pie_sports()

