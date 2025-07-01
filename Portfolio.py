import streamlit as st
from plots import hard_skills, education_timeline, pie_sports, show_experiences_cards, soft_skills_display

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

st.sidebar.text("Engineering student in\nData Science & Bioinformatics\n")

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

st.markdown("# Welcome to my portfolio! ✨")
st.write("### Profile")
st.write(
    "Curious and passionate about biology 🧬, mathematics 📈 and digital technologies 💻, "
    "I aim to innovate in healthcare through data science and AI. I'm looking for a 12-month apprenticeship "
    "in Data Science and/or Bioinformatics starting in September 2025."
)

st.write("### Skills")

st.write("#### Programming")
st.write("- Python, C, Java, Shell, SQL, HTML, CSS, JS, R")

st.write("#### Data Science")
st.write("- Pandas, Matplotlib, Seaborn, Plotly Express")
st.write("- OpenCV, BeautifulSoup, Streamlit")
st.write("- NLP, signal/image/text processing")

st.write("#### Office & Tools")
st.write("- Microsoft Office (Excel, Word, Teams...)")


st.write("#### Languages")
st.write("- **English** : B2 (TOEIC 895/990)")
st.write("- **Spanish** : A1")


hard_skills()

soft_skills_display()

education_timeline()

show_experiences_cards()

st.write("### Interests")

st.write("#### Travel ✈️")
st.write("Malaysia, Singapore, Thailand, Morocco, Spain, Italy, Belgium, United Kingdom")

st.write("#### Sport 🏋️")
pie_sports()
