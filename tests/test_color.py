import cv2, numpy as np, os

os.system("rpicam-still -n -t 100 -o /tmp/foto.jpg")

h = np.mean(
    cv2.cvtColor(
        cv2.imread('/tmp/foto.jpg'),
        cv2.COLOR_BGR2HSV
    )[:, :, 0]
)

print(
    f"Resultado: {'ROJO' if h < 25 or h > 160 else ('VERDE' if 30 < h < 85 else 'AZUL')}"
)