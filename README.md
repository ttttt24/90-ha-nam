Mô tả dự án: dự án này sử dụng ESP8266 để đo nhiêt độ, độ ẩm, ánh sáng và gửi dữ liệu lên một trang web được thiết kế giống da tả dự án: dự án này sử dụng ESP8266 để đo nhiêt độ, độ ẩm, ánh sáng, tốc độ gió và gửi dữ liệu lên một trang web được thiết kế giống dashboard hiển thị theo thời gian thực được gửi lên. Hơn nữa có thể điều khiển các chức năng phần cứng từ web thông qua MQTT. Các cảm biến sẽ thu thập dữ liệu từ môi trường sau đó sẽ truyền cho ESP8266 để nó gửi lên API của Web thông qua MQTT. 
Chuẩn bị:
•	ESP8266: ESP8266 . Nó được sử dụng rộng rãi trong các ứng dụng IoT (Internet of Things) như cảm biến thông minh, hệ thống kiểm soát thiết bị, hoặc các ứng dụng điều khiển từ xa. Trong dự án nó được dùng để giao tiếp với cảm biến và đưa dữ liệu lên cơ sở dữ liệu.
•	Cảm biến nhiệt độ, độ ẩm DHT11: đo nhiệt độ và độ ẩm.
•	Cảm biến ánh sáng: đo cường độ ánh sáng.
•	Điện trở.
•	Dây điện.
•	Nguồn cấp 5V từ cổng USB của máy tính.
•	Giao diện web để hiển thị các dữ liệu cảm biến.
Sơ đồ nguyên lý:
•	Cảm biến nhiệt độ - ESP: VCC-3.3V; GND-GND; Data-D2.
•	Cảm biến ánh sáng – ESP: VCC-3.3V; GND-GND; A0 – A0.
•	D5- trở - LED- GDN, D6- trở - LED- GDN, D7- trở - LED- GDN dùng để điều khiển led khi nhận tín hiệu từ web gửi qua mqtt.
•	D0- trở - LED- GDN dùng để nháy cảnh báo khi tốc độ gió > 50.
Phần mềm:
•	Arduino IDE dùng để nạp code cho ESP8266.
•	Visual studio code dùng để viết các chương trình backend và fontend để thực hiện các chức năng trên web.
Set up:
•	Cài đặt các thư viện cho Arduino IDE: DHT sensor library, Adafruit Sensor Library, ESP8266Wifi, ESP8266WebServer.
•	Trên visual studio code cài các extension cần thiết để chạy web.
•	Kết nối Esp8266 với máy tính bằng USB.
•	Nạp code cho Esp8266 sau khi đã cấu hình wifi cho phù hợp: tên wifi, mật khẩu, địa chỉ ip của wifi, user, password và port để kết nối với mqtt.
Phần xử lý: dữ liệu từ ESP vào database bằng cách chạy file python mqtt-to-mysql.py, dữ liệu từ database đẩy lên API bằng file mysql_to_web2.py, file control-led.py dùng để điệu khiển led khi có tín hiệu từ web gửi xuống.
Cấu trúc thư mục:
Web:
•	Idea
•	Static/images
	ảnh
•	Templates
	Các file .html thực hiện các chức năng của web
•	Và các file .py
Chạy các file .py ở terminal sau đó mở địa chỉ có trong terminal của mqtt-to-mysql.py để mở giao diện web.

