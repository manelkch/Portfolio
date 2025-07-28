import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns(3)

with col2:
    st.image("img/auto.png")
    
st.title("Strategic Recommendations")

st.markdown("Based on the **sales data analysis**, we provide **strategic recommendations** to **optimize stock management and marketing**.")
st.write("Understand which regions are leading in sales and where to invest resources for maximum impact.")

option = st.sidebar.selectbox("Choose the prediction model :", ["Predict specific sales !", "Predict your region's sales !", "Predict your dealership's sales !", "Predict model's sales in a region !"])

if option == "Predict specific sales !":
    # Dictionary mapping companies to their models
    company_models = {
        'Ford': ['Expedition', 'Taurus', 'Explorer', 'F-Series', 'Ranger'],
        'Dodge': ['Durango', 'Ram Van', 'Ram Pickup', 'Ram Wagon', 'Dakota', 'Neon', 'Viper', 'Caravan'],
        'Cadillac': ['Eldorado', 'Escalade', 'Catera', 'DeVille', 'Seville'],
        'Toyota': ['Celica', 'Corolla', 'Land Cruiser', 'Tacoma', 'Camry', '4Runner', 'RAV4', 'Sienna', 'Avalon'],
        'Acura': ['TL', 'RL', 'Integra'],
        'Mitsubishi': ['Diamante', 'Montero Sport', 'Eclipse', 'Mirage', '3000GT', 'Galant', 'Montero'],
        'Volvo': ['S40', 'C70', 'S70', 'S80', 'V40', 'V70'],
        'Mercury': ['Mountaineer', 'Sable', 'Villager', 'Mystique', 'Cougar'],
        'Buick': ['Park Avenue', 'Regal', 'Century', 'LeSabre'],
        'Saturn': ['SW', 'LW', 'SL'],
        'Jaguar': ['S-Type'],
        'Volkswagen': ['Jetta', 'Beetle', 'Passat', 'GTI', 'Golf'],
        'Lexus': ['ES300', 'GS300', 'GS400', 'LS400', 'LX470', 'RX300'],
        'BMW': ['328i', '528i', '323i', 'Z3'],
        'Subaru': ['Outback', 'Forester'],
        'Chevrolet': ['Cavalier', 'Corvette', 'Impala', 'Lumina', 'Monte Carlo', 'Blazer'],
        'Nissan': ['Maxima', 'Frontier', 'Pathfinder', 'Sentra', 'Xterra'],
        'Hyundai': ['Elantra', 'Accent', 'Sonata'],
        'Porsche': ['Carrera Cabrio', 'Boxter', 'Carrera Coupe'],
        'Honda': ['Accord', 'Civic', 'Odyssey', 'Passport', 'CR-V'],
    }

    company = st.selectbox("Select a company:", list(company_models.keys()))

    if company:
        models = company_models[company]
        model = st.selectbox("Select a model:", models)

    Price_in_thousands = st.selectbox("Select a price in thousands:", ['26', '19', '31', '14', '24', '12', '42', '21', '61', '39', '25', '17', '22', '45'])
    Dealer_Location = st.selectbox("Select a dealer address:", ['44 Walnut St', '4333 Ogden Ave', '3 Green Tree Trl', '3203 W Marie St', '6137 S Us-51'])
    Dealer_Region = st.selectbox("Select a dealer region:", ['Middletown', 'Aurora', 'Greenville', 'Pasco', 'Janesville', 'Scottsdale', 'Austin'])

    filtered_url = f"http://127.0.0.1:8000/get-prediction/{company}/{model}/{Price_in_thousands}/{Dealer_Location}/{Dealer_Region}"
    filtered_response = requests.get(filtered_url)

    if filtered_response.status_code == 200:
        pred = filtered_response.json()
        st.write(f"Car Sales Prediction : **{pred['prediction']}** cars.")
    else:
        st.error("Failed to fetch filtered data from the API")

if option == "Predict your region's sales !":
    Dealer_Region = st.selectbox("Select a dealer region : ", ['Middletown', 'Aurora', 'Greenville', 'Pasco', 'Janesville', 'Scottsdale', 'Austin'])

    company = st.selectbox("Select a company:", ['Ford', 'Dodge', 'Cadillac', 'Toyota', 'Acura', 'Mitsubishi', 'Volvo', 'Mercury','Buick', 'Saturn', 'Jaguar', 'Volkswagen', 'Lexus', 'BMW', 'Subaru', 'Chevrolet',
    'Nissan', 'Plymouth', 'Hyundai', 'Porsche', 'Oldsmobile', 'Honda', 'Pontiac', 'Lincoln', 'Mercedes-B', 'Infiniti', 'Jeep', 'Chrysler', 'Saab', 'Audi'])

    filtered_url = f"http://127.0.0.1:8000/get-prediction-region/{Dealer_Region}/{company}"
    filtered_response = requests.get(filtered_url)

    if filtered_response.status_code == 200:
        pred = filtered_response.json()
        st.write(f"Car Sales Prediction for **{company}** in **{Dealer_Region}** : **{pred['prediction']}** cars.")
    else:
        st.error("Failed to fetch filtered data from the API")

