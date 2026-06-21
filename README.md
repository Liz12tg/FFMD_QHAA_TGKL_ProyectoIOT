# Sistema IoT de Clasificación Automatizada de Objetos por Color

Este repositorio contiene el desarrollo completo de una estación inteligente de clasificación y separación física de piezas automatizada basándose en visión por computadora e Internet de las Cosas (IoT). El proyecto está diseñado e implementado bajo los lineamientos académicos de la Escuela Superior de Cómputo (**ESCOM - IPN**).

El sistema utiliza una **Raspberry Pi** que realiza la adquisición de imágenes en tiempo real, procesa el color de los objetos mediante la segmentación en el espacio de color **HSV** con **OpenCV**, persiste el historial en **SQLite** y distribuye la telemetría y comandos asíncronos a través del protocolo **MQTT**. Los resultados y métricas del sistema se visualizan en un **Dashboard Web** dinámico.

---

## ⚙️ Arquitectura del Sistema

El proyecto está estructurado bajo una arquitectura distribuida desacoplada en tres capas principales:

1. **Capa Edge (Hardware e Infraestructura):**
* Una **Raspberry Pi** actúa como el nodo central de cómputo embebido.
* Un **Módulo de Cámara RPi** conectado al puerto FLEX (CSI) captura el entorno de análisis.
* Dos servomotores controlados por hardware mediante modulación por ancho de pulsos (**PWM**) ejecutan las tareas mecánicas.


2. **Capa de Red (Protocolo de Comunicación):**
* Agente de mensajería (Broker) **Eclipse Mosquitto** desplegado localmente en la IP `192.168.1.72`.
* Comunicación basada en el patrón Publicador/Suscriptor con nivel de calidad de servicio **QoS 1** para garantizar la entrega de datos críticos.


3. **Capa de Aplicación y Visualización:**
* Servidor HTTP embebido en Python (`query_db.py`) encargado de exponer APIs REST en el puerto `8000`.
* Base de datos transaccional **SQLite** (`historial.db`) para el almacenamiento persistente.
* **Dashboard Web** asíncrono (`index.html`) que consume los endpoints de base de datos y se conecta al Broker vía WebSockets (puerto `9001`) para graficar telemetría en tiempo real mediante **Chart.js**.



---

## 🔌 Conexiones de Hardware (Pinout)

Para garantizar la estabilidad del sistema, los periféricos y actuadores están conectados estrictamente a los siguientes pines físicos del cabezal GPIO de la Raspberry Pi:
<img width="857" height="432" alt="image" src="https://github.com/user-attachments/assets/6e0ab387-6c0c-467e-a870-23ebea786af3" />

> ⚠️ **Nota de seguridad:** Se recomienda compartir una tierra común (`GND`) robusta entre la Raspberry Pi y las fuentes externas si los servomotores demandan picos elevados de corriente que puedan provocar reinicios o *brownouts* en la placa.

---

## 🗂️ Árbol de Tópicos MQTT

La jerarquía semántica configurada en el Broker Mosquitto para la distribución de la telemetría del proyecto es la siguiente:

```text
iot/
└── sensor/
    └── color    --> Mensajes válidos (Payload): "ROJO", "VERDE", "AZUL"

```

---

## 🚀 Estructura del Código

El repositorio está organizado de forma modular para separar las responsabilidades de adquisición, control, visualización y validación:

```text
.
├── index.html          # Interfaz gráfica del Dashboard (HTML5, Paho MQTT, Chart.js)
├── query_db.py         # Servidor web HTTP y API REST de consulta a SQLite y Sysinfo
├── src/
│   ├── main.py         # Script principal: Controla rpicam-still, procesa HSV y publica en MQTT
│   └── actuador.py     # Script suscriptor: Escucha el tópico de color y controla los Servos 1 y 2
└── tests/
    ├── test_camara.py  # Script de pruebas aisladas para la cámara y OpenCV
    ├── test_color.py   # Suite de pruebas unitarias para los rangos y umbrales de color HSV
    └── test_servos.py  # Validación independiente de la calibración PWM de los servomotores

```

---

## 🛠️ Instalación y Despliegue

### 1. Prerrequisitos en la Raspberry Pi

Asegúrate de actualizar el sistema operativo e instalar las dependencias esenciales de compilación y control de hardware:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-opencv python3-pip mosquitto mosquitto-clients pigpio python3-pigpio

```

Habilita e inicia los servicios del sistema del Broker y el demonio de GPIO:

```bash
sudo systemctl enable mosquitto && sudo systemctl start mosquitto
sudo systemctl enable pigpiod && sudo systemctl start pigpiod

```

### 2. Clonar el repositorio e instalar librerías de Python

```bash
git clone https://github.com/tu-usuario/ffmd_qhaa_tgkl_proyectoiot.git
cd ffmd_qhaa_tgkl_proyectoiot
pip3 install paho-mqtt gpiozero

```

### 3. Configuración de Mosquitto para WebSockets

Para permitir que el Dashboard Web reciba datos en tiempo real desde el navegador, añade la configuración de WebSockets al archivo `/etc/mosquitto/mosquitto.conf`:

```text
listener 1883
allow_anonymous true

listener 9001
protocol websockets
allow_anonymous true

```

Reinicia el servicio: `sudo systemctl restart mosquitto`.

---

## 🏃 Execution / Modo de Uso

El sistema puede ejecutarse e integrarse por componentes independientes para facilitar la depuración en producción:

### Paso 1: Levantar el backend de Base de Datos y Servidor Web

Este script expone la API REST de telemetría histórica y estadísticas del sistema (CPU, Memoria, Temperatura):

```bash
python3 query_db.py

```

### Paso 2: Iniciar el nodo Actuador (Suscriptor)

Mantiene a los servomotores escuchando de manera asíncrona las órdenes enviadas por el Broker:

```bash
python3 src/actuador.py

```

### Paso 3: Lanzar el script de análisis principal (Publicador)

Toma las capturas con la cámara, calcula el canal *Hue* en OpenCV, inserta de manera transaccional el registro en SQLite y publica la clasificación en el Broker:

```bash
python3 src/main.py

```

### Paso 4: Visualización

Abre el archivo `index.html` en cualquier navegador web dentro de la misma red local (`http://192.168.1.72:8000` o mapeado en tu servidor web).

---

## 🧪 Suite de Validación (Pruebas Unitarias)

Antes de realizar integraciones en caliente en el script principal, ejecuta las pruebas unitarias ubicadas en el directorio `tests/` para certificar el correcto funcionamiento por bloques aislados:

* **Validar cámara y visualización OpenCV:**
```bash
python3 tests/test_camara.py

```


* **Validar precisión matemática del algoritmo de rangos HSV:**
```bash
python3 tests/test_color.py

```


* **Probar y calibrar anchos de banda y ángulos de los servomotores:**
```bash
python3 tests/test_servos.py

```



---

*Desarrollado para la materia de Internet de las Cosas - ESCOM IPN.*
