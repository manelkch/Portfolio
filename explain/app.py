
def page_content_explain():
    import shap
    import streamlit as st
    import pickle
    import time
    from streamlit_shap import st_shap

    #image1 = 'explain/logo_projet.webp'
    #image2 = 'explain/lipstipxefrei.png'

    # Créer trois colonnes
    #col1, col2, col3 = st.columns([1, 1, 2])

    # Afficher les images dans les colonnes
    #with col1:
        #st.image(image1)

    #with col3:
        #st.image(image2, width=320)

    # Titre de l'application
    st.markdown(
        """
        <div style="background-color: #e4ebf3;padding:10px;border-radius:10px;text-align:center;">
        <h1 style="color:rgb(45,24,127);">LIPSTIP x EFREI</h1>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<h2 style="color: rgba(80,7,133,255);">EXPLAIN - Classifieur de demande de brevet</h2>'
        '<li>Votre partenaire en propriété intellectuelle.</li>'
        '<li>Précision et automatisation : une nouvelle façon de classifier des brevets.</li>'
        '<li>Optimisez la précision de vos classifications de brevets.</li><br>',
        unsafe_allow_html=True
    )


    #claim = st.text_input("Veuillez saisir la revendication à classifier :")
    #submitted_nb = st.button("Valider")

    #st.write(f"Num claim : {num_claim}.")

    num_claim = st.number_input("**Veuillez saisir le numéro de la revendication à classifier :**", min_value=0, max_value=50000)
    submitted_nb = st.button("Valider")

    time.sleep(3)

    with open('explain/num_claim.pkl', 'wb') as f:
        pickle.dump(num_claim, f)

    #time.sleep(3)

    if submitted_nb:

        # Charger la variable depuis le fichier
        with open('explain/claim.pkl', 'rb') as f:
            claim = pickle.load(f)

        st.write(f"Num claim : {num_claim}.")

        st.subheader("Revendication à classifier :\n")
        st.write(claim)

        with open('explain/predictions.pkl', 'rb') as f:
            predictions = pickle.load(f)
        #st.write(f"Code CPC de votre demande : {predictions}.")

        st.subheader("Résultat de la classification :\n")

        with open('explain/shap_values_list.pkl', 'rb') as f:
            shap_values_list = pickle.load(f)
        #st.write(f"Code CPC de votre demande : {shap_values_list}.")

        for shap_values in shap_values_list:
            st_shap(shap.plots.text(shap_values), height=800, width=800)
    
    
