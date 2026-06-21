from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
factory = PiGPIOFactory()
s1, s2 = Servo(17, pin_factory=factory), Servo(18, pin_factory=factory)
print("Probando servos...")
s1.mid(); s2.mid(); sleep(2)
