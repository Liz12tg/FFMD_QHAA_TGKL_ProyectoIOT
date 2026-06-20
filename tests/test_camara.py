import os
import cv2
os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")
if cv2.imread('/tmp/foto.jpg') is not None:
    print("Prueba de camara: OK")
else:
    print("Error")