if option == "Predict your dealership's sales !":
    Dealer_Location = st.selectbox("Select your dealer address : ", ['44 Walnut St', '4333 Ogden Ave', '3 Green Tree Trl', '3203 W Marie St', '6137 S Us-51', '6640 E McDowell Rd', '8501 Research Blvd'])

    company = st.selectbox("Select a company:", ['Ford', 'Dodge', 'Cadillac', 'Toyota', 'Acura', 'Mitsubishi', 'Volvo', 'Mercury','Buick', 'Saturn', 'Jaguar', 'Volkswagen', 'Lexus', 'BMW', 'Subaru', 'Chevrolet',
    'Nissan', 'Plymouth', 'Hyundai', 'Porsche', 'Oldsmobile', 'Honda', 'Pontiac', 'Lincoln', 'Mercedes-B', 'Infiniti', 'Jeep', 'Chrysler', 'Saab', 'Audi'])

    filtered_url = f"http://127.0.0.1:8000/get-prediction-concession/{Dealer_Location}/{company}"
    filtered_response = requests.get(filtered_url)

    if filtered_response.status_code == 200:
        pred = filtered_response.json()
        st.write(f"Car Sales Prediction of **{company}** in **{Dealer_Location}** : **{pred['prediction']}** cars.")
    else:
        st.error("Failed to fetch filtered data from the API")

if option == "Predict model's sales in a region !":
    # Dictionary mapping companies to their models
    company_models = {
        'Ford': ['Expedition', 'Taurus', 'Explorer', 'F-Series', 'Ranger'],
        'Dodge': ['Durango', 'Ram Van', 'Ram Pickup', 'Ram Wagon', 'Dakota', 'Neon', 'Viper', 'Caravan'],
        'Cadillac': ['Eldorado', 'Escalade', 'Catera', 'DeVille', 'Seville'],
        'Toyota': ['Celica', 'Corolla', 'Land Cruiser', 'Tacoma', 'Camry', '4Runner', 'RAV4', 'Sienna', 'Avalon'],
        'Acura': ['TL', 'RL', 'Integra'],
        'Mitsubishi': ['Diamante', 'Montero Sport', 'Eclipse', 'Mirage', '3000GT', 'Galant', 'Montero'],
        'Volvo': ['S40', 'C70', 'S70', 'S80', 'V40', 'V70'],
        'Mercury': ['Mountaineer', 'Sable', 'Villager', 'Mystique', 'Cougar'],
        'Buick': ['Park Avenue', 'Regal', 'Century', 'LeSabre'],
        'Saturn': ['SW', 'LW', 'SL'],
        'Jaguar': ['S-Type'],
        'Volkswagen': ['Jetta', 'Beetle', 'Passat', 'GTI', 'Golf'],
        'Lexus': ['ES300', 'GS300', 'GS400', 'LS400', 'LX470', 'RX300'],
        'BMW': ['328i', '528i', '323i', 'Z3'],
        'Subaru': ['Outback', 'Forester'],
        'Chevrolet': ['Cavalier', 'Corvette', 'Impala', 'Lumina', 'Monte Carlo', 'Blazer'],
        'Nissan': ['Maxima', 'Frontier', 'Pathfinder', 'Sentra', 'Xterra'],
        'Hyundai': ['Elantra', 'Accent', 'Sonata'],
        'Porsche': ['Carrera Cabrio', 'Boxter', 'Carrera Coupe'],
        'Honda': ['Accord', 'Civic', 'Odyssey', 'Passport', 'CR-V'],
    }

    # User selects a company
    company = st.selectbox("Select a company:", list(company_models.keys()))

    # User selects a model based on the selected company
    models = company_models.get(company, [])
    model = st.selectbox("Select a model:", models)

    Dealer_Region = st.selectbox("Select a dealer region:", ['Middletown', 'Aurora', 'Greenville', 'Pasco', 'Janesville', 'Scottsdale', 'Austin'])

    filtered_url = f"http://127.0.0.1:8000/get-prediction-model-region/{company}/{model}/{Dealer_Region}"
    filtered_response = requests.get(filtered_url)

    if filtered_response.status_code == 200:
        pred = filtered_response.json()
        st.write(f"Car Sales Prediction : **{pred['prediction']}** cars.")
    else:
        st.error("Failed to fetch filtered data from the API")
