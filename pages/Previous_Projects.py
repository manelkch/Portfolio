import streamlit as st
from tips_data_app import page_content_tips
from uber_data_app1 import page_content_uber1
from uber_data_app2 import page_content_uber2

st.set_page_config(layout="wide")

page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Tips Data Project", "Uber Data Project 1", "Uber Data Project 2"]
)


if page == "Home":
    st.markdown("# Discover my previous projects !✨")
    st.write("\n\n- **Tips Data Project 💸**\n - **Uber Data Project 1 🚗**\n- **Uber Data Project 2 📍**\n")

elif page == "Tips Data Project":
    st.markdown("# Discover the Tips Data Project ! 💸")
    page_content_tips()

elif page == "Uber Data Project 1":
    st.markdown("# Discover the Uber Data Project 1 ! 🚗")
    page_content_uber1()

elif page == "Uber Data Project 2":
    st.markdown("# Discover the Uber Data Project 2 ! 📍")
    page_content_uber2()