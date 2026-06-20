import paho.mqtt.client as mqtt
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import cv2, numpy as np, os

# Configuración MQTT
BROKER = "localhost"
TOPIC_COLOR = "iot/sensor/color"
client = mqtt.Client()
client.connect(BROKER, 1883, 60)

# Configuración de Servos
factory = PiGPIOFactory()
s1 = Servo(17, pin_factory=factory)
s2 = Servo(18, pin_factory=factory)

# 1. Escaneo
s1.value = -0.5
sleep(1)
os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")

# 2. Procesamiento
frame = cv2.imread('/tmp/foto.jpg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
h = np.mean(hsv[:, :, 0])

# 3. Clasificación
if h < 25 or h > 160: color = "ROJO"
elif 30 < h < 85: color = "VERDE"
else: color = "AZUL"

# 4. Publicar mensaje y actuar
client.publish(TOPIC_COLOR, color)
print(f"Detectado: {color}. Mensaje enviado a {TOPIC_COLOR}")

if color == "ROJO": s2.min()
elif color == "VERDE": s2.mid()
else: s2.max()

sleep(2)
s1.value = -1
client.disconnect()