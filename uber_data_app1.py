def page_content_uber1():     
    import streamlit as st
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time

    st.title("Uber Data 1")

    st.write("Uber Data 1 Dataframe : ")
    df = pd.read_csv("data/uber-raw-data-apr14-updated.csv", parse_dates = ['Date/Time'])
    st.write(df)

    st.write("Adding the day of the months, weekday and hour : ")
    def get_dom(dt):
        return dt.day # day is an attribute 

    def get_weekday(dt):
        return dt.weekday()

    def get_hour(dt):
        return dt.hour

    df['day'] = df['Date/Time'].map(get_dom)
    df['weekday'] = df['Date/Time'].map(get_weekday)
    df['hour'] = df['Date/Time'].map(get_hour)

    st.write(df.head())

    # Visualization

    hist = df["day"].plot.hist(bins = 30, rwidth = 0.8, range=(0.5, 30.5), title = "Frequency by DoM - Uber - April 2014")
    plt.xlabel('Days of the month')
    st.pyplot(plt)

    st.write("Grouping : ")
    def count_rows(rows):
        return len(rows)

    by_date = df.groupby('day').apply(count_rows)
    by_date

    plt.clf()

    plt.figure(figsize = (10, 5))
    plt.title('Line plot - Uber - April 2014')
    plt.xlabel('Days of the month')
    plt.ylabel('Frequency')
    plt.plot(by_date)
    st.pyplot(plt)

    st.write("Sort : ")

    plt.clf()
    plt.figure(figsize = (10, 5))
    plt.bar(range(1,31), by_date.sort_values())
    plt.xticks(range(1,31), by_date.sort_values().index)
    plt.xlabel('Date of the month')
    plt.ylabel('Frequency')
    plt.title('Frequency by DoM - Uber - April 2014')
    st.pyplot(plt)

    st.write("Heatmap : ")

    df2 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()
    df2.head()
    heatmap = sns.heatmap(df2,linewidths = 0.5)
    #Annoted heatmap
    plt.title('Heatmap by Hour and weekdays - Uber - April 2014', fontsize=15)
    heatmap.set_yticklabels(('Lun Mar Mer Jeu Ven Sam Dim').split(), rotation='horizontal')
    st.pyplot(plt)

    st.write("Latitude and Longitute with twiny(): ")

    plt.clf()
    plt.figure(figsize=(10,10), dpi=100)
    plt.title('Longitute and Latitude distribution - Uber - April 2014', fontsize=15)
    plt.hist(df['Lon'], bins = 100, range = (-74.1, -73.9), color = 'g', alpha = 0.5, label = 'Longitude')
    plt.legend(loc = 'best')
    plt.twiny()
    plt.hist(df['Lat'], bins = 100, range = (40.5, 41), color = 'r', alpha = 0.5, label = 'Latitude')
    plt.legend(loc = 'upper left')
    st.pyplot(plt)

    st.write("Latitude and Longitute : ")
    plt.clf()
    plt.figure(figsize=(10,10), dpi=100)
    plt.title('Scatter plot - Uber - April 2014')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.scatter(df['Lat'], df['Lon'], s=0.8, alpha=0.4)
    plt.ylim(-74.1, -73.9)
    plt.xlim(40.7, 40.9)
    st.pyplot(plt)