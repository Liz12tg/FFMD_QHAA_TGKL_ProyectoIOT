import paho.mqtt.client as mqtt
from time import sleep
import cv2, numpy as np, os

# Configuración MQTT
client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Procesamiento
os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")
frame = cv2.imread('/tmp/foto.jpg')
h = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 0])

if h < 25 or h > 160: color = "ROJO"
elif 30 < h < 85: color = "VERDE"
else: color = "AZUL"

client.publish("iot/sensor/color", color)
print(f"Publicado: {color}")
client.disconnect()