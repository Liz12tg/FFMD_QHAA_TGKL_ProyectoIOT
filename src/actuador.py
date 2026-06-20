import paho.mqtt.client as mqtt
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Setup actuador
factory = PiGPIOFactory()
s2 = Servo(18, pin_factory=factory)

def on_message(client, userdata, msg):
    color = msg.payload.decode()
    print(f"Recibido: {color}. Activando servo...")
    if color == "ROJO": s2.min()
    elif color == "VERDE": s2.mid()
    else: s2.max()

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("iot/sensor/color")
client.on_message = on_message

print("Esperando mensajes MQTT...")
client.loop_forever()