import paho.mqtt.client as mqtt
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()
s1 = Servo(17, pin_factory=factory)  # Servo 1 (Alimentador) - Pin 11
s2 = Servo(18, pin_factory=factory)  # Servo 2 (Clasificador) - Pin 12

s1.value = 1  # Estado inicial: bloqueo
print("Sistema listo. Esperando color...")

# Callback: se activa al recibir un mensaje MQTT
def on_message(client, userdata, msg):
    color = msg.payload.decode()
    print(f"Recibido: {color}. Ejecutando acción...")
    
    # 1. Alinear rampa deflectora (Servo 2)
    if color == "ROJO": s2.value = -1
    elif color == "VERDE": s2.value = 0
    else: s2.value = 1
    sleep(1)  # Retardo de estabilización
    
    # 2. Liberar pieza (Servo 1)
    s1.value = -1
    print("Esperando 5 segundos de tránsito...")
    sleep(5)
    
    # 3. Retornar a posición de espera
    s1.value = 1
    print("Sistema listo para siguiente lectura.")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("iot/sensor/color", qos=1)  # Asegura entrega del mensaje
client.on_message = on_message

client.loop_forever()