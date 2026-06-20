from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import cv2, numpy as np, os

factory = PiGPIOFactory()
s1 = Servo(17, pin_factory=factory)
s2 = Servo(18, pin_factory=factory)

s1.value = -0.5
sleep(1)

os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")

frame = cv2.imread('/tmp/foto.jpg')
h = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 0])

if h < 25 or h > 160:
    print("Color: ROJO")
    s2.min()
elif 30 < h < 85:
    print("Color: VERDE")
    s2.mid()
else:
    print("Color: AZUL")
    s2.max()

sleep(2)
s1.value = -1