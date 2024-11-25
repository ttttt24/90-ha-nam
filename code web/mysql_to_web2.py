from flask import Flask, render_template, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection(database):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="24012003",
            database=database
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Fetch latest sensor data and activity data from MySQL
@app.route('/get_data', methods=['GET'])
def get_data():
    connection1 = get_db_connection("du_lieu")
    connection2 = get_db_connection("device")

    if connection1 is None or connection2 is None:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor1 = connection1.cursor()
        cursor2 = connection2.cursor()

        cursor1.execute("SELECT temperature, humidity, light, rainfall, thoigian FROM du_lieu.sensor_data ORDER BY id DESC LIMIT 1")
        sensor_data = cursor1.fetchone()

        cursor2.execute("SELECT device, hoat_dong, thoi_gian FROM device.device_status ORDER BY id DESC LIMIT 1")
        activity_data = cursor2.fetchone()

        # Return the combined data
        if sensor_data and activity_data:
            return jsonify({
                "device": activity_data[0],
                "hoat_dong": activity_data[1],
                "thoi_gian": activity_data[2],
                "humidity": sensor_data[1],
                "light": sensor_data[2],
                "temperature": sensor_data[0],
                "rainfall": sensor_data[3],
                "time": sensor_data[4]
            })
        else:
            return jsonify({"error": "No data found"}), 404
    except Error as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "Error fetching data from the databases"}), 500
    finally:
        cursor1.close()
        cursor2.close()
        connection1.close()
        connection2.close()

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/activity')
def activity():
    return render_template('activity.html')

@app.route('/new')
def new():
    return render_template('new.html')

if __name__ == '__main__':
    app.run(debug=True, port=5500)