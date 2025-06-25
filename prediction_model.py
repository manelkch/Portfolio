import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score

# 
def preprocess_data(df):
    df_copy = df.copy()

    label_encoder_sanit = LabelEncoder()
    label_encoder_etablissement = LabelEncoder()
    label_encoder_activite = LabelEncoder()

    df_copy['Synthese_eval_sanit'] = label_encoder_sanit.fit_transform(df_copy['Synthese_eval_sanit'])
    df_copy['APP_Libelle_etablissement'] = label_encoder_etablissement.fit_transform(df_copy['APP_Libelle_etablissement'])
    df_copy['APP_Libelle_activite_etablissement'] = label_encoder_activite.fit_transform(df_copy['APP_Libelle_activite_etablissement'])


    X = df_copy[['APP_Libelle_etablissement', 'APP_Libelle_activite_etablissement', 'Code_postal']]
    y = df_copy['Synthese_eval_sanit']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test, label_encoder_sanit, label_encoder_etablissement, label_encoder_activite

# Train MLP Model
def train_model(X_train, y_train):
    mlp = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=1)
    mlp.fit(X_train, y_train)
    return mlp

# Evaluate Model and Display Report
def evaluate_model(mlp, X_train, X_test, y_train, y_test):

    y_train_pred = mlp.predict(X_train)
    y_test_pred = mlp.predict(X_test)
    
    train_report = classification_report(y_train, y_train_pred, zero_division=0)
    test_report = classification_report(y_test, y_test_pred, zero_division=0)
    
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    return train_report, test_report, train_accuracy, test_accuracy


def main_mlp(df):
    X_train, X_test, y_train, y_test, label_encoder_sanit, label_encoder_etablissement, label_encoder_activite = preprocess_data(df)

    mlp = train_model(X_train, y_train)

    train_report, test_report, train_accuracy, test_accuracy = evaluate_model(mlp, X_train, X_test, y_train, y_test)

    st.subheader("Model Evaluation")
    st.write("**Training Set Accuracy:**", train_accuracy)
    st.write("**Test Set Accuracy:**", test_accuracy)
    
    st.subheader("Classification Report - Training Set")
    st.text(train_report)

    st.subheader("Classification Report - Test Set")
    st.text(test_report)

    selected_establishment = st.selectbox(
        "Select Establishment (APP_Libelle_etablissement)",
        df['APP_Libelle_etablissement'].unique()
    )

    if st.button("Predict"):
        if selected_establishment in label_encoder_etablissement.classes_:
            establishment_encoded = label_encoder_etablissement.transform([selected_establishment])[0]
        else:
            st.warning(f"The establishment '{selected_establishment}' is not present in the training data.")
            return

        input_features = [[establishment_encoded, 0, 12345]]  
        try:
            prediction = mlp.predict(input_features)
            predicted_eval = label_encoder_sanit.inverse_transform(prediction)[0]
            st.write(f"The predicted Sanitary Evaluation for {selected_establishment} is: {predicted_eval}")
        except ValueError as e:
            st.error(f"Prediction error: {e}")




