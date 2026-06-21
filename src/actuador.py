import paho.mqtt.client as mqtt
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Configuración
factory = PiGPIOFactory()
s1 = Servo(17, pin_factory=factory)
s2 = Servo(18, pin_factory=factory)

# Inicialización
s1.value = 1
print("Sistema listo. Esperando color...")

def on_message(client, userdata, msg):
    color = msg.payload.decode()
    print(f"Recibido: {color}. Ejecutando acción...")
    
    # Mover Servo 2 según el color
    if color == "ROJO": s2.value = -1
    elif color == "VERDE": s2.value = 0
    else: s2.value = 1
    
    sleep(1)
    
    # Mover Servo 1 a -1 y esperar
    s1.value = -1
    print("Esperando 5 segundos...")
    sleep(5)
    
    # Regresar a inicio
    s1.value = 1
    print("Sistema listo para siguiente lectura.")

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("iot/sensor/color", qos=1)
client.on_message = on_message

client.loop_forever()
