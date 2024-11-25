from flask import Flask, render_template
import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

# khoi tao Flask app
app = Flask(__name__)

mqtt_host = "192.168.231.46"
mqtt_port = 2003
mqtt_topic_in = "in"

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='24012003',
    database='device'
)
cursor = conn.cursor()
client = mqtt.Client()
client.username_pw_set("tutran", "1234")  

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    thoi_gian = datetime.now()

    if message.lower() == "on":
        devices = ['led1', 'led2', 'led3']
        hoat_dong = "on"
        for device in devices:
            insert_into_db(device, hoat_dong, thoi_gian)

    elif message.lower() == "off":
        devices = ['led1', 'led2', 'led3']
        hoat_dong = "off"
        for device in devices:
            insert_into_db(device, hoat_dong, thoi_gian)

    else:
        parts = message.split('-')
        if len(parts) == 2:
            device = parts[0]
            hoat_dong = parts[1]
            insert_into_db(device, hoat_dong, thoi_gian)
        else:
            print(f"Invalid message format: {message}")

# ham insert data vao MySQL
def insert_into_db(device, hoat_dong, thoi_gian):
    query = "INSERT INTO device_status (device, hoat_dong, thoi_gian) VALUES (%s, %s, %s)"
    cursor.execute(query, (device, hoat_dong, thoi_gian))
    conn.commit()
    print(f"Inserted into DB: {device}, {hoat_dong}, {thoi_gian}")

# Flask route to control LEDs via web interface
@app.route('/led/<device>/<state>')
def control_led(device, state):
    message = f"led{device}-{state}"
    try:
        result = client.publish(mqtt_topic_in, message)
        result.wait_for_publish()
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Message sent: {message}")
        else:
            print(f"Message failed: {result.rc}")
    except Exception as e:
        print(f"Error sending MQTT message: {e}")

    return f"{device} is turned {state}"

@app.route('/')
def index():
    return render_template('index2.html')
@app.route('/new')
def new():
    return render_template('new.html')
def connect_mqtt():
    try:
        client.connect(mqtt_host, mqtt_port, 60)
        client.loop_start()
        print("Connected to MQTT broker")
        client.on_message = on_message
        client.subscribe(mqtt_topic_in)
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")

connect_mqtt()

if __name__ == '__main__':
    app.run(debug=True)
# Clean up after stopping the server
@app.teardown_appcontext
def close_db(exception):
    cursor.close()
    conn.close()
    client.loop_stop()
    print("MySQL and MQTT connections closed.")
