import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import json

# Cấu hình MQTT
mqtt_host = '192.168.231.46'
mqtt_port = 2003
mqtt_user = 'tutran'
mqtt_password = '1234'
mqtt_topic = 'out'  # Thay đổi chủ đề theo cấu hình

# Cấu hình MySQL
mysql_host = '127.0.0.1'
mysql_user = 'root'
mysql_password = '24012003'
mysql_database = 'du_lieu'


# Hàm xử lý tin nhắn nhận được từ MQTT
def on_message(client, userdata, msg):
    print(f"Nhận được tin nhắn từ chủ đề {msg.topic}: {msg.payload.decode()}")

    try:
        #  dữ liệu nhận được
        received_data = msg.payload.decode()
        print(f"Dữ liệu nhận được: {received_data}")

        # Kiểm tra nếu dữ liệu không rỗng
        if not received_data:
            print("Không nhận được dữ liệu nào.")
            return

        # Tách chuỗi và lấy các giá trị
        data_parts = received_data.split(', ')
        temperature = None
        humidity = None
        light = None
        rainfall = None

        for part in data_parts:
            key, value = part.split(': ')
            if key == 'Nhietdo':
                temperature = int(float(value.replace(' C', '').strip()))  
            elif key == 'Doam':
                humidity = int(value.replace('%', '').strip())  
            elif key == 'Anhsang':
                light = int(value.replace(' Lux', '').strip())  
            elif key == 'Luongmua':
                rainfall = int(value.replace(' mm', '').strip())  

        # Kiểm tra xem tất cả các giá trị đã được lấy
        if temperature is None or humidity is None or light is None or rainfall is None:
            print("Thiếu dữ liệu cần thiết từ tin nhắn.")
            return

        # Kết nối tới cơ sở dữ liệu MySQL
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )
        if connection.is_connected():
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO sensor_data (temperature, humidity, light, rainfall) VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql_insert_query, (temperature, humidity, light, rainfall))
            connection.commit()
            print("Dữ liệu đã được chèn vào MySQL.")
    except ValueError as ve:
        print(f"Lỗi khi chuyển đổi dữ liệu: {ve}")
    except Error as e:
        print(f"Lỗi khi kết nối hoặc chèn dữ liệu vào MySQL: {e}")
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Đã đóng kết nối với MySQL.")

client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.on_message = on_message

# Kết nối tới broker MQTT
try:
    client.connect(mqtt_host, mqtt_port, 60)
    print("Kết nối đến MQTT thành công.")
except Exception as e:
    print(f"Lỗi kết nối đến MQTT: {e}")

# Đăng ký chủ đề và bắt đầu lắng nghe
client.subscribe(mqtt_topic)
client.loop_forever()
