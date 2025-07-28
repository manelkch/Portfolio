import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    p {
        text-align: justify;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6 {
        color: #6e6d78;
    }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2, col3 = st.columns(3)

with col2:
    st.image("img/auto.png")

def main():    
    st.title("Contact Us - AutoInsight")
    st.write("""
    Welcome to AutoInsight, your go-to solution for comprehensive analysis and strategic recommendations on car sales. 
    We're here to help dealerships optimize their stock management and maximize sales performance. 
    If you have any questions, feedback, or need assistance, feel free to reach out to us using the information below.
    """)

    st.header("Contact Information")
    st.write("**Email:** support@autoinsight.com")
    st.write("**Phone:** +1 (123) 456-7890")
    st.write("""
    **Address:**  
    AutoInsight HQ  
    1234 Car Dealership Blvd,  
    Suite 567, Auto City, AC 78901
    """)

    st.header("Working Hours")
    st.write("""
    - **Monday to Friday:** 9:00 AM - 6:00 PM  
    - **Saturday:** 10:00 AM - 4:00 PM  
    - **Sunday:** Closed
    """)

    st.header("Follow Us")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("[Twitter](#)")
    with col2:
        st.write("[LinkedIn](#)")
    with col3:
        st.write("[Facebook](#)")

    st.header("Feedback & Support")
    st.write("We value your feedback! Let us know how we can improve AutoInsight to better meet your needs. For any support requests, please use the form below, and our team will get back to you as soon as possible.")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send Message")

        if submitted:
            if name and email and message:
                # Here you can add your logic to send the form data (e.g., via email or storing in a database)
                st.success("Thank you for reaching out! We will get back to you shortly.")
            else:
                st.error("Please fill out all fields before submitting.")

if __name__ == "__main__":
    main()
