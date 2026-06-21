import sqlite3, json, os, subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler

class DBHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/historial':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            db = sqlite3.connect('historial.db')
            rows = db.execute("SELECT color, fecha FROM registros ORDER BY id DESC LIMIT 10").fetchall()
            db.close()
            self.wfile.write(json.dumps(rows).encode())
        elif self.path == '/sysinfo':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Obtener datos de la RPi
            cpu = subprocess.check_output("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'", shell=True).decode().strip()
            mem = subprocess.check_output("free -m | awk 'NR==2{printf \"%.1f\", $3*100/$2 }'", shell=True).decode().strip()
            temp = os.popen("vcgencmd measure_temp").readline().replace("temp=","").strip()
            info = {"cpu": cpu, "mem": mem, "temp": temp}
            self.wfile.write(json.dumps(info).encode())
        else:
            super().do_GET()

print("Servidor iniciado en puerto 8000...")
HTTPServer(('', 8000), DBHandler).serve_forever()
