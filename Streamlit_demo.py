import streamlit as st
from joblib import load
import pandas as pd
import numpy as np



df=pd.read_csv("booking.csv")  #adjust it based on your path
pd.set_option('display.max_columns', None)


st.set_page_config(
    page_title="Hotel Cancellation Prediction Project",
    page_icon="https://cloudfront-eu-central-1.images.arcpublishing.com/thenational/LVOFB25TFJDCJII3XHWI5FEAJU.jpg",
    menu_items={
        "Get help": "mailto:emreoksuzbusiness@outlook.com"
       
    }
)


st.title("Hotel Cancellation Prediction Project")


st.markdown("A research company aims to predict hotel booking cancellations based on customer behavior and various features, such as the number of adults, lead time, average price, and more.")


st.image("https://imageio.forbes.com/specials-images/imageserve/5cdb058a5218470008b0b00f/Nobu-Ryokan-Malibu/0x0.jpg?format=jpg&height=1009&width=2000")

st.markdown("After recent advancements in the field of artificial intelligence, the research company anticipates our assistance in creating a machine learning model tailored to their requirements.")
st.markdown("Furthermore, they seek a solution that allows predicting hotel cancellations based on provided information. Let's address their needs and deliver a powerful predictive tool.")
st.markdown("*Let's help them!*")

st.image("https://press.sripanwa.com/assets/uploads/data_img/77724-204-one-bedroom-luxury-villa.jpg")









st.sidebar.markdown("**Choose** the features below to see the result!")


name = st.sidebar.text_input("Name", help="Please capitalize the first letter of your name!")
surname = st.sidebar.text_input("Surname", help="Please capitalize the first letter of your surname!")
adult = st.sidebar.number_input("Number of Adults", min_value=0, format="%d")
child= st.sidebar.number_input("Number of Children", min_value=0, format="%d")
lead_time = st.sidebar.number_input("Lead Time", min_value=0 ,format="%d")
average_price = st.sidebar.number_input("Average Price", min_value=0 ,format="%d")
week_nights = st.sidebar.number_input("Number of Week nights", min_value=0,max_value=5 ,format="%d")
weekend_nights = st.sidebar.number_input("Number of Weekend nights", min_value=0,max_value=2 ,format="%d")
car_parking_space = st.sidebar.number_input("Car Parking Space", min_value=0,max_value=1 ,format="%d")
season = st.sidebar.selectbox("Season", ["Fall", "Spring", "Summer", "Winter"])
market_segment = st.sidebar.selectbox("Market Segment", ["Aviation", "Complementary", "Corporate", "Offline", "Online"])
room_type = st.sidebar.selectbox("Room Type", [1, 2, 3, 4, 5, 6, 7])
meal_plan = st.sidebar.selectbox("Meal Plan", [1, 2])
special_requests = st.sidebar.number_input("Special Request", min_value=0, max_value=5)

new_model = load("xgboost_model.pkl2")
# List of columns used for encoding in the training data
encoded_columns = ['Season_Fall', 'Season_Spring', 'Season_Summer', 'Season_Winter',
                   'market segment type_Aviation', 'market segment type_Complementary',
                   'market segment type_Corporate', 'market segment type_Offline',
                   'market segment type_Online', 'room type_Room_Type 1', 'room type_Room_Type 2',
                   'room type_Room_Type 4', 'room type_Room_Type 5', 'room type_Room_Type 6',
                   'room type_Room_Type 7',"type of meal_Meal Plan 1"]

input_data = {
    'number of adults': [adult],
    'number of children': [child],
    'number of weekend nights': [weekend_nights],
    'car parking space': [car_parking_space],
    'number of week nights': [week_nights],
    'lead time': [lead_time],
    'average price': [average_price],
    'special requests': [special_requests],
    'type of meal_Meal Plan 1': [1 if meal_plan==1 else 0],
    'type of meal_Meal Plan 2': [1 if meal_plan==2 else 0],
    'Season_Fall': [1 if season == "Fall" else 0],
    'Season_Spring': [1 if season == "Spring" else 0],
    'Season_Summer': [1 if season == "Summer" else 0],
    'Season_Winter': [1 if season == "Winter" else 0],
    'market segment type_Aviation': [1 if market_segment=="Aviation" else 0],
    "market segment type_Complementary": [1 if market_segment=="Complementary" else 0],
    'market segment type_Corporate': [1 if market_segment=="Corporate" else 0],
    'market segment type_Offline': [1 if market_segment=="Offline" else 0],
    'market segment type_Online': [1 if market_segment=="Online" else 0],
    "room type_Room_Type 1": [1 if room_type== 1 else 0],
    "room type_Room_Type 2": [1 if room_type== 2 else 0],
    "room type_Room_Type 4": [1 if room_type== 4 else 0],
    "room type_Room_Type 5": [1 if room_type== 5 else 0],
    "room type_Room_Type 6": [1 if room_type== 6 else 0],
    "room type_Room_Type 7": [1 if room_type== 7 else 0],



}

input_df = pd.DataFrame(input_data)





pred = new_model.predict(input_df.values)


if st.sidebar.button("Submit"):


    st.info("You can find the result below.")

    from datetime import date, datetime

    today = date.today()
    time = datetime.now().strftime("%H:%M:%S")

    results_df = pd.DataFrame({
        'Name': [name],
        'Surname': [surname],
        'Date': [today],
        'Time': [time],
        "Season": [season],
        "Price": [average_price],
        "Lead Time" :[lead_time],
        'Prediction': [pred]

    })

    results_df["Prediction"] = results_df["Prediction"].apply(lambda x: "Canceled" if x == 1 else "Not Canceled")


    st.table(results_df)



