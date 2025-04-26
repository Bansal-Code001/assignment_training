import pandas as pd
import pickle
import streamlit as st
data = pd.read_csv(r"/Users/priyanshubansal/developer/training/training_material/09_Day/Used_Bikes.csv")
pipe = pickle.load(open(r"/Users/priyanshubansal/developer/training/training_material/09_Day/model.pkl", "rb"))

st.title("Bike Price Prediction")
st.write("This app predicts the price of used bikes based on various features.")

st.sidebar.header("Select the Brand of Bike")
brand = st.sidebar.selectbox("Choose a brand:",data["brand"].unique())

power = st.selectbox("Choose the CC Power of your bike : ",data["power"].unique())
age = st.number_input("Enter how old Your Bike: ",0,20)
kms_driven = st.slider("select the Kilometer driven of your bike",1,99999,1000,100)
owner = st.radio("Select the Owner :",data["owner"].unique())

input_data = pd.DataFrame([{
            "kms_driven": kms_driven,
            "owner": owner,
            "age": age,
            "power": power,
            "brand": brand
        }])

predict = st.button("Get Bike Price ")
if predict:
    price = pipe.predict(input_data)[0]
    price = round(price, 2)
    st.success(f"Your Bike Price is : {price}")