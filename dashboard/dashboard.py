import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from pathlib import Path

sns.set(style="dark")
st.header(":bike: Bike Sharing Dashboard :bike:")

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='date').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt" : "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "casual": "casual_count",
        "registered": "registered_count",
        "cnt": "total_orders"
    }, inplace=True)
    
    return daily_orders_df

def create_season_df(df):
    season_df = df.groupby(by="season").cnt.sum().sort_values(ascending=False).reset_index()
    season_df.rename(columns={
    "cnt": "customer_count"
    }, inplace=True)

    return season_df

def create_weathersit_df(df):
    weather_df = df.groupby(by="weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    weather_df.rename(columns={
    "cnt": "customer_count"
    }, inplace=True)

    return weather_df

def create_temp_df(df):
    df["temp_group"] = df.temp.apply(lambda x: "Cold" if x <= 10 else ("Hot" if x > 30 else "Normal"))
    temp_df = df.groupby(by=["temp_group"]).cnt.sum().sort_values(ascending=False).reset_index()
    temp_df.rename(columns={
    "cnt": "customer_count"
    }, inplace=True)
    
    return temp_df

def create_hum_df(df):
    df["hum_group"] = df.humidity.apply(lambda x: "Dry" if x <= 30 else ("Wet" if x > 71 else "Normal"))
    hum_df = df.groupby(by=["hum_group"]).cnt.sum().sort_values(ascending=False).reset_index()
    hum_df.rename(columns={
    "cnt": "customer_count"
    }, inplace=True)
    
    return hum_df

def create_wind_df(df):
    df["windspeed_group"] = df.windspeed.apply(lambda x: "Light Winds" if x <= 12 else ("Strong Winds" if x > 22 else "Moderate Winds"))
    wind_df = df.groupby(by=["windspeed_group"]).cnt.sum().sort_values(ascending=False).reset_index()
    wind_df.rename(columns={
    "cnt": "customer_count"
    }, inplace=True)
    
    return wind_df

def sidebar(df):
    df["date"] = pd.to_datetime(df["date"])
    min_date = df["date"].min()
    max_date = df["date"].max()

    with st.sidebar:
        st.image("https://github.com/esaepulloh/Project-Dicoding/blob/master/dashboard/Capital%20Bikeshare%20Logo.png?raw=true")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu", 
            min_value=min_date, 
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

if __name__ == "__main__":
    day_df_csv = Path(__file__).parents[1] / 'dashboard/main_data.csv'
    day_df = pd.read_csv(day_df_csv)
    
    date = sidebar(day_df)
    if(len(date) == 2):
        main_df = day_df[(day_df["date"] >= str(date[0])) & (day_df["date"] <= str(date[1]))]
    else:
        main_df = day_df[(day_df["date"] >= str(st.session_state.date[0])) & (day_df["date"] <= str(st.session_state.date[1]))]

    daily_orders_df = create_daily_orders_df(main_df)
    season_df = create_season_df(main_df)
    weather_df = create_weathersit_df(main_df)
    temp_df = create_temp_df(main_df)
    hum_df = create_hum_df(main_df)
    wind_df = create_wind_df(main_df)

    
    st.subheader('Daily Orders')
    col1, col2, col3 = st.columns(3)
 
    with col1:
        total_orders = daily_orders_df.total_orders.sum()
        st.metric("Total orders", value=total_orders)
 
    with col2:
        casual_orders = daily_orders_df.casual_count.sum()
        st.metric("Total Casual Orders", value=casual_orders)
    
    with col3:
        registered_orders = daily_orders_df.registered_count.sum()
        st.metric("Total Registered Order", value=registered_orders)
 
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        daily_orders_df["date"],
        daily_orders_df["total_orders"],
        marker='o', 
        linewidth=2,
        color="#96BDC9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
 
    st.pyplot(fig)
    
    st.subheader("Number of Customer by Season & Weather")
 
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
    colors = ["#96BDC9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(x="customer_count", y="season", data=season_df, palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel("Number of Customer", fontsize=30)
    ax[0].set_title("Number of Customer by Season", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)
    
    sns.barplot(x="customer_count", y="weathersit", data=weather_df, palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel("Number of Customer", fontsize=30)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Number of Customer by Weather", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)
    
    st.pyplot(fig)
    
    st.subheader("Number of Customer by Temperature, Humidity & Windspeed")
    col1, col2, col3 = st.columns(3)
 
    with col1:
        fig, ax = plt.subplots(figsize=(15, 25))
 
        sns.barplot(
            y="customer_count", 
            x="temp_group",
            data=temp_df.sort_values(by="customer_count", ascending=False),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Customer by Temperature", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)
 
    with col2:
        fig, ax = plt.subplots(figsize=(15, 25))
 
        sns.barplot(
            y="customer_count", 
            x="hum_group",
            data=hum_df.sort_values(by="customer_count", ascending=False),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Customer by Humidity", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)
        
        with col3:
            fig, ax = plt.subplots(figsize=(15, 25))
 
            sns.barplot(
                y="customer_count", 
                x="windspeed_group",
                data=wind_df.sort_values(by="customer_count", ascending=False),
                palette=colors,
                ax=ax
            )
            ax.set_title("Number of Customer by Windspeed", loc="center", fontsize=50)
            ax.set_ylabel(None)
            ax.set_xlabel(None)
            ax.tick_params(axis='x', labelsize=35)
            ax.tick_params(axis='y', labelsize=30)
            st.pyplot(fig)

    year_copyright = datetime.date.today().year
    copyright = "Copyright © " + str(year_copyright) + " | Bike Sharing Dashboard | All Rights Reserved | " + "Made with :heart: by [@esaepulloh](https://www.linkedin.com/in/epul-saepulloh-827467218/)"
    st.caption(copyright)