def page_content_uber2(): 
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt

    st.title("Uber Data 2")

    path = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv"
    df = pd.read_csv(path, delimiter = ',')
    st.write("Uber Data 2 Dataframe : ")
    st.write(df)

    st.write("Pickup locations : ")
    plt.figure(figsize=(15,15), dpi=100)
    plt.title('Scatter plot - Uber - Pickup locations')
    plt.xlabel('Pickup Latitude')
    plt.ylabel('Pickup Longitude')
    plt.scatter(df['pickup_latitude'], df['pickup_longitude'], s=0.8, alpha=0.4, color = "green")
    plt.ylim(-74.1, -73.9)
    plt.xlim(40.7, 40.9)
    st.pyplot(plt)


    st.write("Dropoff locations : ")
    plt.figure(figsize=(15,15), dpi=100)
    plt.title('Scatter plot - Uber - Dropoff locations')
    plt.xlabel('Dropoff Latitude')
    plt.ylabel('Dropoff Longitude')
    plt.scatter(df['dropoff_latitude'], df['dropoff_longitude'], s=0.8, alpha=0.4, color = "red")
    plt.ylim(-74.1, -73.9)
    plt.xlim(40.7, 40.9)
    st.pyplot(plt)

    plt.clf()

    st.write("Pickup and Dropoff locations :")

    plt.figure(figsize=(15, 15), dpi=100)
    plt.title('Scatter plot - Uber - Pickup and Dropoff locations')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')

    plt.scatter(df['pickup_latitude'], df['pickup_longitude'], s=0.8, alpha=0.4, color="green", label='Pickup locations')
    plt.scatter(df['dropoff_latitude'], df['dropoff_longitude'], s=0.8, alpha=0.4, color="red", label='Dropoff locations')

    plt.ylim(-74.1, -73.9)
    plt.xlim(40.7, 40.9)

    plt.legend()
    st.pyplot(plt)

    st.write("Tip Amout : ")

    def count_rows(rows):
        return len(rows)

    by_tip = df.groupby('tip_amount').apply(count_rows)

    plt.clf()
    plt.title('Line plot - Uber 2')
    plt.xlabel('Tip Amount')
    plt.ylabel('Frequency')
    plt.plot(by_tip)
    st.pyplot(plt)