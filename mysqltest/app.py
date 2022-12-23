import traceback

import mysql.connector
import random
from flask import Flask, request, render_template

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="python_db",
    port="3306"
)
cursor = db.cursor()

app = Flask(__name__)

'''
cursor.execute('SELECT * from cars')
cars = cursor.fetchall()
for car in cars:
    print(car)
for car in cars:
    print('brand', car[1])
    print('model', car[2])

'''
@app.route('/', methods=['POST', 'GET'])
def hello_world_post():
    if request.method == "POST":
        car_data = ''
        text = request.form['text']
        cur = ''
        try:
            cur = db.cursor()
            query = f"SELECT * FROM cars WHERE id={text};"
            cur.execute(query)
            row = cur.fetchone()
            car_data = str(row)
            if car_data is None:
                car_data = 'No employee with selected id'
        except Exception as e:
            print(e)
            cur.execute("ROLLBACK")
            db.commit()
            traceback.print_exc()
            car_data = 'Entered data was not an id'
        finally:
            cur.close()
            return render_template('index.html', car_id=text, car_data=car_data)
    if request.method == 'GET':
            return render_template('index.html', car_id='', car_data='')

app.run()
