import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import cv2, numpy as np, os

# Configuración Base de Datos (usando ruta relativa al script)
db_path = os.path.join(os.path.dirname(__file__), '..', 'historial.db')
db = sqlite3.connect(db_path)
db.execute("CREATE TABLE IF NOT EXISTS registros (id INTEGER PRIMARY KEY, color TEXT, fecha TIMESTAMP)")
db.commit()

# Configuración Hardware/MQTT
factory = PiGPIOFactory()
s1 = Servo(17, pin_factory=factory)
client = mqtt.Client()
client.connect("192.168.1.72", 1883, 60)

# Adquisición y Clasificación
os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")
frame = cv2.imread('/tmp/foto.jpg')
h = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 0])

if h < 25 or h > 160: color = "ROJO"
elif 30 < h < 85: color = "VERDE"
else: color = "AZUL"

# Guardar en SQLite
db.execute("INSERT INTO registros (color, fecha) VALUES (?, ?)", (color, datetime.now()))
db.commit()
db.close()

# Publicar
client.publish("iot/sensor/color", color)
print(f"Detectado: {color}. Publicado.")
client.disconnect()
