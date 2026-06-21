import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import cv2, numpy as np, os

# Configuración Base de Datos (Ruta relativa)
db_path = os.path.join(os.path.dirname(__file__), '..', 'historial.db')
db = sqlite3.connect(db_path)
db.execute("CREATE TABLE IF NOT EXISTS registros (id INTEGER PRIMARY KEY, color TEXT, fecha TIMESTAMP)")
db.commit()

# Configuración Hardware y MQTT
factory = PiGPIOFactory()  # Evita parpadeo (jitter) en los servos
s1 = Servo(17, pin_factory=factory)  # Pin físico 11 (GPIO 17)
client = mqtt.Client()
client.connect("192.168.1.72", 1883, 60)

# Adquisición de imagen y conversión a HSV
os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")
frame = cv2.imread('/tmp/foto.jpg')
h = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 0])  # Promedio canal Hue

# Umbralización matemática por rangos cromáticos
if h < 25 or h > 160: color = "ROJO"
elif 30 < h < 85: color = "VERDE"
else: color = "AZUL"

# Persistencia local
db.execute("INSERT INTO registros (color, fecha) VALUES (?, ?)", (color, datetime.now()))
db.commit()
db.close()

# Publicación en el Broker
client.publish("iot/sensor/color", color)
print(f"Detectado: {color}. Publicado.")
client.disconnect()