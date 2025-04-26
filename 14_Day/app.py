from flask import Flask, render_template, request, redirect, url_for
import joblib
#import mysql.connector
import pandas as pd


## load the model
model = joblib.load('bike_prediction_model.lb')

# initialise the flask application
app = Flask(__name__)

## mysql database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user="root",
            password="",
            database="bike_prediction"
        )
        return conn
    except mysql.connector.Error as err:

@app.route('/')
def home():
      return render_template('index.html')

@app.route("/projct")
def projct():
    return render_template('projct.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/history',methods=["GET","POST"])
def history():
    brand_name_filter = request.form.get(
        'brand_name_filter',None)

    

    # conn = get_db_connection()
historical_data = []

if conn:
    cursor = conn.cursor(dictionary=True)
    try:
        if brand_name_filter:
            query = "SELECT * FROM bike_data WHERE brand_name = %s"
            cursor.execute(query, (brand_name_filter,))
        else:
            query = "SELECT * FROM bike_data"
            cursor.execute(query)

            ## fetch all the data
            historical_data = cursor.fetchall()
    except mysql.connector.Error as err:
            print(f"Error fetching data from mysql : {err}")
    finally:
            cursor.close()
            conn.close()
    return render_template('history.html', historical_data=historical_data)

## prediction route
@app.route('/predict', methods=['POST'])
def predict():
            if request.method == 'post':
                 try:
                      brand_name = request.form['brand_name']
                      owner_name = request.form['owner']
                      age_bike = request.form['age']
                      power_bike = int(request.form['power'])
                      kms_driven_bike = int(request.form['kms_driven'])
                      bike_number  = {'TVS': 0,
                        'Royal Enfield': 1,
                        'Triumph': 2,
                        'Yamaha': 3,
                        'Honda': 4,
                        'Hero': 5,
                        'Bajaj': 6,
                        'Suzuki': 7,
                        'Benelli': 8,
                        'KTM': 9,
                        'Mahindra': 10,
                        'Kawasaki': 11,
                        'Ducati': 12,
                        'Hyosung': 13,
                        'Harley-Davidson': 14,
                        'Jawa': 15,
                        'BMW': 16,
                        'Indian': 17,
                        'Rajdoot': 18,
                        'LML': 19,
                        'Yezdi': 20,
                        'MV': 21,
                        'Ideal': 22}
                      brand_name_encoded = bike_number.get(brand_name, -1)
                      ## make prediction 
                      input_data = [[owner_name,brand_name_encoded,
                                     kms_driven_bike,
                                     age_bike,
                                     power_bike]]
                      prediction = model.predict(input_data)[0]
                      prediction = round(prediction, 2)

                       ## save prediction to database
                       conn = get_db_connection()
                    if conn:
                           cursor = conn.cursor()
                           query = "INSERT INTO bike_data (owner_name,brand_name, kms_driven_bike, age_bike, power_bike,prediction) VALUES (%s, %s, %s, %s, %s, %s)"
                           user_data = (owner_name, brand_name, kms_driven_bike, age_bike, power_bike, prediction)
                            cursor.execute(query, user_data)
                            conn.commit()
                            cursor.close()
                            conn.close()
                            return render_template('predict.html', prediction=prediction)
                 except Exception as e:  
                      print(e)
                           

if __name__ == '__main__':
    app.run(debug=True,host='0,0,0,0',port = 2525)                          

