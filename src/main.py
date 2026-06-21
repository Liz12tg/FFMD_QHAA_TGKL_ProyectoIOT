import paho.mqtt.client as mqtt
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Configuración de Actuadores
factory = PiGPIOFactory()
s1 = Servo(17, pin_factory=factory)
s2 = Servo(18, pin_factory=factory)

def on_message(client, userdata, msg):
    color = msg.payload.decode()
    print(f"Recibido: {color}. Ejecutando secuencia...")
    
    # Secuencia de movimiento
    s1.value = -0.5
    sleep(1)
    
    if color == "ROJO": s2.min()
    elif color == "VERDE": s2.mid()
    else: s2.max()
    
    sleep(2)
    s1.value = -1
    print("Secuencia terminada.")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("iot/sensor/color")
client.on_message = on_message

print("Esperando mensajes MQTT para actuar...")
client.loop_forever()